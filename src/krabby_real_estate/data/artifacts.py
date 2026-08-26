"""Helpers for resolving immutable artifacts from snapshot manifests."""

from __future__ import annotations

from pathlib import Path

from krabby_real_estate.data.manifest import read_manifest
from krabby_real_estate.data.model import DataAssetRef


def artifact_path(repository: Path, reference: DataAssetRef, role: str = "accepted") -> Path:
    """Resolve exactly one artifact by role, without accepting an ad hoc path."""
    manifest = read_manifest(reference.manifest_path)
    matches = [artifact for artifact in manifest["artifacts"] if artifact["role"] == role]
    if len(matches) != 1:
        raise ValueError(
            f"snapshot {reference.asset_id}/{reference.snapshot_id} has "
            f"{len(matches)} artifacts with role {role!r}"
        )
    path = (Path(repository).resolve() / matches[0]["path"]).resolve()
    if not path.is_relative_to(Path(repository).resolve()):
        raise ValueError("artifact path escapes repository")
    return path
