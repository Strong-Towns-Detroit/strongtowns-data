"""Round-trippable human review for routing-anchor dispositions."""

from __future__ import annotations

import json
from datetime import UTC
from pathlib import Path

import geopandas as gpd
import pandas as pd

from krabby_real_estate.data.artifacts import artifact_path
from krabby_real_estate.data.catalog import catalog
from krabby_real_estate.data.geoparquet import table_from_columns, write_table
from krabby_real_estate.data.model import DataAssetRef, ProvenanceGrade
from krabby_real_estate.data.storage import PendingArtifact, SnapshotBuilder

REVIEW_STATUSES = {"approved", "rejected", "required"}


def export_anchor_review(
    repository: Path,
    anchor_ref: DataAssetRef,
    disposition_ref: DataAssetRef,
    output: Path,
) -> Path:
    anchors = gpd.read_parquet(artifact_path(repository, anchor_ref))
    dispositions = pd.read_parquet(artifact_path(repository, disposition_ref))
    frame = anchors[
        ["anchor_uuid", "parcel_id", "street_id", "longitude", "latitude", "geometry"]
    ].merge(dispositions, on="anchor_uuid", validate="one_to_one")
    frame["review_reasons"] = frame["review_reasons"].map(lambda values: json.dumps(list(values)))
    frame = frame.rename(columns={"review_status": "original_review_status"})
    frame["proposed_review_status"] = ""
    frame["reviewer"] = ""
    frame["reviewed_at"] = ""
    frame["evidence_uri"] = ""
    frame["notes"] = ""
    frame["anchor_manifest_sha256"] = anchor_ref.manifest_sha256
    frame["disposition_manifest_sha256"] = disposition_ref.manifest_sha256
    frame["anchor_snapshot_id"] = anchor_ref.snapshot_id
    frame["disposition_snapshot_id"] = disposition_ref.snapshot_id
    result = gpd.GeoDataFrame(frame, geometry="geometry", crs=anchors.crs)
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.suffix.lower() == ".csv":
        result.drop(columns="geometry").to_csv(output, index=False)
    elif output.suffix.lower() == ".gpkg":
        result.to_file(output, layer="anchor_review", driver="GPKG")
    else:
        raise ValueError("review export must use .csv or .gpkg")
    return output


def _read_review(path: Path) -> pd.DataFrame:
    if path.suffix.lower() == ".csv":
        return pd.read_csv(path, dtype=str, keep_default_na=False)
    if path.suffix.lower() == ".gpkg":
        return gpd.read_file(path, layer="anchor_review").drop(columns="geometry")
    raise ValueError("review import must use .csv or .gpkg")


def _optional(value):
    if value is None or pd.isna(value):
        return None
    return value


def validate_review_frame(
    frame: pd.DataFrame,
    anchor_ref: DataAssetRef,
    disposition_ref: DataAssetRef,
    valid_anchor_uuids: set[str],
) -> pd.DataFrame:
    required = {
        "anchor_uuid",
        "proposed_review_status",
        "reviewer",
        "reviewed_at",
        "anchor_manifest_sha256",
        "disposition_manifest_sha256",
    }
    missing = sorted(required - set(frame.columns))
    if missing:
        raise ValueError(f"review file missing columns: {missing}")
    if frame["anchor_uuid"].duplicated().any():
        raise ValueError("review file contains duplicate anchor UUIDs")
    if set(frame["anchor_manifest_sha256"]) != {anchor_ref.manifest_sha256}:
        raise ValueError("stale or mixed anchor parent manifest")
    if set(frame["disposition_manifest_sha256"]) != {disposition_ref.manifest_sha256}:
        raise ValueError("stale or mixed disposition parent manifest")
    unknown = set(frame["anchor_uuid"]) - valid_anchor_uuids
    if unknown:
        raise ValueError(f"review file contains unknown anchor UUIDs: {sorted(unknown)[:5]}")
    selected = frame[frame["proposed_review_status"].astype(str).str.strip().ne("")].copy()
    invalid = set(selected["proposed_review_status"]) - REVIEW_STATUSES
    if invalid:
        raise ValueError(f"invalid proposed review statuses: {sorted(invalid)}")
    final = selected["proposed_review_status"].isin({"approved", "rejected"})
    if selected.loc[final, "reviewer"].astype(str).str.strip().eq("").any():
        raise ValueError("approved and rejected reviews require reviewer")
    timestamps = pd.to_datetime(selected.loc[final, "reviewed_at"], utc=True, errors="coerce")
    if timestamps.isna().any():
        raise ValueError("approved and rejected reviews require valid reviewed_at timestamps")
    return selected


def import_anchor_review(
    repository: Path,
    anchor_ref: DataAssetRef,
    disposition_ref: DataAssetRef,
    review_path: Path,
) -> DataAssetRef:
    anchors = gpd.read_parquet(artifact_path(repository, anchor_ref))
    dispositions = pd.read_parquet(artifact_path(repository, disposition_ref))
    frame = _read_review(Path(review_path))
    selected = validate_review_frame(
        frame, anchor_ref, disposition_ref, set(anchors["anchor_uuid"])
    )
    updates = selected.set_index("anchor_uuid")
    output = dispositions.copy().set_index("anchor_uuid")
    for anchor_id, row in updates.iterrows():
        output.loc[anchor_id, "review_status"] = row["proposed_review_status"]
        output.loc[anchor_id, "reviewer"] = row.get("reviewer") or None
        reviewed_at = row.get("reviewed_at") or None
        output.loc[anchor_id, "reviewed_at"] = (
            pd.Timestamp(reviewed_at).tz_convert(UTC) if reviewed_at else None
        )
        output.loc[anchor_id, "evidence_uri"] = row.get("evidence_uri") or None
        output.loc[anchor_id, "notes"] = row.get("notes") or None
    output = output.reset_index()
    asset = catalog.assets["detroit.anchor-dispositions"]
    builder = SnapshotBuilder(repository, asset)
    path = builder.path("accepted.parquet")
    columns = {}
    for field in asset.contract.arrow_schema:
        values = output[field.name].tolist()
        if field.name == "review_reasons":
            values = [list(value) for value in values]
        elif field.nullable:
            values = [_optional(value) for value in values]
        columns[field.name] = values
    table = table_from_columns(columns, asset.contract.arrow_schema)
    output_schema_hash = write_table(table, path, asset.contract)
    return builder.finalize(
        artifacts=[
            PendingArtifact(
                "accepted",
                path,
                asset.media_type,
                record_count=len(output),
                schema_hash=output_schema_hash,
            )
        ],
        provenance_grade=ProvenanceGrade.NATIVE,
        parents=[anchor_ref, disposition_ref],
        counts={"input": len(output), "accepted": len(output), "rejected": 0},
        parameters={
            "review_contract_version": "1.0.0",
            "reviewed_record_count": len(selected),
            "review_source_name": Path(review_path).name,
        },
    )
