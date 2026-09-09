"""Read-only resolution and materialization of pinned dataset snapshots."""

from __future__ import annotations

import json
import os
import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from uuid import uuid4

from strongtowns_data.models import ArtifactDescriptor, DataAssetRef
from strongtowns_data.pipelines.engine import DataBuildSystem
from strongtowns_data.pipelines.snapshots import SnapshotStore, manifest_hash, sha256, validate_snapshot


@dataclass(frozen=True)
class DataLock:
    assets: tuple[DataAssetRef, ...]

    def asset(self, dataset_id: str) -> DataAssetRef:
        """Return one pinned dataset reference by its stable ID."""
        matches = [item for item in self.assets if item.dataset_id == dataset_id]
        if not matches:
            raise KeyError(f"dataset is not pinned: {dataset_id}")
        return matches[0]

    def to_dict(self) -> dict:
        return {
            "lock_version": "1.0.0",
            "assets": [
                {
                    "dataset_id": item.dataset_id,
                    "snapshot_id": item.snapshot_id,
                    "manifest_sha256": item.manifest_sha256,
                }
                for item in sorted(self.assets, key=lambda value: value.dataset_id)
            ],
        }

    def write(self, path: Path | str) -> None:
        """Atomically write the lock in its canonical, deterministic form."""
        target = Path(path).resolve()
        target.parent.mkdir(parents=True, exist_ok=True)
        temporary = target.with_name(f".{target.name}.{uuid4()}.tmp")
        temporary.write_text(json.dumps(self.to_dict(), indent=2) + "\n", encoding="utf-8")
        os.replace(temporary, target)

    def update_promoted(
        self,
        system: DataBuildSystem,
        dataset_ids: list[str],
    ) -> DataLock:
        """Return a lock with selected IDs replaced by promoted snapshots."""
        unknown = set(dataset_ids) - set(system.assets)
        if unknown:
            raise ValueError(f"unknown datasets: {sorted(unknown)}")
        updated = {item.dataset_id: item for item in self.assets}
        store = SnapshotStore(system.root)
        for dataset_id in dataset_ids:
            _, manifest = store.promoted(system.assets[dataset_id])
            updated[dataset_id] = DataAssetRef(
                dataset_id=dataset_id,
                snapshot_id=manifest["snapshot_id"],
                manifest_sha256=manifest_hash(manifest),
            )
        return DataLock(tuple(updated[key] for key in sorted(updated)))

    @classmethod
    def load(cls, path: Path | str) -> DataLock:
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
        if payload.get("lock_version") != "1.0.0":
            raise ValueError("unsupported data lock version")
        records = payload.get("assets")
        if not isinstance(records, list):
            raise TypeError("data lock assets must be a list")
        assets = tuple(
            DataAssetRef(
                dataset_id=str(item["dataset_id"]),
                snapshot_id=str(item["snapshot_id"]),
                manifest_sha256=str(item["manifest_sha256"]),
            )
            for item in records
        )
        ids = [item.dataset_id for item in assets]
        if len(ids) != len(set(ids)):
            raise ValueError("data lock contains duplicate dataset IDs")
        for item in assets:
            if not re.fullmatch(r"[0-9a-f]{64}", item.manifest_sha256):
                raise ValueError(f"invalid manifest hash for {item.dataset_id}")
        return cls(assets)


@dataclass(frozen=True)
class DataRepository:
    """Resolve registered assets without building or fetching them."""

    system: DataBuildSystem

    def resolve(self, reference: DataAssetRef) -> tuple[Path, dict]:
        asset = self.system.assets.get(reference.dataset_id)
        if asset is None:
            raise ValueError(f"unknown dataset: {reference.dataset_id}")
        directory, manifest = SnapshotStore(self.system.root).snapshot(
            asset, reference.snapshot_id
        )
        manifest_path = directory / "manifest.json"
        if sha256(manifest_path) != reference.manifest_sha256:
            raise ValueError(f"locked manifest hash mismatch for {reference.dataset_id}")
        return directory, manifest

    def artifacts(self, reference: DataAssetRef) -> tuple[ArtifactDescriptor, ...]:
        _, manifest = self.resolve(reference)
        return tuple(
            ArtifactDescriptor(item["path"], item["size"], item["sha256"])
            for item in manifest["artifacts"]
        )

    def artifact(self, reference: DataAssetRef, path: str) -> Path:
        """Resolve one declared artifact from a validated pinned snapshot."""
        directory, manifest = self.resolve(reference)
        records = {item["path"]: item for item in manifest["artifacts"]}
        if path not in records:
            raise ValueError(
                f"artifact is not declared by {reference.dataset_id}: {path}"
            )
        resolved = (directory / path).resolve()
        resolved.relative_to(directory.resolve())
        return resolved

    def materialize(self, lock: DataLock, destination: Path | str) -> tuple[Path, ...]:
        root = Path(destination).resolve()
        root.mkdir(parents=True, exist_ok=True)
        written: list[Path] = []
        for reference in lock.assets:
            source, _ = self.resolve(reference)
            target = root / reference.dataset_id / reference.snapshot_id
            if target.exists():
                if sha256(target / "manifest.json") != reference.manifest_sha256:
                    raise ValueError(f"existing materialization differs: {target}")
                validate_snapshot(self.system.assets[reference.dataset_id], target)
                written.append(target)
                continue
            staging = target.parent / f".staging-{uuid4()}"
            staging.parent.mkdir(parents=True, exist_ok=True)
            try:
                shutil.copytree(source, staging)
                if sha256(staging / "manifest.json") != reference.manifest_sha256:
                    raise ValueError(f"copied manifest hash mismatch for {reference.dataset_id}")
                validate_snapshot(self.system.assets[reference.dataset_id], staging)
                os.replace(staging, target)
            finally:
                if staging.exists():
                    shutil.rmtree(staging)
            written.append(target)
        return tuple(written)
