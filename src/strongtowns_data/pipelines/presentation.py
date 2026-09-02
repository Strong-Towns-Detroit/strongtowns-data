"""Validated presentation datasets preserved from the pre-split repository."""

from __future__ import annotations

import json
import re
import shutil

import geopandas as gpd
import pandas as pd

from strongtowns_data.models import BuildMetadata, PipelineContext, ProvenanceGrade


def preserve_spirit_plaza(
    context: PipelineContext, *, input_asset: str, output_asset: str
) -> dict[str, BuildMetadata]:
    source = context.inputs[input_asset]
    destination = context.staging[output_asset]
    for name in ("display_isochrones.geojson", "road_context.geojson"):
        shutil.copy2(source / name, destination / name)
    return {
        output_asset: BuildMetadata(
            counts={"files": 2},
            parameters={"migration": "preserve-then-replace-v1"},
            provenance_grade=ProvenanceGrade.LEGACY,
        )
    }


def preserve_parking_audit(
    context: PipelineContext, *, input_asset: str, output_asset: str
) -> dict[str, BuildMetadata]:
    source = context.inputs[input_asset] / "parking-case-audit.csv"
    shutil.copy2(source, context.staging[output_asset] / source.name)
    return {
        output_asset: BuildMetadata(
            counts={"records": 62},
            parameters={"migration": "preserve-then-replace-v1"},
            provenance_grade=ProvenanceGrade.LEGACY,
        )
    }


def _normalize_parcel_id(value: object) -> str | None:
    if value is None or pd.isna(value):
        return None
    cleaned = re.sub(r"[^0-9A-Za-z]", "", str(value)).upper()
    return cleaned or None


def _building_type_crosswalk(root) -> dict[str, str | None]:
    path = root / "pipelines/parcel-data/parcel_use_codes_to_zoning_use_codes_manual_mapping.json"
    mapping = json.loads(path.read_text(encoding="utf-8"))
    zoning_types = {
        "Single-family detached dwelling": "single_family",
        "Two-family dwelling": "two_family",
        "Townhouse": "townhouse",
        "Multiple-family dwelling": "multiple_family",
    }
    result: dict[str, str | None] = {}
    for assessor_use, groups in mapping.items():
        candidates = {
            zoning_types[specific_use]
            for group in groups
            for specific_use in group.get("specific_use", [])
            if specific_use in zoning_types
        }
        result[assessor_use.strip().upper()] = (
            next(iter(candidates)) if len(candidates) == 1 else None
        )
    return result


def build_residential_setback_classification(
    context: PipelineContext,
    *,
    parcels_asset: str,
    results_asset: str,
    output_asset: str,
) -> dict[str, BuildMetadata]:
    parcels = gpd.read_parquet(
        context.inputs[parcels_asset] / "accepted.parquet",
        columns=[
            "source_row", "parcel_id", "zoning_district", "use_code_description",
            "geometry",
        ],
    )
    parcels["parcel_key"] = parcels["parcel_id"].map(_normalize_parcel_id)
    crosswalk = _building_type_crosswalk(context.root)

    def classify(row) -> str | None:
        district = str(row.zoning_district or "").strip().upper()
        if district not in {f"R{number}" for number in range(1, 7)}:
            return None
        kind = crosswalk.get(str(row.use_code_description or "").strip().upper())
        return None if district == "R1" and kind == "two_family" else kind

    parcels["building_type"] = [classify(row) for row in parcels.itertuples()]
    parcels["in_scope"] = parcels["building_type"].isin(
        ["single_family", "two_family"]
    )
    source = context.inputs[results_asset]
    audit = pd.read_csv(
        source / "principal_building_site_audit.csv", dtype={"parcel_key": "string"}
    )
    ambiguous = set(
        audit.loc[audit["principal_site_ambiguous"], "parcel_key"].dropna()
    )
    parcels["candidate_multi_parcel_site"] = parcels["parcel_key"].isin(ambiguous)
    results = pd.concat(
        [
            pd.read_csv(source / name, dtype={"parcel_key": "string"})
            for name in (
                "single-family-setback-results.csv",
                "two-family-setback-results.csv",
            )
        ],
        ignore_index=True,
    ).drop_duplicates("parcel_key", keep="last")
    frame = parcels.merge(results, on="parcel_key", how="left", validate="one_to_one")
    frame["evaluated"] = frame["evaluated"].fillna(False).astype(bool)
    frame["crosses_envelope"] = frame["crosses_envelope"].fillna(False).astype(bool)
    frame.loc[
        frame["in_scope"] & frame["candidate_multi_parcel_site"], "evaluation_reason"
    ] = "possible_multi_parcel_site"
    frame.loc[~frame["in_scope"], "evaluation_reason"] = "other_building_type"
    for column in ("building_type", "evaluation_reason", "frontage_confidence"):
        frame[column] = frame[column].astype("string")
    result = gpd.GeoDataFrame(frame, geometry="geometry", crs=parcels.crs)
    result.to_parquet(
        context.staging[output_asset] / "classification.parquet", index=False
    )
    return {
        output_asset: BuildMetadata(
            counts={
                "accepted": len(result),
                "evaluated": int(result["evaluated"].sum()),
                "crosses_envelope": int(result["crosses_envelope"].sum()),
            },
            parameters={"migration": "preserve-then-replace-v1"},
            provenance_grade=ProvenanceGrade.LEGACY,
        )
    }
