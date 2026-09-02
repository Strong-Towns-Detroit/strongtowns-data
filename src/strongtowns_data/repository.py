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
from strongtowns_data.pipelines.snapshots import SnapshotStore, sha256


@dataclass(frozen=True)
class DataLock:
    assets: tuple[DataAssetRef, ...]

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
                written.append(target)
                continue
            staging = target.parent / f".staging-{uuid4()}"
            staging.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(source, staging)
            if sha256(staging / "manifest.json") != reference.manifest_sha256:
                shutil.rmtree(staging)
                raise ValueError(f"copied manifest hash mismatch for {reference.dataset_id}")
            os.replace(staging, target)
            written.append(target)
        return tuple(written)
