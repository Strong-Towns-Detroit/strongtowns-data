"""Derive evidence-preserving routing anchors for Detroit assessor parcels."""

from __future__ import annotations

import json
import logging
import math
import re
from collections import defaultdict
from numbers import Integral, Real

import geopandas as gpd
import pandas as pd
from shapely.ops import unary_union

from strongtowns_data.base_units.geometry import (
    estimate_street_facing_edge,
    normalize_parcel_id,
)

PROJECTED_CRS = "EPSG:2898"
OUTPUT_CRS = "EPSG:4326"
logger = logging.getLogger(__name__)


def _require_columns(frame, columns, label):
    missing = sorted(set(columns) - set(frame.columns))
    if missing:
        raise ValueError(f"{label} missing required columns: {missing}")
    if frame.crs is None:
        raise ValueError(f"{label} must declare a CRS")


def _require_unique_parcels(frame: gpd.GeoDataFrame) -> None:
    duplicates = frame.loc[frame["parcel_key"].duplicated(keep=False), "parcel_key"].unique()
    if len(duplicates):
        examples = ", ".join(map(str, sorted(duplicates)[:5]))
        raise ValueError(
            "parcels contains duplicate normalized parcel identifiers; "
            f"resolve them before routing-anchor construction (examples: {examples})"
        )


def normalize_relationship_id(value):
    """Normalize ArcGIS relationship IDs without changing genuinely textual IDs."""
    if value is None or pd.isna(value):
        return None
    if isinstance(value, Integral):
        return str(int(value))
    if isinstance(value, Real) and math.isfinite(value) and float(value).is_integer():
        return str(int(value))
    cleaned = str(value).strip()
    # GeoJSON readers may infer a nullable numeric relationship as float in one layer and
    # integer in another (for example 14966.0 versus 14966). Canonicalize only that lossless
    # representation; preserve genuinely textual identifiers unchanged.
    if re.fullmatch(r"[+-]?\d+\.0+", cleaned):
        return cleaned.split(".", 1)[0]
    return cleaned or None


def _relationship_values(group, fields) -> list[str]:
    for field in fields:
        if field in group:
            return sorted(
                {
                    normalize_relationship_id(value)
                    for value in group[field]
                    if normalize_relationship_id(value)
                }
            )
    return []


def _address_evidence(group) -> list[dict[str, str]]:
    records = []
    for _, row in group.iterrows():
        address_id = next(
            (
                normalize_relationship_id(row.get(field))
                for field in ("address_id", "objectid", "OBJECTID")
                if field in group and normalize_relationship_id(row.get(field))
            ),
            None,
        )
        source_object_id = next(
            (
                normalize_relationship_id(row.get(field))
                for field in ("source_object_id", "objectid", "OBJECTID")
                if field in group and normalize_relationship_id(row.get(field))
            ),
            None,
        )
        if address_id and source_object_id:
            records.append({"address_id": address_id, "source_object_id": source_object_id})
    return sorted(records, key=lambda item: (item["address_id"], item["source_object_id"]))


def _linked_building_counts(buildings: gpd.GeoDataFrame | None) -> dict[str, int]:
    if buildings is None or buildings.empty:
        return {}
    _require_columns(buildings, {"parcel_id", "geometry"}, "buildings")
    current = buildings.copy()
    if "status" in current:
        current = current[current["status"].fillna("").str.lower().isin({"active", "current"})]
    current["parcel_key"] = current["parcel_id"].map(normalize_parcel_id)
    return current.dropna(subset=["parcel_key"]).groupby("parcel_key").size().to_dict()


def _anchor_on_edge(edge, address_geometries):
    points = [
        geometry
        for geometry in address_geometries
        if geometry is not None and not geometry.is_empty
    ]
    if not points:
        return edge.interpolate(0.5, normalized=True), "address_linked_front_edge_midpoint"
    address_center = unary_union(points).centroid
    return (
        edge.interpolate(edge.project(address_center)),
        "address_linked_front_edge_projection",
    )


def _anchor_confidence(frontage_confidence: str, source: str) -> str:
    if source == "nearest_base_units_street":
        return "low" if frontage_confidence != "not_evaluated" else "not_evaluated"
    return frontage_confidence


def build_parcel_routing_anchors(
    parcels: gpd.GeoDataFrame,
    addresses: gpd.GeoDataFrame,
    streets: gpd.GeoDataFrame,
    *,
    buildings: gpd.GeoDataFrame | None = None,
) -> tuple[gpd.GeoDataFrame, gpd.GeoDataFrame, dict]:
    """Build one anchor per linked parcel/street pair, retaining explicit fallbacks.

    Corner and through parcels may emit multiple anchors. A parcel with no usable Base Units
    address/street relationship receives one nearest-street fallback anchor. Returned layers
    are WGS84 points and front edges, keyed by ``parcel_id + anchor_id``.
    """
    _require_columns(parcels, {"parcel_id", "geometry"}, "parcels")
    _require_columns(addresses, {"parcel_id", "street_id", "geometry"}, "addresses")
    _require_columns(streets, {"street_id", "geometry"}, "streets")

    parcel_frame = parcels[["parcel_id", "geometry"]].copy().to_crs(PROJECTED_CRS)
    parcel_frame["parcel_key"] = parcel_frame["parcel_id"].map(normalize_parcel_id)
    parcel_frame = parcel_frame.dropna(subset=["parcel_key", "geometry"])
    _require_unique_parcels(parcel_frame)

    address_frame = addresses.copy().to_crs(PROJECTED_CRS)
    address_frame["parcel_key"] = address_frame["parcel_id"].map(normalize_parcel_id)
    address_frame["street_key"] = address_frame["street_id"].map(normalize_relationship_id)
    address_frame = address_frame.dropna(subset=["parcel_key", "street_key"])

    street_frame = streets.copy().to_crs(PROJECTED_CRS)
    street_frame["street_key"] = street_frame["street_id"].map(normalize_relationship_id)
    street_frame = street_frame.dropna(subset=["street_key", "geometry"])
    if street_frame.empty:
        raise ValueError("streets contains no usable street identifiers and geometries")
    street_lookup = {
        street_key: unary_union(group.geometry.tolist())
        for street_key, group in street_frame.groupby("street_key")
    }
    nearest_tree = street_frame.sindex
    building_counts = _linked_building_counts(buildings)

    address_groups = {
        parcel_key: group for parcel_key, group in address_frame.groupby("parcel_key")
    }
    records = []
    edge_geometries = []
    point_geometries = []
    method_counts = defaultdict(int)

    for parcel_number, parcel in enumerate(parcel_frame.itertuples(), start=1):
        if parcel_number % 25_000 == 0:
            logger.info("Constructed routing-anchor candidates for %s parcels", parcel_number)
        candidates = []
        parcel_addresses = address_groups.get(parcel.parcel_key)
        if parcel_addresses is not None:
            for street_key, group in parcel_addresses.groupby("street_key"):
                street_geometry = street_lookup.get(street_key)
                if street_geometry is not None and not street_geometry.is_empty:
                    candidates.append((street_key, street_geometry, group))

        if not candidates:
            nearest = nearest_tree.nearest(parcel.geometry, return_all=False)
            indices = nearest[1] if len(nearest) > 1 else []
            if len(indices):
                nearest_street = street_frame.iloc[int(indices[0])]
                candidates.append((nearest_street.street_key, nearest_street.geometry, None))

        for sequence, (street_key, street_geometry, address_group) in enumerate(
            candidates, start=1
        ):
            frontage = estimate_street_facing_edge(parcel.geometry, street_geometry)
            edge = frontage.pop("geometry")
            if edge is None or edge.is_empty:
                continue
            if address_group is None:
                source = "nearest_base_units_street"
                method = "nearest_street_front_edge_midpoint"
                anchor = edge.interpolate(0.5, normalized=True)
                address_ids = []
                address_source_object_ids = []
                address_evidence = []
            else:
                source = "base_units_address_link"
                anchor, method = _anchor_on_edge(edge, address_group.geometry.tolist())
                address_evidence = _address_evidence(address_group)
                address_ids = sorted({item["address_id"] for item in address_evidence})
                address_source_object_ids = sorted(
                    {item["source_object_id"] for item in address_evidence}
                )
            method_counts[method] += 1
            anchor_id = f"{parcel.parcel_key}-{street_key}-{sequence}"
            records.append(
                {
                    "parcel_id": str(parcel.parcel_id),
                    "parcel_key": parcel.parcel_key,
                    "anchor_id": anchor_id,
                    "street_id": street_key,
                    "routing_anchor_method": method,
                    "frontage_source": source,
                    "frontage_confidence": frontage["frontage_confidence"],
                    "anchor_confidence": _anchor_confidence(
                        frontage["frontage_confidence"], source
                    ),
                    "geometry_frontage_ft": frontage["geometry_frontage"],
                    "edge_to_street_distance_ft": frontage["edge_to_street_distance"],
                    "angle_difference_degrees": frontage["angle_difference"],
                    "address_objectids_json": json.dumps(address_source_object_ids),
                    "address_ids": address_ids,
                    "address_source_object_ids": address_source_object_ids,
                    "address_evidence": address_evidence,
                    "linked_current_building_count": int(building_counts.get(parcel.parcel_key, 0)),
                }
            )
            point_geometries.append(anchor)
            edge_geometries.append(edge)

    anchors = gpd.GeoDataFrame(records, geometry=point_geometries, crs=PROJECTED_CRS)
    edges = gpd.GeoDataFrame(records, geometry=edge_geometries, crs=PROJECTED_CRS)
    if not anchors.empty:
        anchors = anchors.to_crs(OUTPUT_CRS)
        anchors["longitude"] = anchors.geometry.x
        anchors["latitude"] = anchors.geometry.y
        edges = edges.to_crs(OUTPUT_CRS)
    summary = {
        "parcel_count": len(parcel_frame),
        "parcel_count_with_anchor": int(anchors["parcel_key"].nunique()) if len(anchors) else 0,
        "anchor_count": len(anchors),
        "multi_anchor_parcel_count": int((anchors.groupby("parcel_key").size() > 1).sum())
        if len(anchors)
        else 0,
        "method_counts": dict(sorted(method_counts.items())),
        "unanchored_parcel_count": int(len(parcel_frame) - anchors["parcel_key"].nunique())
        if len(anchors)
        else len(parcel_frame),
    }
    return anchors, edges, summary
