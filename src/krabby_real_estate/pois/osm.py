"""Collect and normalize a broad OpenStreetMap POI catalog.

The collector deliberately gathers a broad source catalog. Decisions about whether a POI is
a grocery, a useful grocery, or relevant to a later score belong in downstream enrichment.
"""

from __future__ import annotations

import json
from collections.abc import Mapping
from pathlib import Path

import geopandas as gpd
import osmnx as ox
import pandas as pd

DEFAULT_OSM_TAGS = {
    "shop": True,
    "amenity": True,
    "leisure": True,
    "tourism": True,
    "office": True,
    "craft": True,
}

_CATEGORY_KEYS = tuple(DEFAULT_OSM_TAGS)
_DISPLAY_FIELDS = (
    "name",
    "brand",
    "operator",
    "shop",
    "amenity",
    "leisure",
    "tourism",
    "office",
    "craft",
    "opening_hours",
    "website",
    "phone",
    "addr:housenumber",
    "addr:street",
    "addr:city",
    "addr:postcode",
)


def _plain(value):
    """Convert source values to stable JSON/string-friendly scalars."""
    if value is None or value is pd.NA:
        return None
    try:
        if pd.isna(value):
            return None
    except (TypeError, ValueError):
        pass
    if isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, (list, tuple, set)):
        return [str(item) for item in value]
    return str(value)


def _first_present(row, names):
    for name in names:
        if name in row:
            value = _plain(row[name])
            if value not in (None, ""):
                return value
    return None


def _category(row):
    for key in _CATEGORY_KEYS:
        value = _plain(row.get(key))
        if value not in (None, ""):
            return key, value
    return None, None


def normalize_osm_pois(features: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """Return a stable point catalog while preserving OSM identity and source tags."""
    if features.crs is None:
        raise ValueError("OSM features must have a CRS")

    source = features.to_crs("EPSG:4326").reset_index()
    rows = []
    for _, row in source.iterrows():
        geometry = row.geometry
        if geometry is None or geometry.is_empty:
            continue
        source_geometry_type = geometry.geom_type
        point = geometry if source_geometry_type == "Point" else geometry.representative_point()
        element_type = _first_present(row, ("element", "element_type", "type")) or "feature"
        source_id = _first_present(row, ("id", "osmid", "osm_id"))
        if source_id is None:
            raise ValueError("OSM feature lacks an element id")
        category_key, category_value = _category(row)
        tags = {
            field: _plain(row.get(field))
            for field in _DISPLAY_FIELDS
            if _plain(row.get(field)) is not None
        }
        name = _first_present(row, ("name", "brand", "operator"))
        rows.append(
            {
                "poi_id": f"osm:{element_type}:{source_id}",
                "source": "openstreetmap",
                "source_element_type": str(element_type),
                "source_id": str(source_id),
                "name": name,
                "primary_category": category_key,
                "category_value": category_value,
                "source_geometry_type": source_geometry_type,
                "longitude": float(point.x),
                "latitude": float(point.y),
                "source_tags_json": json.dumps(tags, sort_keys=True),
                "geometry": point,
            }
        )

    columns = [
        "poi_id",
        "source",
        "source_element_type",
        "source_id",
        "name",
        "primary_category",
        "category_value",
        "source_geometry_type",
        "longitude",
        "latitude",
        "source_tags_json",
        "geometry",
    ]
    return gpd.GeoDataFrame(rows, columns=columns, geometry="geometry", crs="EPSG:4326")


def collect_osm_pois(
    *,
    place: str | None = None,
    boundary=None,
    tags: Mapping[str, object] = DEFAULT_OSM_TAGS,
) -> tuple[gpd.GeoDataFrame, gpd.GeoDataFrame]:
    """Collect broad OSM features for a place or polygon and return raw + normalized data."""
    if (place is None) == (boundary is None):
        raise ValueError("provide exactly one of place= or boundary=")
    if place is not None:
        raw = ox.features_from_place(place, tags=dict(tags))
    else:
        raw = ox.features_from_polygon(boundary, tags=dict(tags))
    return raw, normalize_osm_pois(raw)


def write_osm_snapshot(
    raw: gpd.GeoDataFrame,
    normalized: gpd.GeoDataFrame,
    output_dir: Path,
) -> dict[str, Path]:
    """Write source geometry and normalized routing points as separate GeoJSON files."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    raw_path = output_dir / "osm-pois.raw.geojson"
    normalized_path = output_dir / "osm-pois.normalized.geojson"
    raw.to_crs("EPSG:4326").to_file(raw_path, driver="GeoJSON")
    normalized.to_file(normalized_path, driver="GeoJSON")
    return {"raw": raw_path, "normalized": normalized_path}
