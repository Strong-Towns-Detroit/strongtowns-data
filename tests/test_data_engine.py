import json
from pathlib import Path

import pyarrow as pa
import pytest

from krabby_real_estate.data.catalog import catalog
from krabby_real_estate.data.hashing import schema_hash, sha256_file
from krabby_real_estate.data.manifest import manifest_ref, resolve_promoted
from krabby_real_estate.data.model import (
    DataAsset,
    DatasetContract,
    PipelineDefinition,
    ProvenanceGrade,
    Tier,
)
from krabby_real_estate.data.registry import AssetRegistry
from krabby_real_estate.data.storage import PendingArtifact, SnapshotBuilder, validate_snapshot
from krabby_real_estate.data.table_validation import validate_foreign_key, validate_table


def asset(tmp_path):
    return DataAsset(
        "test.records",
        Tier.DERIVED,
        "application/json",
        DatasetContract("test-records-v1", "1.0.0"),
        Path("data/derived/test.records"),
    )


def test_catalog_is_valid_and_acyclic():
    catalog.validate()
    ordered = catalog.topological_pipelines()
    assert ordered.index("canonicalize.parcels") < ordered.index("derive.parcel-routing")
    assert ordered.index("derive.parcel-routing") < ordered.index("prepare.traveltime-requests")


def test_registry_rejects_duplicate_producer_and_cycle():
    registry = AssetRegistry()
    contract = DatasetContract("test-v1", "1.0.0")
    for name, producer in (("test.a", "test.one"), ("test.b", "test.two")):
        registry.register_asset(
            DataAsset(name, Tier.DERIVED, "application/json", contract, Path(name), producer)
        )
    registry.register_pipeline(PipelineDefinition("test.one", ("test.b",), ("test.a",)))
    registry.register_pipeline(PipelineDefinition("test.two", ("test.a",), ("test.b",)))
    with pytest.raises(ValueError, match="cycle"):
        registry.validate()


def test_snapshot_counts_are_reconciled_and_hashes_validate(tmp_path, monkeypatch):
    monkeypatch.setattr(
        "krabby_real_estate.data.storage.git_state",
        lambda _root: type("S", (), {"commit": "a" * 40, "clean": True})(),
    )
    builder = SnapshotBuilder(tmp_path, asset(tmp_path))
    output = builder.path("records.json")
    output.write_text('[{"id":"1"}]')
    reference = builder.finalize(
        artifacts=[PendingArtifact("accepted", output, "application/json", 1)],
        provenance_grade=ProvenanceGrade.NATIVE,
        counts={"input": 1, "accepted": 1, "rejected": 0},
    )
    assert not validate_snapshot(tmp_path, reference.manifest_path)
    output_path = next(reference.manifest_path.parent.glob("records.json"))
    output_path.write_text("changed")
    assert any(
        "hash changed" in error for error in validate_snapshot(tmp_path, reference.manifest_path)
    )


def test_snapshot_rejects_accepted_parquet_outside_contract(tmp_path, monkeypatch):
    monkeypatch.setattr(
        "krabby_real_estate.data.storage.git_state",
        lambda _root: type("S", (), {"commit": "a" * 40, "clean": True})(),
    )
    contract = DatasetContract(
        "typed-v1", "1.0.0", pa.schema([pa.field("id", pa.string(), nullable=False)]), ("id",)
    )
    current = DataAsset(
        "test.typed",
        Tier.DERIVED,
        "application/vnd.apache.parquet",
        contract,
        Path("data/derived/test.typed"),
    )
    builder = SnapshotBuilder(tmp_path, current)
    output = builder.path("accepted.parquet")
    import pyarrow.parquet as pq

    wrong = pa.table({"wrong": ["1"]})
    pq.write_table(wrong, output)
    reference = builder.finalize(
        artifacts=[
            PendingArtifact(
                "accepted",
                output,
                "application/vnd.apache.parquet",
                1,
                schema_hash=schema_hash(pq.ParquetFile(output).schema_arrow),
            )
        ],
        provenance_grade=ProvenanceGrade.NATIVE,
        counts={"input": 1, "accepted": 1, "rejected": 0},
    )
    assert any(
        "violates contract schema" in error
        for error in validate_snapshot(tmp_path, reference.manifest_path)
    )


def test_snapshot_rejects_bad_count_accounting(tmp_path):
    builder = SnapshotBuilder(tmp_path, asset(tmp_path))
    output = builder.path("records.json")
    output.write_text("[]")
    with pytest.raises(ValueError, match=r"accepted \+ rejected"):
        builder.finalize(
            artifacts=[PendingArtifact("accepted", output, "application/json", 0)],
            provenance_grade=ProvenanceGrade.NATIVE,
            counts={"input": 2, "accepted": 1, "rejected": 0},
        )


def test_recursive_validation_uses_pinned_parent_path(tmp_path, monkeypatch):
    monkeypatch.setattr(
        "krabby_real_estate.data.storage.git_state",
        lambda _root: type("S", (), {"commit": "a" * 40, "clean": True})(),
    )
    current_asset = asset(tmp_path)
    parent_builder = SnapshotBuilder(tmp_path, current_asset)
    parent_output = parent_builder.path("parent.json")
    parent_output.write_text('[{"id":"parent"}]')
    parent = parent_builder.finalize(
        artifacts=[PendingArtifact("accepted", parent_output, "application/json", 1)],
        provenance_grade=ProvenanceGrade.NATIVE,
        counts={"input": 1, "accepted": 1, "rejected": 0},
    )
    child_builder = SnapshotBuilder(tmp_path, current_asset)
    child_output = child_builder.path("child.json")
    child_output.write_text('[{"id":"child"}]')
    child = child_builder.finalize(
        artifacts=[PendingArtifact("accepted", child_output, "application/json", 1)],
        provenance_grade=ProvenanceGrade.NATIVE,
        parents=[parent],
        counts={"input": 1, "accepted": 1, "rejected": 0},
    )
    assert not validate_snapshot(tmp_path, child.manifest_path)
    document = json.loads(parent.manifest_path.read_text())
    document["parameters"] = {"tampered": True}
    parent.manifest_path.write_text(json.dumps(document))
    assert any(
        "parent manifest hash changed" in error
        for error in validate_snapshot(tmp_path, child.manifest_path)
    )


def test_promotion_pointer_pins_manifest_hash(tmp_path, monkeypatch):
    current_asset = asset(tmp_path)
    monkeypatch.setattr(
        "krabby_real_estate.data.storage.git_state",
        lambda _root: type("S", (), {"commit": "a" * 40, "clean": True})(),
    )
    builder = SnapshotBuilder(tmp_path, current_asset)
    output = builder.path("records.json")
    output.write_text('[{"id":"1"}]')
    reference = builder.finalize(
        artifacts=[PendingArtifact("accepted", output, "application/json", 1)],
        provenance_grade=ProvenanceGrade.NATIVE,
        counts={"input": 1, "accepted": 1, "rejected": 0},
    )
    pointer_dir = tmp_path / current_asset.storage_root
    pointer = {
        "pointer_contract_version": "1.0.0",
        "asset_id": current_asset.asset_id,
        "snapshot_id": reference.snapshot_id,
        "manifest_path": str(reference.manifest_path.relative_to(pointer_dir)),
        "manifest_sha256": sha256_file(reference.manifest_path),
        "promoted_at": "2026-08-26T12:00:00+00:00",
    }
    pointer_path = pointer_dir / "PROMOTED.json"
    pointer_path.write_text(json.dumps(pointer))
    assert resolve_promoted(pointer_path) == manifest_ref(reference.manifest_path)
    pointer["manifest_sha256"] = "0" * 64
    pointer_path.write_text(json.dumps(pointer))
    with pytest.raises(ValueError, match="hash"):
        resolve_promoted(pointer_path)


def test_promotion_pointer_cannot_escape_asset_root(tmp_path):
    pointer_dir = tmp_path / "data/derived/test.records"
    pointer_dir.mkdir(parents=True)
    pointer = {
        "pointer_contract_version": "1.0.0",
        "asset_id": "test.records",
        "snapshot_id": "2bbf8a61-67af-40d2-adfd-1aa61f39d863",
        "manifest_path": "../../outside/manifest.json",
        "manifest_sha256": "0" * 64,
        "promoted_at": "2026-08-26T12:00:00+00:00",
    }
    path = pointer_dir / "PROMOTED.json"
    path.write_text(json.dumps(pointer))
    with pytest.raises(ValueError, match="escapes"):
        resolve_promoted(path)


def test_contract_requires_semver_and_relative_storage():
    with pytest.raises(ValueError, match="MAJOR"):
        DatasetContract("test-v1", "1")
    with pytest.raises(ValueError, match="repository-relative"):
        DataAsset(
            "test.bad",
            Tier.SOURCE,
            "application/json",
            DatasetContract("test-v1", "1.0.0", pa.schema([])),
            Path("/tmp/data"),
        )


def test_table_contract_rejects_duplicate_keys_invalid_enum_and_orphan_fk():
    request_contract = catalog.assets["traveltime.requests"].contract
    row = {
        "request_uuid": ["r", "r"],
        "provider_search_id": ["p1", "p2"],
        "anchor_uuid": ["a", "missing"],
        "parcel_id": ["1", "2"],
        "direction": ["arrival", "sideways"],
        "transportation": ["walking", "walking"],
        "travel_time_seconds": [3600, 3601],
        "reference_time_utc": [None, None],
        "latitude": [42.0, 42.0],
        "longitude": [-83.0, -83.0],
        "selection_override": [False, False],
    }
    table = pa.Table.from_pydict(row, schema=request_contract.arrow_schema)
    result = validate_table(table, request_contract)
    assert {issue.code for issue in result.issues} >= {
        "duplicate_primary_key",
        "invalid_enum",
        "null_not_allowed",
        "out_of_range",
    }
    parent = pa.table({"anchor_uuid": ["a"]})
    fk = validate_foreign_key(table, ("anchor_uuid",), parent, ("anchor_uuid",))
    assert [issue.code for issue in fk.issues] == ["foreign_key_violation"]
