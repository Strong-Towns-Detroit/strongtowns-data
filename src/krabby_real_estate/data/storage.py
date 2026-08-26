"""Immutable snapshot staging, finalization, validation, and promotion."""

from __future__ import annotations

import json
import os
import shutil
import uuid
from dataclasses import dataclass
from datetime import UTC, datetime
from importlib.metadata import version
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq

from krabby_real_estate.data.git import git_state
from krabby_real_estate.data.hashing import schema_hash, sha256_file
from krabby_real_estate.data.manifest import manifest_ref, read_manifest, validate_json_document
from krabby_real_estate.data.model import (
    ArtifactDescriptor,
    DataAsset,
    DataAssetRef,
    ProvenanceGrade,
)


@dataclass(frozen=True)
class PendingArtifact:
    role: str
    path: Path
    media_type: str
    record_count: int | None = None
    schema_hash: str | None = None
    crs: str | None = None
    geometry_types: tuple[str, ...] = ()


class SnapshotBuilder:
    """Build one snapshot in staging and atomically finalize its directory."""

    def __init__(self, repository: Path, asset: DataAsset):
        self.repository = Path(repository).resolve()
        self.asset = asset
        self.snapshot_uuid = uuid.uuid4()
        self.started_at = datetime.now(UTC)
        self.asset_root = self.repository / asset.storage_root
        self.staging_dir = self.asset_root / ".staging" / str(self.snapshot_uuid)
        self.staging_dir.mkdir(parents=True, exist_ok=False)

    def path(self, relative: str | Path) -> Path:
        destination = (self.staging_dir / relative).resolve()
        if not destination.is_relative_to(self.staging_dir):
            raise ValueError("staging artifact path escapes snapshot directory")
        destination.parent.mkdir(parents=True, exist_ok=True)
        return destination

    def record_failure(self, code: str, error: Exception | str) -> Path:
        """Leave a machine-readable diagnostic in this staging attempt."""
        path = self.path("failure-report.json")
        path.write_text(
            json.dumps(
                {
                    "failure_contract_version": "1.0.0",
                    "asset_id": self.asset.asset_id,
                    "snapshot_id": str(self.snapshot_uuid),
                    "code": code,
                    "message": str(error),
                    "failed_at": datetime.now(UTC).isoformat(),
                },
                indent=2,
            )
            + "\n"
        )
        return path

    def finalize(
        self,
        *,
        artifacts: list[PendingArtifact],
        provenance_grade: ProvenanceGrade,
        parents: list[DataAssetRef] | None = None,
        counts: dict[str, int],
        rejection_counts_by_reason: dict[str, int] | None = None,
        acquisition_fingerprint: dict | None = None,
        parameters: dict | None = None,
        crs: str | None = None,
        geometry_types: tuple[str, ...] = (),
    ) -> DataAssetRef:
        if counts["accepted"] + counts["rejected"] != counts["input"]:
            raise ValueError("snapshot counts must satisfy accepted + rejected = input")
        if self.asset.tier.value == "source" and counts["accepted"] <= 0:
            raise ValueError("a source snapshot cannot complete with zero accepted records")
        rejection_counts_by_reason = rejection_counts_by_reason or {}
        if sum(rejection_counts_by_reason.values()) != counts["rejected"]:
            raise ValueError("rejection reason counts must sum to rejected count")

        completed_at = datetime.now(UTC)
        dated_name = f"{completed_at.date().isoformat()}_{self.snapshot_uuid}"
        final_dir = self.asset_root / "snapshots" / dated_name
        if final_dir.exists():
            raise FileExistsError(final_dir)
        descriptors = [self._descriptor(artifact, final_dir) for artifact in artifacts]
        producer = git_state(self.repository)
        manifest = {
            "manifest_contract_version": "1.0.0",
            "dataset_contract_id": self.asset.contract.contract_id,
            "dataset_contract_version": self.asset.contract.version,
            "schema_hash": schema_hash(self.asset.contract.arrow_schema),
            "asset_id": self.asset.asset_id,
            "snapshot_id": str(self.snapshot_uuid),
            "tier": self.asset.tier.value,
            "status": "complete",
            "provenance_grade": provenance_grade.value,
            "producer": {
                "package_version": version("krabby-real-estate"),
                "git_commit": producer.commit,
                "git_clean": producer.clean,
            },
            "started_at": self.started_at.isoformat(),
            "completed_at": completed_at.isoformat(),
            "acquisition_fingerprint": acquisition_fingerprint,
            "parameters": parameters or {},
            "parents": [
                {
                    "asset_id": parent.asset_id,
                    "snapshot_id": parent.snapshot_id,
                    "manifest_path": parent.manifest_path.resolve()
                    .relative_to(self.repository)
                    .as_posix(),
                    "manifest_sha256": parent.manifest_sha256,
                }
                for parent in parents or []
            ],
            "counts": counts,
            "rejection_counts_by_reason": rejection_counts_by_reason,
            "crs": crs,
            "geometry_types": sorted(set(geometry_types)),
            "artifacts": [
                {
                    "role": descriptor.role,
                    "path": descriptor.path,
                    "media_type": descriptor.media_type,
                    "bytes": descriptor.bytes,
                    "sha256": descriptor.sha256,
                    "record_count": descriptor.record_count,
                    "schema_hash": descriptor.schema_hash,
                    "crs": descriptor.crs,
                    "geometry_types": list(descriptor.geometry_types),
                }
                for descriptor in descriptors
            ],
            "archive_tier": "local_only",
            "archive_status": "not_configured",
        }
        errors = validate_json_document(manifest, "snapshot-manifest-v1.json")
        if errors:
            raise ValueError(f"snapshot manifest failed validation: {'; '.join(errors)}")
        (self.staging_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
        final_dir.parent.mkdir(parents=True, exist_ok=True)
        self.staging_dir.replace(final_dir)
        return manifest_ref(final_dir / "manifest.json")

    def _descriptor(self, pending: PendingArtifact, final_dir: Path) -> ArtifactDescriptor:
        source = pending.path.resolve()
        if not source.is_relative_to(self.repository):
            raise ValueError(f"artifact path is outside repository: {source}")
        if source.is_relative_to(self.staging_dir):
            eventual = final_dir / source.relative_to(self.staging_dir)
        else:
            eventual = source
        return ArtifactDescriptor(
            role=pending.role,
            path=eventual.relative_to(self.repository).as_posix(),
            media_type=pending.media_type,
            bytes=source.stat().st_size,
            sha256=sha256_file(source),
            record_count=pending.record_count,
            schema_hash=pending.schema_hash,
            crs=pending.crs,
            geometry_types=tuple(sorted(set(pending.geometry_types))),
        )


def validate_snapshot(
    repository: Path,
    manifest_path: Path,
    *,
    recursive: bool = True,
    _visited: set[Path] | None = None,
) -> list[str]:
    repository = Path(repository).resolve()
    manifest_path = Path(manifest_path).resolve()
    if not manifest_path.is_relative_to(repository):
        return [f"manifest escapes repository: {manifest_path}"]
    visited = _visited if _visited is not None else set()
    if manifest_path in visited:
        return []
    visited.add(manifest_path)
    try:
        manifest = read_manifest(manifest_path)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        return [str(error)]
    errors = []
    counts = manifest["counts"]
    if counts["accepted"] + counts["rejected"] != counts["input"]:
        errors.append("accepted + rejected does not equal input")
    if sum(manifest["rejection_counts_by_reason"].values()) != counts["rejected"]:
        errors.append("rejection reason counts do not equal rejected count")
    for artifact in manifest["artifacts"]:
        path = (repository / artifact["path"]).resolve()
        if not path.is_relative_to(repository):
            errors.append(f"artifact escapes repository: {artifact['path']}")
            continue
        if not path.exists():
            errors.append(f"artifact missing: {artifact['path']}")
            continue
        if path.stat().st_size != artifact["bytes"]:
            errors.append(f"artifact byte count changed: {artifact['path']}")
        if sha256_file(path) != artifact["sha256"]:
            errors.append(f"artifact hash changed: {artifact['path']}")
        if artifact["media_type"] in {
            "application/vnd.apache.parquet",
            "application/vnd.apache.geoparquet",
        }:
            try:
                parquet = pq.ParquetFile(path)
                if (
                    artifact["record_count"] is not None
                    and parquet.metadata.num_rows != artifact["record_count"]
                ):
                    errors.append(f"Parquet row count changed: {artifact['path']}")
                actual_schema = schema_hash(parquet.schema_arrow)
                if artifact["schema_hash"] and actual_schema != artifact["schema_hash"]:
                    errors.append(f"Parquet schema hash changed: {artifact['path']}")
                if artifact["role"] == "accepted":
                    contract_schema = schema_hash(parquet.schema_arrow.remove_metadata())
                    if contract_schema != manifest["schema_hash"]:
                        errors.append(
                            f"accepted artifact violates contract schema: {artifact['path']}"
                        )
                if artifact["media_type"] == "application/vnd.apache.geoparquet":
                    geo_value = (parquet.schema_arrow.metadata or {}).get(b"geo")
                    if not geo_value:
                        errors.append(f"GeoParquet metadata missing: {artifact['path']}")
                    else:
                        try:
                            geo = json.loads(geo_value)
                        except (TypeError, json.JSONDecodeError):
                            errors.append(f"GeoParquet metadata malformed: {artifact['path']}")
                        else:
                            if geo.get("primary_column") not in parquet.schema_arrow.names:
                                errors.append(
                                    f"GeoParquet primary geometry missing: {artifact['path']}"
                                )
                            declared_types = set(artifact["geometry_types"])
                            metadata_types = {
                                geometry_type
                                for column in geo.get("columns", {}).values()
                                for geometry_type in column.get("geometry_types", [])
                            }
                            if not metadata_types.issubset(declared_types):
                                errors.append(
                                    f"GeoParquet geometry types exceed manifest: {artifact['path']}"
                                )
            except (OSError, pa.ArrowInvalid) as error:
                errors.append(f"invalid Parquet artifact {artifact['path']}: {error}")
    if recursive:
        for parent in manifest["parents"]:
            parent_path = (repository / parent["manifest_path"]).resolve()
            if not parent_path.is_relative_to(repository):
                errors.append(f"parent manifest escapes repository: {parent['manifest_path']}")
                continue
            if not parent_path.exists():
                errors.append(f"parent manifest not found: {parent['manifest_path']}")
                continue
            if sha256_file(parent_path) != parent["manifest_sha256"]:
                errors.append(f"parent manifest hash changed: {parent['asset_id']}")
            else:
                try:
                    parent_manifest = read_manifest(parent_path)
                except (OSError, ValueError, json.JSONDecodeError) as error:
                    errors.append(str(error))
                    continue
                if parent_manifest["asset_id"] != parent["asset_id"]:
                    errors.append(f"parent asset id mismatch: {parent['asset_id']}")
                if parent_manifest["snapshot_id"] != parent["snapshot_id"]:
                    errors.append(f"parent snapshot id mismatch: {parent['asset_id']}")
                errors.extend(
                    validate_snapshot(repository, parent_path, recursive=True, _visited=visited)
                )
    return errors


def promote_snapshot(repository: Path, asset: DataAsset, manifest_path: Path) -> DataAssetRef:
    repository = Path(repository).resolve()
    state = git_state(repository)
    if not state.clean:
        raise RuntimeError("promotion requires a clean Git working tree")
    reference = manifest_ref(manifest_path)
    if reference.asset_id != asset.asset_id:
        raise ValueError("snapshot asset does not match promotion target")
    errors = validate_snapshot(repository, manifest_path)
    if errors:
        raise ValueError(f"snapshot cannot be promoted: {'; '.join(errors)}")
    pointer_path = repository / asset.storage_root / "PROMOTED.json"
    pointer_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_relative = os.path.relpath(reference.manifest_path, pointer_path.parent)
    pointer = {
        "pointer_contract_version": "1.0.0",
        "asset_id": asset.asset_id,
        "snapshot_id": reference.snapshot_id,
        "manifest_path": manifest_relative,
        "manifest_sha256": reference.manifest_sha256,
        "promoted_at": datetime.now(UTC).isoformat(),
    }
    errors = validate_json_document(pointer, "promotion-pointer-v1.json")
    if errors:
        raise ValueError(f"promotion pointer failed validation: {'; '.join(errors)}")
    temporary = pointer_path.with_suffix(".tmp")
    temporary.write_text(json.dumps(pointer, indent=2) + "\n")
    temporary.replace(pointer_path)
    return reference


def discard_staging(builder: SnapshotBuilder) -> None:
    """Explicitly remove one known staging attempt; never targets a dataset root."""
    if builder.staging_dir.exists():
        shutil.rmtree(builder.staging_dir)
