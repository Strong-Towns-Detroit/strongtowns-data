#!/usr/bin/env python3
"""Recover unmatched BZA sites through Detroit's Base Units address layer."""

from __future__ import annotations

import re

import geopandas as gpd
import pandas as pd

from .bza_site_matching import clean_street


def parcel_key(value: object) -> str | None:
    if value is None or pd.isna(value):
        return None
    result = re.sub(r"[^0-9A-Za-z]", "", str(value)).upper()
    return result or None


def build_recoveries(
    candidates: pd.DataFrame,
    matched_parcels: pd.DataFrame,
    base_units: pd.DataFrame,
    parcels: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    matched_histories = set(matched_parcels["case_history_id"])
    targets = candidates[~candidates["case_history_id"].isin(matched_histories)].copy()
    base_units = base_units.copy()
    base_units["number"] = pd.to_numeric(base_units["street_number"], errors="coerce")
    base_units = base_units[base_units["number"].notna()].copy()
    base_units["number"] = base_units["number"].astype(int)
    base_units["street"] = (
        base_units["street_prefix"].fillna("").astype(str)
        + " "
        + base_units["street_name"].fillna("").astype(str)
    ).map(clean_street)
    base_units["street_nodir"] = base_units["street"].str.replace(
        r"^(?:N|S|E|W)\s+", "", regex=True
    )
    targets["street_nodir"] = targets["street"].str.replace(
        r"^(?:N|S|E|W)\s+", "", regex=True
    )
    base_columns = ["number", "street", "street_nodir", "parcel_id"]
    if "geometry" in base_units.columns:
        base_columns.append("geometry")
    base_address_rows = base_units[base_columns].rename(
        columns={"parcel_id": "parcel_id_base"}
    )
    exact = targets.merge(
        base_address_rows[
            ["number", "street", "parcel_id_base"]
            + (["geometry"] if "geometry" in base_address_rows else [])
        ],
        on=["number", "street"],
        how="left",
    )
    exact = exact[exact["parcel_id_base"].notna()].copy()

    missing = targets[~targets["site_key"].isin(exact["site_key"])]
    # Directionless matching is permitted only when Base Units resolves the
    # number/street pair to one directional street spelling.
    unique_direction = base_units.groupby(["number", "street_nodir"]).filter(
        lambda group: group["street"].nunique() == 1
    )
    fallback = missing.merge(
        unique_direction[
            ["number", "street_nodir", "parcel_id"]
            + (["geometry"] if "geometry" in unique_direction else [])
        ].rename(columns={"parcel_id": "parcel_id_base"}),
        on=["number", "street_nodir"],
        how="left",
    )
    fallback = fallback[fallback["parcel_id_base"].notna()].copy()
    recovered = pd.concat([exact, fallback], ignore_index=True)
    recovered["parcel_key"] = recovered["parcel_id_base"].map(parcel_key)

    parcel_lookup = parcels.copy()
    parcel_lookup["parcel_key"] = parcel_lookup["parcel_id"].map(parcel_key)
    parcel_lookup = parcel_lookup.dropna(subset=["parcel_key"]).drop_duplicates(
        ["parcel_key", "parcel_id"]
    )
    recovered = recovered.merge(
        parcel_lookup[["parcel_key", "parcel_id"]].rename(
            columns={"parcel_id": "current_parcel_id"}
        ),
        on="parcel_key",
        how="left",
    )
    recovered["recovery_method"] = "base_units_parcel_id"

    missing_current = recovered[
        recovered["current_parcel_id"].isna()
        & recovered.get(
            "geometry", pd.Series(index=recovered.index, dtype=object)
        ).notna()
    ].copy()
    spatial_rows = pd.DataFrame()
    if (
        not missing_current.empty
        and isinstance(base_units, gpd.GeoDataFrame)
        and isinstance(parcels, gpd.GeoDataFrame)
        and parcels.crs is not None
    ):
        points = gpd.GeoDataFrame(
            missing_current.drop(columns=["current_parcel_id"]),
            geometry="geometry",
            crs=base_units.crs,
        ).to_crs(parcels.crs)
        spatial_rows = gpd.sjoin(
            points,
            parcels[["parcel_id", "geometry"]].rename(
                columns={"parcel_id": "current_parcel_id"}
            ),
            how="inner",
            predicate="within",
        ).drop(columns=["index_right"])
        spatial_rows["recovery_method"] = (
            "base_units_address_point_within_current_parcel"
        )
    direct_rows = recovered[recovered["current_parcel_id"].notna()].drop(
        columns=["geometry"], errors="ignore"
    )
    spatial_rows = spatial_rows.drop(columns=["geometry"], errors="ignore")
    recovered = pd.concat(
        [direct_rows, spatial_rows],
        ignore_index=True,
    )
    recovered = recovered.drop_duplicates(
        ["case_history_id", "site_key", "current_parcel_id"]
    )
    overrides = recovered[["site_key", "current_parcel_id"]].drop_duplicates()
    overrides = overrides.rename(columns={"current_parcel_id": "parcel_id"})
    overrides["action"] = "assign"
    overrides["note"] = "Recovered through Detroit Base Units address-to-parcel link"
    overrides["evidence"] = "exact normalized Base Units address or address point"
    return overrides, recovered
