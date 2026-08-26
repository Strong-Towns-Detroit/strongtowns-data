"""Public data-engine value objects.

The objects in this module are deliberately small and immutable. Filesystem mutation and
promotion live in :mod:`krabby_real_estate.data.storage`.
"""

from __future__ import annotations

import re
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path
from typing import Any

import pyarrow as pa

_STABLE_ID = re.compile(r"^[a-z][a-z0-9]*(?:[._-][a-z0-9]+)*$")


class Tier(StrEnum):
    SOURCE = "source"
    DERIVED = "derived"
    PROVIDER = "provider"


class AcquisitionPolicy(StrEnum):
    OFFLINE = "offline"
    NETWORK = "network"
    PAID = "paid"


class ProvenanceGrade(StrEnum):
    NATIVE = "native"
    LEGACY = "legacy"
    BEST_EFFORT = "best_effort"


@dataclass(frozen=True)
class ValidationIssue:
    code: str
    message: str
    record_locator: str | None = None


@dataclass
class ValidationResult:
    issues: list[ValidationIssue] = field(default_factory=list)
    warnings: list[ValidationIssue] = field(default_factory=list)

    @property
    def valid(self) -> bool:
        return not self.issues

    def require(self, condition: bool, code: str, message: str) -> None:
        if not condition:
            self.issues.append(ValidationIssue(code, message))

    def extend(self, other: ValidationResult) -> None:
        self.issues.extend(other.issues)
        self.warnings.extend(other.warnings)


TableValidator = Callable[[pa.Table], ValidationResult]


@dataclass(frozen=True)
class DatasetContract:
    contract_id: str
    version: str
    arrow_schema: pa.Schema | None = None
    primary_key: tuple[str, ...] = ()
    foreign_keys: Mapping[tuple[str, ...], tuple[str, tuple[str, ...]]] = field(
        default_factory=dict
    )
    geometry_column: str | None = None
    geometry_types: tuple[str, ...] = ()
    crs: str | None = None
    validators: tuple[TableValidator, ...] = ()

    def __post_init__(self):
        _require_stable_id(self.contract_id, "contract_id")
        if not re.fullmatch(r"\d+\.\d+\.\d+", self.version):
            raise ValueError("contract version must use MAJOR.MINOR.PATCH")


@dataclass(frozen=True)
class DataAsset:
    asset_id: str
    tier: Tier
    media_type: str
    contract: DatasetContract
    storage_root: Path
    producer_pipeline_id: str | None = None
    acquisition_policy: AcquisitionPolicy = AcquisitionPolicy.OFFLINE
    archive_tier: str = "local_only"

    def __post_init__(self):
        _require_stable_id(self.asset_id, "asset_id")
        if self.producer_pipeline_id:
            _require_stable_id(self.producer_pipeline_id, "producer_pipeline_id")
        if self.storage_root.is_absolute() or ".." in self.storage_root.parts:
            raise ValueError("storage_root must be repository-relative and cannot escape")


@dataclass(frozen=True)
class DataAssetRef:
    asset_id: str
    snapshot_id: str
    manifest_path: Path
    manifest_sha256: str

    def __post_init__(self):
        _require_stable_id(self.asset_id, "asset_id")
        if not re.fullmatch(r"[a-f0-9]{64}", self.manifest_sha256):
            raise ValueError("manifest_sha256 must be a lowercase SHA-256 digest")


@dataclass(frozen=True)
class ArtifactDescriptor:
    role: str
    path: str
    media_type: str
    bytes: int
    sha256: str
    record_count: int | None = None
    schema_hash: str | None = None
    crs: str | None = None
    geometry_types: tuple[str, ...] = ()


PipelineBuilder = Callable[["PipelineContext"], Mapping[str, Path]]


@dataclass(frozen=True)
class PipelineDefinition:
    pipeline_id: str
    inputs: tuple[str, ...]
    outputs: tuple[str, ...]
    builder: PipelineBuilder | None = None

    def __post_init__(self):
        _require_stable_id(self.pipeline_id, "pipeline_id")
        for value in (*self.inputs, *self.outputs):
            _require_stable_id(value, "asset_id")


@dataclass(frozen=True)
class PipelineContext:
    pipeline: PipelineDefinition
    inputs: Mapping[str, DataAssetRef]
    parameters: Mapping[str, Any]
    staging_dir: Path


def _require_stable_id(value: str, label: str) -> None:
    if not _STABLE_ID.fullmatch(value):
        raise ValueError(f"invalid {label} {value!r}")
