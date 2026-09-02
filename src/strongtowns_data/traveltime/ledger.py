"""Deterministic TravelTime request identities and strict result reconciliation."""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass
from datetime import UTC, datetime
from email.utils import parsedate_to_datetime
from typing import Literal

import pandas as pd
import requests
from shapely.geometry import shape

from strongtowns_data.traveltime.client import MAX_SEARCHES_PER_REQUEST, TIME_MAP_URL

REQUEST_NAMESPACE = uuid.UUID("099ef5f2-e70e-563b-8c57-40fd7df979d3")
REQUEST_CONTRACT_VERSION = "1.0.0"


@dataclass(frozen=True)
class LedgerSpec:
    direction: Literal["departure", "arrival"]
    transportation: str
    travel_time_seconds: int
    reference_time_utc: datetime

    def __post_init__(self):
        if self.direction not in {"departure", "arrival"}:
            raise ValueError("invalid direction")
        if not self.transportation.strip():
            raise ValueError("transportation cannot be empty")
        if not 0 < self.travel_time_seconds <= 3600:
            raise ValueError("travel_time_seconds must be between 1 and 3600")
        if self.reference_time_utc.tzinfo is None:
            raise ValueError("reference_time_utc must be timezone-aware")


def request_uuid(anchor_uuid: str, spec: LedgerSpec) -> str:
    reference = spec.reference_time_utc.astimezone(UTC).isoformat()
    identity = "\x1f".join(
        (
            "traveltime",
            REQUEST_CONTRACT_VERSION,
            anchor_uuid,
            spec.direction,
            spec.transportation,
            str(spec.travel_time_seconds),
            reference,
        )
    )
    return str(uuid.uuid5(REQUEST_NAMESPACE, identity))


def prepare_request_records(
    anchors: pd.DataFrame,
    dispositions: pd.DataFrame,
    specs: list[LedgerSpec],
    *,
    override_anchor_uuids: set[str] | None = None,
) -> list[dict]:
    """Select provider-eligible anchors and create stable request/provider mappings."""
    overrides = override_anchor_uuids or set()
    if anchors["anchor_uuid"].duplicated().any():
        raise ValueError("anchors must be unique")
    if dispositions["anchor_uuid"].duplicated().any():
        raise ValueError("anchor dispositions must be unique")
    anchor_ids = set(anchors["anchor_uuid"])
    disposition_ids = set(dispositions["anchor_uuid"])
    if anchor_ids != disposition_ids:
        raise ValueError(
            "anchor/disposition coverage differs: "
            f"missing={len(anchor_ids - disposition_ids)}, "
            f"unexpected={len(disposition_ids - anchor_ids)}"
        )
    invalid_statuses = set(dispositions["review_status"]) - {
        "not_required",
        "required",
        "approved",
        "rejected",
    }
    if invalid_statuses:
        raise ValueError(f"invalid review statuses: {sorted(invalid_statuses)}")
    joined = anchors.merge(dispositions, on="anchor_uuid", validate="one_to_one")
    unknown_overrides = overrides - anchor_ids
    if unknown_overrides:
        raise ValueError(f"unknown override anchors: {sorted(unknown_overrides)}")
    records = []
    for row in joined.itertuples():
        override = row.anchor_uuid in overrides
        if row.review_status == "rejected":
            if override:
                raise ValueError(f"rejected anchor cannot be overridden: {row.anchor_uuid}")
            continue
        eligible = row.review_status in {"not_required", "approved"} or (
            row.review_status == "required" and override
        )
        if not eligible:
            continue
        for spec in specs:
            identifier = request_uuid(row.anchor_uuid, spec)
            records.append(
                {
                    "request_uuid": identifier,
                    "provider_search_id": f"kr-{uuid.UUID(identifier).hex}",
                    "anchor_uuid": row.anchor_uuid,
                    "parcel_id": str(row.parcel_id),
                    "direction": spec.direction,
                    "transportation": spec.transportation,
                    "travel_time_seconds": spec.travel_time_seconds,
                    "reference_time_utc": spec.reference_time_utc.astimezone(UTC),
                    "latitude": float(row.latitude),
                    "longitude": float(row.longitude),
                    "selection_override": override,
                }
            )
    if len({record["request_uuid"] for record in records}) != len(records):
        raise ValueError("request identity collision or duplicate specification")
    return records


def payload_for_records(records: list[dict]) -> dict:
    if not 0 < len(records) <= MAX_SEARCHES_PER_REQUEST:
        raise ValueError(f"a batch must contain 1-{MAX_SEARCHES_PER_REQUEST} records")
    directions = {record["direction"] for record in records}
    if len(directions) != 1:
        raise ValueError("a TravelTime batch cannot mix directions")
    direction = directions.pop()
    time_key = "departure_time" if direction == "departure" else "arrival_time"
    searches = []
    for record in records:
        searches.append(
            {
                "id": record["provider_search_id"],
                "coords": {"lat": record["latitude"], "lng": record["longitude"]},
                time_key: record["reference_time_utc"].isoformat(),
                "travel_time": record["travel_time_seconds"],
                "transportation": {"type": record["transportation"]},
            }
        )
    return {f"{direction}_searches": searches}


def reconcile_response(records: list[dict], response: dict, received_at: datetime) -> list[dict]:
    """Require every expected provider ID to resolve exactly once as success or error."""
    expected = {record["provider_search_id"]: record for record in records}
    if len(expected) != len(records):
        raise ValueError("request ledger contains duplicate provider IDs")
    resolved: dict[str, dict] = {}
    if response.get("type") != "FeatureCollection":
        raise ValueError("TravelTime response is not a GeoJSON FeatureCollection")
    for feature in response.get("features", []):
        properties = feature.get("properties") or {}
        provider_id = properties.get("search_id") or properties.get("id")
        if provider_id not in expected:
            raise ValueError(f"unexpected provider result id: {provider_id!r}")
        if provider_id in resolved:
            raise ValueError(f"duplicate provider result id: {provider_id}")
        geometry_document = feature.get("geometry")
        if not geometry_document:
            raise ValueError(f"empty geometry for provider result: {provider_id}")
        try:
            geometry = shape(geometry_document)
        except (TypeError, ValueError) as error:
            raise ValueError(f"malformed geometry for provider result: {provider_id}") from error
        if geometry.is_empty or geometry.geom_type not in {"Polygon", "MultiPolygon"}:
            raise ValueError(f"invalid geometry for provider result: {provider_id}")
        resolved[provider_id] = {
            "request_uuid": expected[provider_id]["request_uuid"],
            "provider_search_id": provider_id,
            "result_status": "success",
            "provider_error_code": None,
            "provider_error_message": None,
            "received_at": received_at.astimezone(UTC),
            "geometry": geometry,
        }
    for error in response.get("errors", []):
        provider_id = error.get("search_id") or error.get("id")
        if provider_id not in expected:
            raise ValueError(f"unexpected provider error id: {provider_id!r}")
        if provider_id in resolved:
            raise ValueError(f"duplicate provider resolution id: {provider_id}")
        resolved[provider_id] = {
            "request_uuid": expected[provider_id]["request_uuid"],
            "provider_search_id": provider_id,
            "result_status": "error",
            "provider_error_code": str(error.get("code") or "provider_error"),
            "provider_error_message": str(error.get("message") or ""),
            "received_at": received_at.astimezone(UTC),
            "geometry": None,
        }
    missing = sorted(set(expected) - set(resolved))
    if missing:
        raise ValueError(f"missing provider resolutions: {missing}")
    return [resolved[record["provider_search_id"]] for record in records]


def _retry_delay(response, attempt: int) -> float:
    value = response.headers.get("Retry-After") if response is not None else None
    if value:
        try:
            return min(float(value), 30.0)
        except ValueError:
            try:
                return min(
                    max((parsedate_to_datetime(value) - datetime.now(UTC)).total_seconds(), 0),
                    30.0,
                )
            except (TypeError, ValueError, OverflowError):
                pass
    return min(0.5 * 2 ** (attempt - 1), 8.0)


def post_batch_with_retry(
    records: list[dict],
    *,
    app_id: str,
    api_key: str,
    session=requests,
    timeout: int = 120,
    max_attempts: int = 5,
    sleep=time.sleep,
) -> dict:
    """Retry only transport, rate-limit, and server failures; never hide client errors."""
    if not app_id or not api_key:
        raise ValueError("TravelTime application ID and API key are required")
    if max_attempts <= 0:
        raise ValueError("max_attempts must be positive")
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/geo+json",
        "X-Application-Id": app_id,
        "X-Api-Key": api_key,
    }
    payload = payload_for_records(records)
    last_error = None
    for attempt in range(1, max_attempts + 1):
        response = None
        try:
            response = session.post(TIME_MAP_URL, headers=headers, json=payload, timeout=timeout)
            if response.status_code not in {429} and response.status_code < 500:
                response.raise_for_status()
                return response.json()
            last_error = requests.HTTPError(f"retryable HTTP {response.status_code}")
        except (requests.Timeout, requests.ConnectionError) as error:
            last_error = error
        if attempt < max_attempts:
            sleep(_retry_delay(response, attempt))
    raise RuntimeError(f"TravelTime request failed after {max_attempts} attempts") from last_error
