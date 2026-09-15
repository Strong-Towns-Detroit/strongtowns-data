"""Pure OSM source preparation and routing-point derivation (schema 2)."""

from __future__ import annotations

import json
from collections.abc import Mapping

import geopandas as gpd
import numpy as np
import pandas as pd

DEFAULT_POI_TAGS = dict.fromkeys(("amenity", "shop", "office", "tourism", "leisure", "craft"), True)
SOURCE_COLUMNS = ("source_id", "osm_type", "osm_id", "source_tags_json")
POINT_COLUMNS = (
    *SOURCE_COLUMNS,
    "primary_category",
    "category_value",
    "routing_point_method",
    "source_geometry_type",
)
REJECT_COLUMNS = ("source_row", "source_id", "reason", "source_tags_json", "geometry_wkb")
IDENTITY_COLUMNS = {"element", "element_type", "osm_type", "id", "osmid", "osm_id", "source_id"}


def plain(value):
    """JSON-safe values, retaining list structure and explicit nulls within lists."""
    if isinstance(value, Mapping):
        return {str(k): plain(v) for k, v in sorted(value.items())}
    if isinstance(value, (list, tuple, np.ndarray)):
        return [plain(v) for v in value]
    if isinstance(value, set):
        return sorted((plain(v) for v in value), key=lambda v: json.dumps(v, sort_keys=True))
    if value is None or value is pd.NA or pd.isna(value):
        return None
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, (str, int, float, bool)):
        return value
    return str(value)


def json_tags(tags):
    return json.dumps(tags, sort_keys=True, ensure_ascii=False, allow_nan=False)


def category(tags, order):
    return next(
        ((key, tags[key]) for key in order if tags.get(key) not in (None, "", [])), (None, None)
    )


def _frame(rows, columns, crs="EPSG:4326"):
    result = gpd.GeoDataFrame(rows, columns=[*columns, "geometry"], geometry="geometry", crs=crs)
    for name in columns:
        result[name] = result[name].astype("string")
    return result


def _rejects(rows):
    result = pd.DataFrame(rows, columns=REJECT_COLUMNS)
    result["source_row"] = result.source_row.astype("int64")
    for column in REJECT_COLUMNS[1:]:
        result[column] = result[column].astype("string")
    return result


def _identity(index, row):
    if isinstance(index, tuple) and len(index) == 2:
        element, identity = index
    else:
        element = next(
            (
                row[k]
                for k in ("osm_type", "element", "element_type", "type")
                if k in row and plain(row[k]) is not None
            ),
            None,
        )
        identity = next(
            (row[k] for k in ("osm_id", "osmid", "id") if k in row and plain(row[k]) is not None),
            None,
        )
    if element not in ("node", "way", "relation") or identity is None:
        raise ValueError("OSM feature lacks a valid element type/id")
    # Numeric OSM identifiers must not change to '123.0' after nullable-frame coercion.
    if isinstance(identity, (float, np.floating)) and identity.is_integer():
        identity = int(identity)
    identity = str(identity)
    if not identity.isdecimal() or int(identity) <= 0:
        raise ValueError("OSM feature lacks a valid element id")
    return str(element), identity


def prepare_features(frame, *, category_keys=None):
    """Preserve tags and source geometry; account for every rejected source row.

    ``category_keys`` optionally requires a selected category tag (POI contract).
    Without it, this same source representation also supports water features.
    """
    if frame.crs is None:
        raise ValueError("OSM features must have a CRS")
    source = frame.to_crs("EPSG:4326")
    rows, rejected, seen = [], [], set()
    prepared = set(SOURCE_COLUMNS) <= set(source.columns)
    legacy = {"osm_type", "osm_id", "tag_keys", "tag_values"} <= set(source.columns)
    for position, (index, row) in enumerate(source.iterrows()):
        element, identity = _identity(index, row)
        source_id = f"osm:{element}:{identity}"
        if source_id in seen:
            raise ValueError(f"duplicate OSM source identity: {source_id}")
        seen.add(source_id)
        if prepared:
            if row.source_id != source_id:
                raise ValueError("OSM source identity disagrees with element type/id")
            tags = json.loads(row.source_tags_json)
            if not isinstance(tags, dict):
                raise ValueError("OSM source tags must be a JSON object")
        elif legacy:
            if len(row.tag_keys) != len(row.tag_values):
                raise ValueError("OSM tag key/value counts disagree")
            tags = dict(zip(row.tag_keys, row.tag_values))
        else:
            tags = {
                str(k): plain(v)
                for k, v in row.items()
                if k != source.geometry.name and k not in IDENTITY_COLUMNS and plain(v) is not None
            }
        serialized = json_tags(tags)
        geometry = source.geometry.iloc[position]
        if pd.isna(geometry):
            geometry = None
        reason = None
        if geometry is None or geometry.is_empty:
            reason = "missing_geometry"
        elif not geometry.is_valid:
            reason = "invalid_geometry"
        elif geometry.geom_type not in (
            "Point",
            "MultiPoint",
            "LineString",
            "MultiLineString",
            "Polygon",
            "MultiPolygon",
        ):
            reason = "unsupported_geometry"
        elif category_keys is not None and category(tags, category_keys)[0] is None:
            reason = "missing_tags"
        if reason:
            rejected.append(
                (
                    position,
                    source_id,
                    reason,
                    serialized,
                    geometry.wkb_hex if geometry is not None else None,
                )
            )
            continue
        rows.append((source_id, element, identity, serialized, geometry))
    accepted = _frame(rows, SOURCE_COLUMNS).sort_values("source_id").reset_index(drop=True)
    return accepted, _rejects(rejected)


def routing_points(frame, *, category_order=tuple(DEFAULT_POI_TAGS)):
    """Derive point geometry while retaining tags and the interpretation method."""
    source, rejected = prepare_features(frame, category_keys=category_order)
    rows = []
    for row in source.itertuples():
        key, value = category(json.loads(row.source_tags_json), category_order)
        geometry = row.geometry
        method = "source_point" if geometry.geom_type == "Point" else "representative_point"
        rows.append(
            (
                row.source_id,
                row.osm_type,
                row.osm_id,
                row.source_tags_json,
                key,
                value if isinstance(value, str) else json_tags(value),
                method,
                geometry.geom_type,
                geometry if method == "source_point" else geometry.representative_point(),
            )
        )
    return _frame(rows, POINT_COLUMNS), rejected
