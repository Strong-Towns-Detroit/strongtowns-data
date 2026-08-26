"""Falsifiable migration gates for the 2026-08-26 routing-anchor baseline."""

from __future__ import annotations

from pathlib import Path

import geopandas as gpd
import pandas as pd

ANCHOR_BASELINE = {
    "anchor_count": 380_120,
    "multi_anchor_parcel_count": 1_795,
    "fallback_count": 1_279,
    "address_linked_count": 378_841,
    "not_required_count": 370_787,
    "required_count": 9_333,
}


def validate_anchor_migration(
    current: gpd.GeoDataFrame,
    dispositions: pd.DataFrame,
    legacy_path: Path,
    *,
    tolerance_us_survey_feet: float = 0.01,
) -> dict:
    legacy = gpd.read_file(legacy_path, layer="anchors")
    counts = {
        "anchor_count": len(current),
        "multi_anchor_parcel_count": int((current.groupby("parcel_key").size() > 1).sum()),
        "fallback_count": int(current["frontage_source"].eq("nearest_base_units_street").sum()),
        "address_linked_count": int(current["frontage_source"].eq("base_units_address_link").sum()),
        "not_required_count": int(dispositions["review_status"].eq("not_required").sum()),
        "required_count": int(dispositions["review_status"].eq("required").sum()),
    }
    mismatches = {
        name: {"expected": expected, "actual": counts[name]}
        for name, expected in ANCHOR_BASELINE.items()
        if counts[name] != expected
    }
    keys = ["parcel_key", "street_id", "routing_anchor_method"]
    legacy = legacy.copy()
    current = current.copy()
    legacy["street_id"] = legacy["street_id"].astype(str)
    current["street_id"] = current["street_id"].astype(str)
    if legacy.duplicated(keys).any() or current.duplicated(keys).any():
        raise ValueError("migration natural keys are not unique")
    joined = legacy[keys + ["geometry"]].merge(
        current[keys + ["geometry"]],
        on=keys,
        suffixes=("_legacy", "_current"),
        validate="one_to_one",
    )
    legacy_geometry = gpd.GeoSeries(joined["geometry_legacy"], crs=legacy.crs).to_crs("EPSG:2898")
    current_geometry = gpd.GeoSeries(joined["geometry_current"], crs=current.crs).to_crs(
        "EPSG:2898"
    )
    distances = legacy_geometry.distance(current_geometry)
    report = {
        "counts": counts,
        "count_mismatches": mismatches,
        "legacy_anchor_count": len(legacy),
        "matched_natural_keys": len(joined),
        "maximum_distance_us_survey_feet": float(distances.max()) if len(distances) else None,
        "over_tolerance_count": int((distances > tolerance_us_survey_feet).sum()),
        "tolerance_us_survey_feet": tolerance_us_survey_feet,
    }
    if (
        mismatches
        or len(joined) != len(legacy)
        or len(joined) != len(current)
        or report["over_tolerance_count"]
    ):
        raise ValueError(f"anchor migration gates failed: {report}")
    return report
