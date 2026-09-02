"""Parcel-keyed client for TravelTime time-map polygons.

This module only collects geometry and request provenance. It does not select POIs, combine
directions, or score parcels.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
from itertools import islice
from typing import Literal

import requests

TIME_MAP_URL = "https://api.traveltimeapp.com/v4/time-map"
MAX_SEARCHES_PER_REQUEST = 10


@dataclass(frozen=True)
class ParcelAnchor:
    parcel_id: str
    anchor_id: str
    latitude: float
    longitude: float

    def __post_init__(self):
        if not self.parcel_id.strip():
            raise ValueError("parcel_id cannot be empty")
        if not self.anchor_id.strip():
            raise ValueError("anchor_id cannot be empty")
        if not -90 <= self.latitude <= 90:
            raise ValueError(f"invalid latitude for {self.parcel_id!r}")
        if not -180 <= self.longitude <= 180:
            raise ValueError(f"invalid longitude for {self.parcel_id!r}")


@dataclass(frozen=True)
class TimeMapSpec:
    direction: Literal["departure", "arrival"]
    transportation: str
    travel_time_seconds: int
    reference_time: datetime

    def __post_init__(self):
        if self.direction not in {"departure", "arrival"}:
            raise ValueError("direction must be 'departure' or 'arrival'")
        if not self.transportation.strip():
            raise ValueError("transportation cannot be empty")
        if self.travel_time_seconds <= 0:
            raise ValueError("travel_time_seconds must be positive")
        if self.reference_time.tzinfo is None:
            raise ValueError("reference_time must include a timezone")


def _batched(items, size):
    iterator = iter(items)
    while batch := tuple(islice(iterator, size)):
        yield batch


def search_id(parcel: ParcelAnchor, spec: TimeMapSpec) -> str:
    """Create a reversible identifier that links every polygon to a parcel and spec."""
    parcel_token = parcel.parcel_id.replace(":", "_")
    anchor_token = parcel.anchor_id.replace(":", "_")
    return (
        f"parcel:{parcel_token}:anchor:{anchor_token}:"
        f"{spec.direction}:{spec.transportation}:{spec.travel_time_seconds}"
    )


def build_time_map_payload(
    parcels: list[ParcelAnchor] | tuple[ParcelAnchor, ...], spec: TimeMapSpec
) -> dict:
    """Build one TravelTime request body for at most ten parcel points."""
    if not parcels:
        raise ValueError("at least one parcel point is required")
    if len(parcels) > MAX_SEARCHES_PER_REQUEST:
        raise ValueError(f"a time-map request supports at most {MAX_SEARCHES_PER_REQUEST} searches")

    searches = []
    time_key = "departure_time" if spec.direction == "departure" else "arrival_time"
    for parcel in parcels:
        searches.append(
            {
                "id": search_id(parcel, spec),
                "coords": {"lat": parcel.latitude, "lng": parcel.longitude},
                time_key: spec.reference_time.isoformat(),
                "travel_time": spec.travel_time_seconds,
                "transportation": {"type": spec.transportation},
            }
        )
    return {f"{spec.direction}_searches": searches}


def collect_time_maps(
    parcels: list[ParcelAnchor],
    specs: list[TimeMapSpec],
    *,
    app_id: str,
    api_key: str,
    session=requests,
    timeout: int = 120,
) -> tuple[dict, dict]:
    """Collect GeoJSON polygons for every parcel/spec combination in batches of ten."""
    if not parcels:
        raise ValueError("at least one parcel point is required")
    if not specs:
        raise ValueError("at least one time-map specification is required")
    if not app_id or not api_key:
        raise ValueError("TravelTime application id and API key are required")

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/geo+json",
        "X-Application-Id": app_id,
        "X-Api-Key": api_key,
    }
    features = []
    requests_made = []
    for spec in specs:
        for batch in _batched(parcels, MAX_SEARCHES_PER_REQUEST):
            payload = build_time_map_payload(batch, spec)
            response = session.post(TIME_MAP_URL, headers=headers, json=payload, timeout=timeout)
            response.raise_for_status()
            data = response.json()
            if data.get("type") != "FeatureCollection":
                raise ValueError("TravelTime did not return a GeoJSON FeatureCollection")
            features.extend(data.get("features", []))
            requests_made.append(
                {
                    "direction": spec.direction,
                    "transportation": spec.transportation,
                    "travel_time_seconds": spec.travel_time_seconds,
                    "reference_time": spec.reference_time.isoformat(),
                    "anchors": [
                        {"parcel_id": parcel.parcel_id, "anchor_id": parcel.anchor_id}
                        for parcel in batch
                    ],
                }
            )

    feature_collection = {"type": "FeatureCollection", "features": features}
    manifest = {
        "endpoint": TIME_MAP_URL,
        "parcel_count": len({parcel.parcel_id for parcel in parcels}),
        "anchor_count": len(parcels),
        "specifications": [
            {
                **asdict(spec),
                "reference_time": spec.reference_time.isoformat(),
            }
            for spec in specs
        ],
        "requests": requests_made,
        "feature_count": len(features),
    }
    return feature_collection, manifest
