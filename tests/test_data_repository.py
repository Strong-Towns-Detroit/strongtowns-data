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
