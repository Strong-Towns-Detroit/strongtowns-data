"""Canonical assessment tables and auditable land-value allocation."""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import pyogrio

from strongtowns_data.models import BuildMetadata, PipelineBuilder, PipelineContext


ASSESSMENT_COLUMNS: Mapping[str, str] = {
    "ObjectId": "object_id",
    "parcel_id": "parcel_id",
    "address": "address",
    "tax_status": "tax_status",
    "tax_status_description": "tax_status_description",
    "amt_assessed_value_tentative": "assessed_value_tentative",
    "amt_assessed_value": "assessed_value",
    "amt_assessed_value_previous": "assessed_value_previous",
    "amt_taxable_value_tentative": "taxable_value_tentative",
    "amt_taxable_value": "taxable_value",
    "amt_taxable_value_previous": "taxable_value_previous",
    "amt_estimated_true_cash_value": "true_cash_value",
    "amt_land_value": "land_value",
    "pct_pre_claimed": "pre_percent",
    "nez_district": "nez_district",
    "ecf_neighborhood": "ecf_neighborhood",
    "is_improved": "is_improved",
    "related_parcel_id": "related_parcel_id",
    "property_class": "property_class",
    "property_class_description": "property_class_description",
    "use_code": "use_code",
    "use_code_description": "use_code_description",
    "total_square_footage": "parcel_area_sqft",
    "total_acreage": "parcel_area_acres",
    "landmap": "landmap",
    "neighborhood": "neighborhood",
}

INTEGER_COLUMNS = ("object_id",)
NUMBER_COLUMNS = (
    "assessed_value_tentative",
    "assessed_value",
    "assessed_value_previous",
    "taxable_value_tentative",
    "taxable_value",
    "taxable_value_previous",
    "true_cash_value",
    "land_value",
    "pre_percent",
    "is_improved",
    "parcel_area_sqft",
    "parcel_area_acres",
)
STRING_COLUMNS = tuple(
    column
    for column in ASSESSMENT_COLUMNS.values()
    if column not in INTEGER_COLUMNS and column not in NUMBER_COLUMNS
)


def _empty_rejects() -> pa.Table:
    return pa.table({
        "source_row": pa.array([], type=pa.int64()),
        "source_id": pa.array([], type=pa.string()),
        "reason": pa.array([], type=pa.string()),
    })


def canonical_assessment_builder(
    *,
    input_asset: str,
    output_asset: str,
    roll_year: int,
    input_artifact: str = "raw.geojson",
) -> PipelineBuilder:
    """Create a typed assessment table without parcel-level aggregation."""

    def build(context: PipelineContext):
        source = context.inputs[input_asset] / input_artifact
        rows = pyogrio.read_dataframe(source, read_geometry=False)
        missing = set(ASSESSMENT_COLUMNS) - set(rows)
        if missing:
            raise ValueError(f"assessment source is missing fields: {sorted(missing)}")
        rows = rows.loc[:, list(ASSESSMENT_COLUMNS)].rename(columns=ASSESSMENT_COLUMNS)
        rows.insert(0, "source_row", np.arange(len(rows), dtype="int64"))
        rows.insert(1, "assessment_roll_year", np.full(len(rows), roll_year, dtype="int64"))

        reasons = pd.Series(pd.NA, index=rows.index, dtype="string")
        for column in INTEGER_COLUMNS + NUMBER_COLUMNS:
            original = rows[column]
            converted = pd.to_numeric(original, errors="coerce")
            malformed = original.notna() & converted.isna()
            reasons.loc[reasons.isna() & malformed] = f"invalid_{column}"
            rows[column] = converted
        reasons.loc[reasons.isna() & rows["object_id"].isna()] = "null_object_id"
        parcel_id = rows["parcel_id"].astype("string").str.strip()
        reasons.loc[reasons.isna() & (parcel_id.isna() | parcel_id.eq(""))] = (
            "null_parcel_id"
        )
        duplicate = rows["object_id"].duplicated(keep="first")
        reasons.loc[reasons.isna() & duplicate] = "duplicate_object_id"
        for column in NUMBER_COLUMNS:
            invalid = rows[column].notna() & (
                ~np.isfinite(rows[column]) | rows[column].lt(0)
            )
            reasons.loc[reasons.isna() & invalid] = f"invalid_{column}"

        accepted = rows.loc[reasons.isna()].copy()
        accepted["object_id"] = accepted["object_id"].astype("int64")
        accepted["parcel_id"] = parcel_id.loc[accepted.index]
        for column in STRING_COLUMNS:
            accepted[column] = accepted[column].astype("string")
        for column in NUMBER_COLUMNS:
            accepted[column] = accepted[column].astype("float64")
        accepted = accepted.reset_index(drop=True)

        rejected_rows = rows.loc[reasons.notna()]
        if len(rejected_rows):
            rejected = pa.table({
                "source_row": pa.array(rejected_rows["source_row"], type=pa.int64()),
                "source_id": pa.array(
                    rejected_rows["object_id"].astype("Int64").astype("string"),
                    type=pa.string(),
                    from_pandas=True,
                ),
                "reason": pa.array(reasons.loc[reasons.notna()], type=pa.string()),
            })
        else:
            rejected = _empty_rejects()

        target = context.staging[output_asset]
        pq.write_table(pa.Table.from_pandas(accepted, preserve_index=False), target / "accepted.parquet")
        pq.write_table(rejected, target / "rejects.parquet")
        return {
            output_asset: BuildMetadata(
                counts={
                    "input": len(rows),
                    "accepted": len(accepted),
                    "rejected": len(rejected_rows),
                },
                parameters={
                    "assessment_roll_year": roll_year,
                    "record_identity": "ArcGIS ObjectId; parcel_id is not aggregated",
                },
            )
        }

    return build


def allocate_taxable_land(
    taxable_value: np.ndarray,
    land_value: np.ndarray,
    true_cash_value: np.ndarray,
) -> np.ndarray:
    """Allocate taxable value by land's share of true cash value.

    Invalid or incomplete rows remain NaN. The result is bounded by total
    taxable value, which also protects against inconsistent source records.
    """
    taxable = np.asarray(taxable_value, dtype="float64")
    land = np.asarray(land_value, dtype="float64")
    cash = np.asarray(true_cash_value, dtype="float64")
    result = np.full(np.broadcast_shapes(taxable.shape, land.shape, cash.shape), np.nan)
    valid = (
        np.isfinite(taxable)
        & np.isfinite(land)
        & np.isfinite(cash)
        & (taxable >= 0)
        & (land >= 0)
        & (cash > 0)
    )
    result[valid] = np.clip(
        taxable[valid] * land[valid] / cash[valid], 0, taxable[valid]
    )
    return result


def canonical_lvt_2023_builder(
    *, input_asset: str, output_asset: str, input_artifact: str = "raw.csv"
) -> PipelineBuilder:
    """Canonicalize the City-released 2023 residential LVT estimator table."""

    def build(context: PipelineContext):
        source = context.inputs[input_asset] / input_artifact
        source_rows = pd.read_csv(source, dtype={"parcel_num": "string"})
        required = {
            "ObjectId", "parcel_num", "property_class", "a_tv", "land_value",
            "tv_land", "tax_classification",
        }
        missing = required - set(source_rows)
        if missing:
            raise ValueError(f"2023 LVT source is missing fields: {sorted(missing)}")
        rows = source_rows.loc[:, list(sorted(required))].rename(columns={
            "ObjectId": "object_id",
            "parcel_num": "parcel_id",
            "a_tv": "taxable_value",
            "land_value": "assessed_land_value",
            "tv_land": "taxable_land_value",
        })
        rows.insert(0, "source_row", np.arange(len(rows), dtype="int64"))
        reasons = pd.Series(pd.NA, index=rows.index, dtype="string")
        for column in (
            "object_id", "property_class", "taxable_value",
            "assessed_land_value", "taxable_land_value",
        ):
            original = rows[column]
            converted = pd.to_numeric(original, errors="coerce")
            malformed = original.notna() & converted.isna()
            reasons.loc[reasons.isna() & malformed] = f"invalid_{column}"
            rows[column] = converted
        rows["parcel_id"] = rows["parcel_id"].astype("string").str.strip()
        reasons.loc[
            reasons.isna() & (rows["parcel_id"].isna() | rows["parcel_id"].eq(""))
        ] = "null_parcel_id"
        reasons.loc[reasons.isna() & rows["object_id"].isna()] = "null_object_id"
        reasons.loc[
            reasons.isna() & rows["object_id"].duplicated(keep="first")
        ] = "duplicate_object_id"
        for column in ("taxable_value", "assessed_land_value", "taxable_land_value"):
            invalid = rows[column].notna() & (
                ~np.isfinite(rows[column]) | rows[column].lt(0)
            )
            reasons.loc[reasons.isna() & invalid] = f"invalid_{column}"

        accepted = rows.loc[reasons.isna()].copy()
        accepted["object_id"] = accepted["object_id"].astype("int64")
        accepted["property_class"] = accepted["property_class"].astype("Int64")
        accepted["parcel_id"] = accepted["parcel_id"].astype("string")
        accepted["tax_classification"] = accepted["tax_classification"].astype("string")
        for column in ("taxable_value", "assessed_land_value", "taxable_land_value"):
            accepted[column] = accepted[column].astype("float64")
        rejected_rows = rows.loc[reasons.notna()]
        rejected = pa.table({
            "source_row": pa.array(rejected_rows["source_row"], type=pa.int64()),
            "source_id": pa.array(
                rejected_rows["object_id"].astype("Int64").astype("string"),
                type=pa.string(), from_pandas=True,
            ),
            "reason": pa.array(reasons.loc[reasons.notna()], type=pa.string()),
        }) if len(rejected_rows) else _empty_rejects()
        target = context.staging[output_asset]
        pq.write_table(
            pa.Table.from_pandas(accepted, preserve_index=False),
            target / "accepted.parquet",
        )
        pq.write_table(rejected, target / "rejects.parquet")
        return {output_asset: BuildMetadata(
            counts={
                "input": len(rows), "accepted": len(accepted),
                "rejected": len(rejected_rows),
            },
            parameters={
                "year": 2023,
                "scope": "City-released residential LVT estimator",
            },
        )}

    return build
