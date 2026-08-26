"""Executable implementations for the registered Contract-v1 pipeline DAG."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from itertools import islice
from pathlib import Path

import geopandas as gpd
import pandas as pd

from krabby_real_estate.data.artifacts import artifact_path
from krabby_real_estate.data.canonical import CANONICALIZERS
from krabby_real_estate.data.catalog import catalog
from krabby_real_estate.data.geoparquet import table_from_columns, write_geoparquet, write_table
from krabby_real_estate.data.model import DataAssetRef, ProvenanceGrade
from krabby_real_estate.data.routing import derive_parcel_routing
from krabby_real_estate.data.storage import PendingArtifact, SnapshotBuilder
from krabby_real_estate.traveltime.ledger import (
    LedgerSpec,
    post_batch_with_retry,
    prepare_request_records,
    reconcile_response,
)


def _batches(records, size=10):
    iterator = iter(records)
    while batch := list(islice(iterator, size)):
        yield batch


def _parse_reference(parameters: dict) -> datetime:
    value = parameters.get("reference_time_utc")
    if not value:
        raise ValueError(
            "prepare.traveltime-requests requires parameter reference_time_utc="
            "<timezone-aware ISO-8601>"
        )
    result = datetime.fromisoformat(str(value))
    if result.tzinfo is None:
        raise ValueError("reference_time_utc must include a timezone")
    return result.astimezone(UTC)


def prepare_traveltime_requests(
    repository: Path, inputs: dict[str, DataAssetRef], parameters: dict
) -> dict[str, DataAssetRef]:
    anchors = gpd.read_parquet(artifact_path(repository, inputs["detroit.parcel-routing-anchors"]))
    dispositions = pd.read_parquet(artifact_path(repository, inputs["detroit.anchor-dispositions"]))
    reference = _parse_reference(parameters)
    directions = tuple(
        part.strip()
        for part in str(parameters.get("directions", "arrival,departure")).split(",")
        if part.strip()
    )
    mode = str(parameters.get("transportation", "walking"))
    horizon = int(parameters.get("travel_time_seconds", 3600))
    specs = [LedgerSpec(direction, mode, horizon, reference) for direction in directions]
    overrides = {
        item.strip()
        for item in str(parameters.get("override_anchor_uuids", "")).split(",")
        if item.strip()
    }
    selected_anchors = {
        item.strip() for item in str(parameters.get("anchor_uuids", "")).split(",") if item.strip()
    }
    if selected_anchors:
        unknown = selected_anchors - set(anchors["anchor_uuid"])
        if unknown:
            raise ValueError(f"unknown selected anchors: {sorted(unknown)}")
        anchors = anchors[anchors["anchor_uuid"].isin(selected_anchors)].copy()
        dispositions = dispositions[dispositions["anchor_uuid"].isin(selected_anchors)].copy()
    records = prepare_request_records(anchors, dispositions, specs, override_anchor_uuids=overrides)
    if not records:
        raise ValueError("TravelTime selection produced no eligible requests")
    asset = catalog.assets["traveltime.requests"]
    builder = SnapshotBuilder(repository, asset)
    path = builder.path("accepted.parquet")
    table = table_from_columns(
        {
            field.name: [record[field.name] for record in records]
            for field in asset.contract.arrow_schema
        },
        asset.contract.arrow_schema,
    )
    output_schema_hash = write_table(table, path, asset.contract)
    output_reference = builder.finalize(
        artifacts=[
            PendingArtifact(
                "accepted",
                path,
                asset.media_type,
                record_count=len(records),
                schema_hash=output_schema_hash,
            )
        ],
        provenance_grade=ProvenanceGrade.NATIVE,
        parents=list(inputs.values()),
        counts={"input": len(records), "accepted": len(records), "rejected": 0},
        parameters={
            "request_contract_version": "1.0.0",
            "directions": list(directions),
            "transportation": mode,
            "travel_time_seconds": horizon,
            "reference_time_utc": reference.isoformat(),
            "override_anchor_count": len(overrides),
            "selected_anchor_count": len(selected_anchors) or None,
        },
    )
    return {"traveltime.requests": output_reference}


def collect_traveltime_results(
    repository: Path,
    request_ref: DataAssetRef,
    *,
    app_id: str,
    api_key: str,
    session=None,
) -> DataAssetRef:
    """Collect a promoted request ledger; any unresolved/provider error blocks completion."""
    requests = pd.read_parquet(artifact_path(repository, request_ref)).to_dict("records")
    if not requests:
        raise ValueError("request ledger is empty")
    asset = catalog.assets["traveltime.results"]
    builder = SnapshotBuilder(repository, asset)
    raw_artifacts = []
    results = []
    batch_number = 0
    for direction in sorted({record["direction"] for record in requests}):
        directional = [record for record in requests if record["direction"] == direction]
        for batch in _batches(directional):
            batch_number += 1
            kwargs = {"app_id": app_id, "api_key": api_key}
            if session is not None:
                kwargs["session"] = session
            response = post_batch_with_retry(batch, **kwargs)
            raw_path = builder.path(f"raw/response-{batch_number:06d}.json")
            raw_path.write_text(json.dumps(response, sort_keys=True, separators=(",", ":")) + "\n")
            raw_artifacts.append(PendingArtifact("raw_response", raw_path, "application/geo+json"))
            results.extend(reconcile_response(batch, response, datetime.now(UTC)))
    errors = [result for result in results if result["result_status"] != "success"]
    if errors:
        failure = builder.path("failure-report.json")
        failure.write_text(
            json.dumps(
                {
                    "error": "terminal_provider_results",
                    "request_uuids": [item["request_uuid"] for item in errors],
                },
                indent=2,
            )
            + "\n"
        )
        raise ValueError(
            f"TravelTime returned {len(errors)} terminal provider errors; attempt remains staged"
        )
    path = builder.path("accepted.parquet")
    columns = {
        field.name: [record[field.name] for record in results]
        for field in asset.contract.arrow_schema
        if field.name != "geometry"
    }
    output_schema_hash = write_geoparquet(
        columns,
        path,
        asset.contract,
        geometry_columns={
            "geometry": ([item["geometry"] for item in results], ("Polygon", "MultiPolygon"))
        },
    )
    return builder.finalize(
        artifacts=[
            PendingArtifact(
                "accepted",
                path,
                asset.media_type,
                record_count=len(results),
                schema_hash=output_schema_hash,
                crs="EPSG:4326",
                geometry_types=("MultiPolygon", "Polygon"),
            ),
            *raw_artifacts,
        ],
        provenance_grade=ProvenanceGrade.NATIVE,
        parents=[request_ref],
        counts={"input": len(requests), "accepted": len(results), "rejected": 0},
        acquisition_fingerprint={
            "provider": "traveltime",
            "endpoint": "https://api.traveltimeapp.com/v4/time-map",
            "request_manifest_sha256": request_ref.manifest_sha256,
        },
        parameters={"request_contract_version": "1.0.0"},
        crs="EPSG:4326",
        geometry_types=("MultiPolygon", "Polygon"),
    )


def run_offline_pipeline(
    repository: Path,
    pipeline_id: str,
    inputs: dict[str, DataAssetRef],
    parameters: dict | None = None,
) -> dict[str, DataAssetRef]:
    parameters = parameters or {}
    try:
        if pipeline_id in CANONICALIZERS:
            parent = inputs[next(iter(inputs))]
            output = CANONICALIZERS[pipeline_id](repository, parent)
            return {output.asset_id: output}
        if pipeline_id == "derive.parcel-routing":
            return derive_parcel_routing(repository, inputs)
        if pipeline_id == "prepare.traveltime-requests":
            return prepare_traveltime_requests(repository, inputs, parameters)
        if pipeline_id == "collect.traveltime-results":
            raise ValueError("paid acquisition must use `krabby-data fetch traveltime`")
        raise KeyError(pipeline_id)
    except Exception as error:
        pipeline = catalog.pipelines.get(pipeline_id)
        if pipeline is not None:
            for output_asset_id in pipeline.outputs:
                failure = SnapshotBuilder(repository, catalog.assets[output_asset_id])
                failure.record_failure("pipeline_failed", error)
        raise
