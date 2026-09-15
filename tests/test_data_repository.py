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


@pytest.fixture
def materialization(tmp_path):
    from types import SimpleNamespace

    from strongtowns_data.models import BuildMetadata, DataAsset, DatasetModel
    from strongtowns_data.pipelines.snapshots import SnapshotStore, sha256
    item = DataAsset("example", Path("data/example"), DatasetModel("example", "1.0.0"))
    store = SnapshotStore(tmp_path)
    snapshot_id, staging = store.create_staging(item)
    (staging / "payload.txt").write_text("original")
    store.write_manifest(item, staging, snapshot_id, BuildMetadata(), [], producer={
        "name": "test", "git_commit": "fixture", "dirty": False,
    })
    source = store.promote(item, staging)
    reference = DataAssetRef(item.id, snapshot_id, sha256(source / "manifest.json"))
    repository = DataRepository(SimpleNamespace(root=tmp_path, assets={item.id: item}))
    return repository, DataLock((reference,)), tmp_path / "output"


def test_materialization_validates_repeated_copy(materialization):
    repository, lock, output = materialization
    first = repository.materialize(lock, output)
    assert repository.materialize(lock, output) == first
    assert (first[0] / "payload.txt").read_text() == "original"


@pytest.mark.parametrize("damage", ["corrupt", "missing"])
def test_materialization_rejects_damaged_destination(materialization, damage):
    repository, lock, output = materialization
    target, = repository.materialize(lock, output)
    payload = target / "payload.txt"
    if damage == "corrupt":
        payload.write_text("tampered")  # Same size, different hash.
    else:
        payload.unlink()
    with pytest.raises(ValueError, match="artifact"):
        repository.materialize(lock, output)
    assert payload.read_text() == "tampered" if payload.exists() else damage == "missing"


@pytest.mark.parametrize("failure", ["interrupt", "corrupt"])
def test_materialization_cleans_failed_staging(materialization, monkeypatch, failure):
    import shutil
    repository, lock, output = materialization
    copytree = shutil.copytree

    def damaged_copy(source, destination):
        copytree(source, destination)
        if failure == "interrupt":
            raise OSError("interrupted copy")
        (destination / "payload.txt").write_text("tampered")

    monkeypatch.setattr("strongtowns_data.repository.shutil.copytree", damaged_copy)
    with pytest.raises((OSError, ValueError)):
        repository.materialize(lock, output)
    assert not list(output.rglob(".staging-*"))
    assert not (output / lock.assets[0].dataset_id / lock.assets[0].snapshot_id).exists()
