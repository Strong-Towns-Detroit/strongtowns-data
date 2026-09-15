"""Collect and normalize a broad OpenStreetMap POI catalog.

The collector deliberately gathers a broad source catalog. Decisions about whether a POI is
a grocery, a useful grocery, or relevant to a later score belong in downstream enrichment.
"""

from __future__ import annotations

import json
from pathlib import Path

import geopandas as gpd

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


def normalize_osm_pois(features: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """Preserve the public schema and shop-first precedence through an adapter."""
    from strongtowns_data.osm.features import routing_points

    points, rejected = routing_points(features, category_order=_CATEGORY_KEYS)
    tags = points.source_tags_json.map(json.loads)
    result = points.rename(
        columns={"source_id": "poi_id", "osm_type": "source_element_type", "osm_id": "source_id"}
    ).drop(columns="routing_point_method")
    result["source"] = "openstreetmap"
    result["name"] = tags.map(
        lambda t: next(
            (t[k] for k in ("name", "brand", "operator") if t.get(k) not in (None, "")), None
        )
    )
    result["longitude"] = points.geometry.x
    result["latitude"] = points.geometry.y
    result["source_tags_json"] = tags.map(
        lambda t: json.dumps({k: t[k] for k in _DISPLAY_FIELDS if k in t}, sort_keys=True)
    )
    result = result[
        [
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
    ]
    result.attrs["rejections"] = rejected.to_dict("records")
    return result


def collect_osm_pois(*, place=None, boundary=None, tags=DEFAULT_OSM_TAGS):
    """Compatibility entry point for explicit acquisition; returns raw + points."""
    from strongtowns_data.osm.acquisition import acquire_features

    result = acquire_features(place=place, boundary=boundary, tags=tags)
    result.data.attrs["acquisition"] = result.metadata
    return result.data, normalize_osm_pois(result.data)


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
