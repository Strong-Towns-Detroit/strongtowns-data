"""Explicit OSMnx acquisition shared by registered pipelines and legacy callers."""

from __future__ import annotations

import hashlib
import json
import shutil
import threading
from contextlib import contextmanager
from copy import deepcopy
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

import geopandas as gpd
from shapely import normalize

from .features import DEFAULT_POI_TAGS, prepare_features

SETTINGS_LOCK = threading.RLock()
ATTRIBUTION = {
    "provider": "OpenStreetMap",
    "attribution": "© OpenStreetMap contributors",
    "license": "ODbL-1.0",
    "license_url": "https://www.openstreetmap.org/copyright",
}
QUERY_SETTINGS = (
    "overpass_url",
    "overpass_settings",
    "overpass_memory",
    "requests_timeout",
    "max_query_area_size",
    "default_access",
    "bidirectional_network_types",
    "useful_tags_node",
    "useful_tags_way",
    "nominatim_url",
)


def fingerprint(value):
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def file_hash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


@contextmanager
def settings_session(*, cache_root=Path("cache/osm"), endpoint=None):
    """Serialize OSMnx settings changes and restore them even after a failure."""
    import osmnx as ox

    with SETTINGS_LOCK:
        changed = {"use_cache": True, "cache_folder": str(Path(cache_root).resolve())}
        if endpoint is not None:
            changed["overpass_url"] = endpoint
        previous = {key: deepcopy(getattr(ox.settings, key)) for key in changed}
        try:
            for key, value in changed.items():
                setattr(ox.settings, key, value)
            yield ox
        finally:
            for key, value in previous.items():
                setattr(ox.settings, key, value)


@dataclass
class Acquisition:
    data: object
    boundary: gpd.GeoDataFrame
    metadata: dict
    cache: Path


def _boundary(ox, *, place=None, boundary=None, point=None, dist=None):
    if sum(x is not None for x in (place, boundary, point)) != 1:
        raise ValueError("provide exactly one of place=, boundary=, or point=+dist=")
    if place is not None:
        frame = ox.geocode_to_gdf(place).to_crs("EPSG:4326")
    elif boundary is not None:
        if isinstance(boundary, gpd.GeoDataFrame):
            if boundary.crs is None:
                raise ValueError("Boundary must have a CRS")
            frame = boundary.to_crs("EPSG:4326")
        else:
            frame = gpd.GeoDataFrame(geometry=[boundary], crs="EPSG:4326")
    else:
        if dist is None or dist <= 0:
            raise ValueError("point= requires a positive dist= in metres")
        from shapely.geometry import box

        frame = gpd.GeoDataFrame(
            geometry=[box(*ox.utils_geo.bbox_from_point(point, dist))], crs="EPSG:4326"
        )
    if frame.empty or frame.geometry.isna().any() or not frame.geometry.is_valid.all():
        raise ValueError("OSM query boundary is empty or invalid")
    polygon = frame.geometry.union_all()
    if polygon.is_empty or polygon.geom_type not in ("Polygon", "MultiPolygon"):
        raise ValueError("OSM query boundary must be polygonal")
    return frame, polygon


def acquire(
    kind,
    *,
    place=None,
    boundary=None,
    point=None,
    dist=None,
    tags=None,
    cache_root=Path("cache/osm"),
    endpoint=None,
    **graph_options,
):
    """Acquire boundaries, features, or a graph; exceptions never become empty data.

    OSM response JSON is retained in a query-specific cache, with content hashes.
    The query fingerprint includes resolved geometry and OSMnx interpretation settings.
    """
    if kind not in ("boundary", "features", "graph"):
        raise ValueError(f"Unknown OSM acquisition kind: {kind}")
    started = datetime.now(UTC).isoformat()
    cache_root = Path(cache_root)
    with settings_session(cache_root=cache_root / "geocoding", endpoint=endpoint) as ox:
        bounds, polygon = _boundary(ox, place=place, boundary=boundary, point=point, dist=dist)
        settings = {key: deepcopy(getattr(ox.settings, key)) for key in QUERY_SETTINGS}
        query = {
            "kind": kind,
            "place": place,
            "point": point,
            "dist": dist,
            "boundary_sha256": hashlib.sha256(normalize(polygon).wkb).hexdigest(),
            "tags": tags,
            "graph_options": graph_options,
            "settings": settings,
            "osmnx_version": ox.__version__,
        }
        digest = fingerprint(query)
        cache = cache_root / digest
        cache.mkdir(parents=True, exist_ok=True)
        # Retain geocoding responses alongside the query rather than losing the
        # provenance of the resolved place boundary.
        for path in (cache_root / "geocoding").glob("*.json"):
            shutil.copy2(path, cache / path.name)
        ox.settings.cache_folder = str(cache.resolve())
        if kind == "boundary":
            data = bounds
        elif kind == "features":
            if not tags:
                raise ValueError("Feature acquisition requires explicit nonempty tags")
            data = ox.features_from_polygon(polygon, tags=dict(tags))
        elif point is not None:
            # Preserve graph_from_point's historical bounding/truncation semantics.
            data = ox.graph_from_point(point, dist=dist, **graph_options)
        else:
            data = ox.graph_from_polygon(polygon, **graph_options)
        responses = {}
        for path in sorted(cache.glob("*.json")):
            response = json.loads(path.read_text())
            if isinstance(response, dict) and response.get("remark"):
                raise ValueError(
                    f"Incomplete Overpass response in {path.name}: {response['remark']}"
                )
            responses[path.name] = file_hash(path)
    return Acquisition(
        data,
        bounds,
        {
            **ATTRIBUTION,
            "query": query,
            "cache_fingerprint": digest,
            "boundary_sha256": query["boundary_sha256"],
            "endpoint": settings["overpass_url"],
            "osmnx_version": query["osmnx_version"],
            "response_hashes": responses,
            "started_at": started,
            "completed_at": datetime.now(UTC).isoformat(),
            "transaction_quality": "best_effort",
            "osm_as_of": None,
            "cache_policy": "verified response reuse; collection times are not OSM snapshot dates",
        },
        cache,
    )


def acquire_features(*, tags=None, **kwargs):
    return acquire("features", tags=DEFAULT_POI_TAGS if tags is None else tags, **kwargs)


def acquire_graph(**kwargs):
    return acquire("graph", **kwargs)


def acquire_boundaries(**kwargs):
    return acquire("boundary", **kwargs)


def write_provenance(result, output):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    result.boundary.to_parquet(output / "boundary.parquet", index=False)
    (output / "acquisition.json").write_text(json.dumps(result.metadata, indent=2) + "\n")
    responses = output / "responses"
    responses.mkdir(exist_ok=True)
    for name, digest in result.metadata["response_hashes"].items():
        source = result.cache / name
        if file_hash(source) != digest:
            raise ValueError("OSM response cache changed during acquisition")
        shutil.copy2(source, responses / name)


def collect_pois(
    output,
    *,
    place="Detroit, Michigan, USA",
    cache_root=Path("cache/osm"),
    tags=None,
    boundary=None,
):
    if boundary is not None:
        place = None
    tags = DEFAULT_POI_TAGS if tags is None else tags
    result = acquire_features(place=place, boundary=boundary, tags=tags, cache_root=cache_root)
    source, rejects = prepare_features(result.data, category_keys=tuple(tags))
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    source.to_parquet(output / "raw.parquet", index=False)
    rejects.to_parquet(output / "rejects.parquet", index=False)
    write_provenance(result, output)
    return {
        **result.metadata,
        "input": len(result.data),
        "accepted": len(source),
        "rejected": len(rejects),
    }


def geocode_point(place, *, cache_root=Path("cache/osm")):
    """Legacy explicit point geocoding for graph coverage checks."""
    with settings_session(cache_root=Path(cache_root) / "geocoding") as ox:
        return ox.geocode(place)


def validate_acquisition(directory):
    """Verify the recorded query against its preserved boundary and response evidence."""
    directory = Path(directory)
    metadata = json.loads((directory / "acquisition.json").read_text())
    if fingerprint(metadata["query"]) != metadata["cache_fingerprint"]:
        raise ValueError("OSM query fingerprint mismatch")
    bounds = gpd.read_parquet(directory / "boundary.parquet")
    if bounds.crs is None or bounds.crs.to_epsg() != 4326:
        raise ValueError("OSM boundary CRS mismatch")
    digest = hashlib.sha256(normalize(bounds.geometry.union_all()).wkb).hexdigest()
    if digest != metadata["boundary_sha256"] or digest != metadata["query"]["boundary_sha256"]:
        raise ValueError("OSM boundary fingerprint mismatch")
    for name, digest in metadata["response_hashes"].items():
        if Path(name).name != name or file_hash(directory / "responses" / name) != digest:
            raise ValueError("OSM response evidence mismatch")
    return metadata
