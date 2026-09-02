import json
from pathlib import Path
from typing import ClassVar

import pytest

from strongtowns_data.models import DataAssetRef
from strongtowns_data.pipelines.cli import parser
from strongtowns_data.repository import DataLock, DataRepository


def test_data_lock_rejects_duplicate_assets(tmp_path):
    path = tmp_path / "data.lock.json"
    record = {
        "dataset_id": "detroit.parcels",
        "snapshot_id": "snapshot",
        "manifest_sha256": "a" * 64,
    }
    path.write_text(json.dumps({"lock_version": "1.0.0", "assets": [record, record]}))

    with pytest.raises(ValueError, match="duplicate"):
        DataLock.load(path)


def test_data_lock_rejects_invalid_manifest_hash(tmp_path):
    path = tmp_path / "data.lock.json"
    path.write_text(json.dumps({
        "lock_version": "1.0.0",
        "assets": [{
            "dataset_id": "detroit.parcels",
            "snapshot_id": "snapshot",
            "manifest_sha256": "not-a-hash",
        }],
    }))

    with pytest.raises(ValueError, match="invalid manifest hash"):
        DataLock.load(path)


def test_repository_rejects_unknown_dataset():
    class System:
        assets: ClassVar[dict] = {}
        root = Path(".")

    reference = DataAssetRef("missing", "snapshot", "a" * 64)
    with pytest.raises(ValueError, match="unknown dataset"):
        DataRepository(System()).resolve(reference)


def test_materialize_accepts_explicit_repository():
    args = parser().parse_args([
        "materialize", "--repository", "../data", "--lock", "data.lock.json",
        "--output", ".data",
    ])

    assert args.repository == "../data"


def test_data_lock_finds_assets_and_writes_deterministically(tmp_path):
    lock = DataLock((
        DataAssetRef("z", "snapshot-z", "b" * 64),
        DataAssetRef("a", "snapshot-a", "a" * 64),
    ))
    path = tmp_path / "data.lock.json"
    lock.write(path)

    assert DataLock.load(path).asset("a").snapshot_id == "snapshot-a"
    assert [item["dataset_id"] for item in json.loads(path.read_text())["assets"]] == ["a", "z"]
    with pytest.raises(KeyError, match="not pinned"):
        lock.asset("missing")


def test_repository_resolves_only_declared_artifacts(tmp_path, monkeypatch):
    reference = DataAssetRef("detroit.parcels", "snapshot", "a" * 64)
    artifact = tmp_path / "parcels.gpkg"
    artifact.write_text("data")
    repository = DataRepository(object())
    monkeypatch.setattr(
        DataRepository,
        "resolve",
        lambda self, item: (tmp_path, {"artifacts": [{"path": "parcels.gpkg"}]}),
    )

    assert repository.artifact(reference, "parcels.gpkg") == artifact.resolve()
    with pytest.raises(ValueError, match="not declared"):
        repository.artifact(reference, "other.gpkg")


def test_lock_update_parser_is_dry_run_by_default():
    args = parser().parse_args([
        "lock", "update", "--repository", "../data", "--lock", "data.lock.json",
        "detroit.parcels",
    ])

    assert args.repository == "../data"
    assert args.apply is False
    assert args.asset == ["detroit.parcels"]


def test_legacy_import_parser_accepts_external_source_root():
    args = parser().parse_args([
        "legacy-import", "--source-root", "../consumer", "legacy.asset",
    ])

    assert args.source_root == "../consumer"
    assert args.asset == ["legacy.asset"]


def test_data_lock_updates_only_requested_promoted_assets(monkeypatch, tmp_path):
    manifest = {"snapshot_id": "new-snapshot", "artifacts": []}

    class Store:
        def __init__(self, root):
            pass

        def promoted(self, asset):
            return tmp_path, manifest

    monkeypatch.setattr("strongtowns_data.repository.SnapshotStore", Store)
    system = type(
        "System",
        (),
        {"root": tmp_path, "assets": {"a": object(), "b": object()}},
    )()
    original = DataLock((DataAssetRef("b", "old-b", "b" * 64),))

    updated = original.update_promoted(system, ["a"])

    assert [item.dataset_id for item in updated.assets] == ["a", "b"]
    assert updated.asset("a").snapshot_id == "new-snapshot"
    assert updated.asset("b") == original.asset("b")
    with pytest.raises(ValueError, match="unknown datasets"):
        original.update_promoted(system, ["missing"])
