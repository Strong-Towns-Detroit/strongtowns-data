"""Schema-1 compatibility adapters over the shared OSM implementation."""

import json
from pathlib import Path

import pandas as pd

from strongtowns_data.osm.acquisition import collect_pois
from strongtowns_data.osm.features import prepare_features, routing_points

DEFAULT_POI_TAGS = dict.fromkeys(("amenity", "shop", "office", "tourism", "leisure"), True)


def _legacy(frame):
    result = frame.drop(columns=["source_tags_json", "category_value"], errors="ignore").copy()
    pairs = [
        [(k, tags[k]) for k in DEFAULT_POI_TAGS if tags.get(k) not in (None, "", [])]
        for tags in frame.source_tags_json.map(json.loads)
    ]
    import pyarrow as pa

    dtype = pd.ArrowDtype(pa.list_(pa.string()))
    result["tag_keys"] = pd.Series([[k for k, _ in row] for row in pairs], dtype=dtype)
    result["tag_values"] = pd.Series([[str(v) for _, v in row] for row in pairs], dtype=dtype)
    return result


def prepare_osm_source(frame, *, return_rejected=False):
    source, rejected = prepare_features(frame, category_keys=tuple(DEFAULT_POI_TAGS))
    result = _legacy(source)
    # Retain the original rejection-table columns for schema-1 callers.
    rejected = rejected[["source_row", "source_id", "reason"]]
    return (result, rejected) if return_rejected else result


def normalize_osm_features(frame, *, return_rejected=False):
    points, rejected = routing_points(frame, category_order=tuple(DEFAULT_POI_TAGS))
    result = _legacy(points)
    rejected = rejected[["source_row", "source_id", "reason"]]
    return (result, rejected) if return_rejected else result


def collect_osm_pois(output: Path, *, place="Detroit, Michigan, USA", tags=None, cache_root):
    """Legacy source schema; all network acquisition lives in osm.acquisition."""
    import geopandas as gpd

    output = Path(output)
    metadata = collect_pois(
        output.parent, place=place, tags=tags or DEFAULT_POI_TAGS, cache_root=cache_root
    )
    source = gpd.read_parquet(output.parent / "raw.parquet")
    _legacy(source).to_parquet(output, index=False)
    return metadata
