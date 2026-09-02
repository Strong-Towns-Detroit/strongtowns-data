"""Quality-assurance summaries for parcel routing anchors and Base Units relations."""

from __future__ import annotations

from collections import Counter

import geopandas as gpd
import numpy as np
import pandas as pd

from strongtowns_data.base_units.anchors import normalize_relationship_id
from strongtowns_data.base_units.geometry import normalize_parcel_id


def audit_source_relations(
    parcels: pd.DataFrame, addresses: pd.DataFrame, streets: pd.DataFrame
) -> dict:
    """Count usable and broken address→parcel→street relations without geometry."""
    parcel_keys = set(parcels["parcel_id"].map(normalize_parcel_id).dropna())
    street_keys = set(streets["street_id"].map(normalize_relationship_id).dropna())
    address_parcels = addresses["parcel_id"].map(normalize_parcel_id)
    address_streets = addresses["street_id"].map(normalize_relationship_id)
    parcel_present = address_parcels.isin(parcel_keys)
    street_present = address_streets.isin(street_keys)
    usable = parcel_present & street_present
    usable_parcels = set(address_parcels[usable])
    return {
        "parcel_record_count": len(parcels),
        "parcel_key_count": len(parcel_keys),
        "street_record_count": len(streets),
        "street_key_count": len(street_keys),
        "address_record_count": len(addresses),
        "address_missing_parcel_id_count": int(address_parcels.isna().sum()),
        "address_parcel_not_current_count": int((address_parcels.notna() & ~parcel_present).sum()),
        "address_missing_street_id_count": int(address_streets.isna().sum()),
        "address_street_not_current_count": int((address_streets.notna() & ~street_present).sum()),
        "usable_address_relation_count": int(usable.sum()),
        "parcel_with_usable_address_relation_count": len(usable_parcels),
        "parcel_without_usable_address_relation_count": len(parcel_keys - usable_parcels),
    }


def audit_anchors(anchors: gpd.GeoDataFrame) -> tuple[dict, gpd.GeoDataFrame]:
    """Summarize anchors and return geometries selected for human review."""
    required = {
        "parcel_key",
        "anchor_id",
        "routing_anchor_method",
        "anchor_confidence",
        "edge_to_street_distance_ft",
        "angle_difference_degrees",
        "geometry",
    }
    missing = sorted(required - set(anchors.columns))
    if missing:
        raise ValueError(f"anchors missing required columns: {missing}")

    per_parcel = anchors.groupby("parcel_key").size()
    distances = pd.to_numeric(anchors["edge_to_street_distance_ft"], errors="coerce")
    finite_distances = distances[np.isfinite(distances)]
    reasons = []
    reason_counts: Counter[str] = Counter()
    multi_parcels = set(per_parcel[per_parcel > 1].index)
    for row, distance in zip(anchors.itertuples(), distances):
        row_reasons = []
        if row.routing_anchor_method == "nearest_street_front_edge_midpoint":
            row_reasons.append("nearest_street_fallback")
        if row.anchor_confidence in {"low", "not_evaluated"}:
            row_reasons.append(f"anchor_confidence_{row.anchor_confidence}")
        if pd.notna(distance) and distance > 80:
            row_reasons.append("street_distance_over_80ft")
        if row.parcel_key in multi_parcels:
            row_reasons.append("multiple_street_anchors")
        reasons.append(row_reasons)
        reason_counts.update(row_reasons)

    review = anchors.copy()
    review["qa_reasons"] = [";".join(row_reasons) for row_reasons in reasons]
    review = review[review["qa_reasons"].ne("")].copy()
    quantiles = (
        finite_distances.quantile([0, 0.5, 0.9, 0.95, 0.99, 1]).to_dict()
        if len(finite_distances)
        else {}
    )
    report = {
        "anchor_count": len(anchors),
        "parcel_count": int(anchors["parcel_key"].nunique()),
        "multi_anchor_parcel_count": len(multi_parcels),
        "review_anchor_count": len(review),
        "routing_anchor_method_counts": anchors["routing_anchor_method"].value_counts().to_dict(),
        "anchor_confidence_counts": anchors["anchor_confidence"].value_counts().to_dict(),
        "review_reason_counts": dict(sorted(reason_counts.items())),
        "edge_to_street_distance_ft_quantiles": {
            str(key): float(value) for key, value in quantiles.items()
        },
    }
    if "is_improved" in anchors:
        improved = anchors["is_improved"].fillna("unknown").astype(str)
        fallback_mask = anchors["routing_anchor_method"].eq("nearest_street_front_edge_midpoint")
        report["is_improved_counts"] = improved.value_counts().to_dict()
        report["fallback_is_improved_counts"] = improved[fallback_mask].value_counts().to_dict()
    return report, review
