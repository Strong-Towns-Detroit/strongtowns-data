"""Strict parcel-routing vertical-slice outputs and eligibility dispositions."""

from __future__ import annotations

import uuid
from pathlib import Path

import geopandas as gpd
import pyarrow as pa

from krabby_real_estate.base_units.anchors import build_parcel_routing_anchors
from krabby_real_estate.data.artifacts import artifact_path
from krabby_real_estate.data.catalog import catalog
from krabby_real_estate.data.geoparquet import table_from_columns, write_geoparquet, write_table
from krabby_real_estate.data.model import DataAssetRef, ProvenanceGrade
from krabby_real_estate.data.storage import PendingArtifact, SnapshotBuilder

ANCHOR_NAMESPACE = uuid.UUID("48c45608-59fe-56d6-8e93-34c3660d2f47")


def anchor_uuid(row) -> str:
    """Stable identity independent of source row order and unrelated additions."""
    address_ids = sorted(map(str, row.address_ids))
    identity = "\x1f".join(
        (
            "routing-anchor-v1",
            str(row.parcel_key),
            str(row.street_id),
            str(row.routing_anchor_method),
            ",".join(address_ids),
        )
    )
    return str(uuid.uuid5(ANCHOR_NAMESPACE, identity))


def review_disposition(row) -> tuple[str, list[str]]:
    reasons = []
    if row.frontage_source == "nearest_base_units_street":
        reasons.append("fallback_anchor")
    if row.anchor_confidence in {"low", "not_evaluated"}:
        reasons.append(f"anchor_confidence_{row.anchor_confidence}")
    if row.edge_to_street_distance_ft > 80:
        reasons.append("street_distance_over_80ft")
    return ("required" if reasons else "not_required", reasons)


def _write_snapshot(
    repository: Path,
    asset_id: str,
    parents: list[DataAssetRef],
    *,
    table: pa.Table | None = None,
    columns: dict | None = None,
    geometries: dict | None = None,
    record_count: int,
) -> DataAssetRef:
    asset = catalog.assets[asset_id]
    builder = SnapshotBuilder(repository, asset)
    path = builder.path("accepted.parquet")
    if geometries is not None:
        output_schema_hash = write_geoparquet(
            columns or {}, path, asset.contract, geometry_columns=geometries
        )
    else:
        if table is None:
            table = table_from_columns(columns or {}, asset.contract.arrow_schema)
        output_schema_hash = write_table(table, path, asset.contract)
    geometry_types = tuple(
        sorted({item for _, types in (geometries or {}).values() for item in types})
    )
    return builder.finalize(
        artifacts=[
            PendingArtifact(
                "accepted",
                path,
                asset.media_type,
                record_count=record_count,
                schema_hash=output_schema_hash,
                crs=asset.contract.crs,
                geometry_types=geometry_types,
            )
        ],
        provenance_grade=ProvenanceGrade.NATIVE,
        parents=parents,
        counts={"input": record_count, "accepted": record_count, "rejected": 0},
        parameters={"routing_contract_version": "1.0.0"},
        crs=asset.contract.crs,
        geometry_types=geometry_types,
    )


def derive_parcel_routing(
    repository: Path, inputs: dict[str, DataAssetRef]
) -> dict[str, DataAssetRef]:
    parcels = gpd.read_parquet(artifact_path(repository, inputs["detroit.parcels"]))
    addresses = gpd.read_parquet(artifact_path(repository, inputs["detroit.base-units.addresses"]))
    streets = gpd.read_parquet(artifact_path(repository, inputs["detroit.base-units.streets"]))
    buildings = gpd.read_parquet(artifact_path(repository, inputs["detroit.base-units.buildings"]))
    anchors, frontages, _summary = build_parcel_routing_anchors(
        parcels, addresses, streets, buildings=buildings
    )
    if anchors.empty:
        raise ValueError("parcel routing produced no anchors")
    anchors = anchors.copy()
    anchors["anchor_uuid"] = [anchor_uuid(row) for row in anchors.itertuples()]
    if anchors["anchor_uuid"].duplicated().any():
        raise ValueError("stable anchor identity is not unique")
    frontages = frontages.copy()
    frontages["anchor_uuid"] = anchors["anchor_uuid"].values

    projected_parcels = parcels[["parcel_key", "geometry"]].to_crs("EPSG:2898")
    parcel_lookup = projected_parcels.set_index("parcel_key").geometry
    projected_anchors = anchors.to_crs("EPSG:2898")
    boundary_distances = [
        point.distance(parcel_lookup[key].boundary)
        for point, key in zip(projected_anchors.geometry, anchors["parcel_key"], strict=True)
    ]
    if max(boundary_distances, default=0.0) > 0.01:
        raise ValueError("routing anchor exceeds the 0.01 survey-foot boundary tolerance")

    anchor_records = {
        field: anchors[field].tolist()
        for field in catalog.assets["detroit.parcel-routing-anchors"].contract.arrow_schema.names
        if field != "geometry"
    }
    parents = list(inputs.values())
    result = {
        "detroit.parcel-routing-anchors": _write_snapshot(
            repository,
            "detroit.parcel-routing-anchors",
            parents,
            columns=anchor_records,
            geometries={"geometry": (anchors.geometry.tolist(), ("Point",))},
            record_count=len(anchors),
        )
    }

    evidence_records = []
    for row in anchors.itertuples():
        for evidence in row.address_evidence:
            evidence_records.append(
                {
                    "anchor_uuid": row.anchor_uuid,
                    "address_id": str(evidence["address_id"]),
                    "source_object_id": str(evidence["source_object_id"]),
                }
            )
    evidence_anchor_ids = {record["anchor_uuid"] for record in evidence_records}
    linked_anchor_ids = set(
        anchors.loc[anchors["frontage_source"].eq("base_units_address_link"), "anchor_uuid"]
    )
    fallback_anchor_ids = set(anchors["anchor_uuid"]) - linked_anchor_ids
    if linked_anchor_ids - evidence_anchor_ids:
        raise ValueError("linked routing anchors are missing address evidence")
    if fallback_anchor_ids & evidence_anchor_ids:
        raise ValueError("fallback routing anchors cannot claim linked-address evidence")
    known_address_ids = set(addresses["address_id"].dropna().astype(str))
    orphan_address_ids = {record["address_id"] for record in evidence_records} - known_address_ids
    if orphan_address_ids:
        raise ValueError("anchor evidence contains unknown address IDs")
    evidence_schema = catalog.assets["detroit.anchor-address-evidence"].contract.arrow_schema
    evidence_columns = {
        field.name: [record[field.name] for record in evidence_records] for field in evidence_schema
    }
    result["detroit.anchor-address-evidence"] = _write_snapshot(
        repository,
        "detroit.anchor-address-evidence",
        parents,
        columns=evidence_columns,
        record_count=len(evidence_records),
    )
    result["detroit.anchor-frontages"] = _write_snapshot(
        repository,
        "detroit.anchor-frontages",
        parents,
        columns={"anchor_uuid": anchors["anchor_uuid"].tolist()},
        geometries={"geometry": (frontages.geometry.tolist(), ("LineString", "MultiLineString"))},
        record_count=len(frontages),
    )

    disposition_records = []
    for row in anchors.itertuples():
        status, reasons = review_disposition(row)
        disposition_records.append(
            {
                "anchor_uuid": row.anchor_uuid,
                "review_status": status,
                "review_reasons": reasons,
                "reviewer": None,
                "reviewed_at": None,
                "evidence_uri": None,
                "notes": None,
            }
        )
    disposition_schema = catalog.assets["detroit.anchor-dispositions"].contract.arrow_schema
    result["detroit.anchor-dispositions"] = _write_snapshot(
        repository,
        "detroit.anchor-dispositions",
        parents,
        columns={
            field.name: [record[field.name] for record in disposition_records]
            for field in disposition_schema
        },
        record_count=len(disposition_records),
    )

    anchored_keys = set(anchors["parcel_key"])
    blocked = [
        {"parcel_id": str(row.parcel_id), "parcel_key": row.parcel_key, "reason": "no_anchor"}
        for row in parcels.itertuples()
        if row.parcel_key not in anchored_keys
    ]
    blocked_schema = catalog.assets["detroit.blocked-routing-parcels"].contract.arrow_schema
    result["detroit.blocked-routing-parcels"] = _write_snapshot(
        repository,
        "detroit.blocked-routing-parcels",
        parents,
        columns={
            field.name: [record[field.name] for record in blocked] for field in blocked_schema
        },
        record_count=len(blocked),
    )
    return result
