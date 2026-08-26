"""Honest registration of the known 2026-08-26 legacy source bytes."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from pyogrio import read_info

from krabby_real_estate.data.catalog import catalog
from krabby_real_estate.data.hashing import sha256_file
from krabby_real_estate.data.manifest import manifest_ref, read_manifest
from krabby_real_estate.data.model import DataAssetRef, ProvenanceGrade
from krabby_real_estate.data.storage import PendingArtifact, SnapshotBuilder, validate_snapshot


@dataclass(frozen=True)
class LegacySource:
    asset_id: str
    path: Path
    expected_count: int


LEGACY_SOURCES = {
    item.asset_id: item
    for item in (
        LegacySource(
            "detroit.parcels.raw",
            Path("data/raw/parcels/2026-08-26/parcels.geojson"),
            377_940,
        ),
        LegacySource(
            "detroit.base-units.addresses.raw",
            Path("data/raw/base-units/2026-08-26/base_units_addresses.geojson"),
            486_646,
        ),
        LegacySource(
            "detroit.base-units.streets.raw",
            Path("data/raw/base-units/2026-08-26/base_units_streets.geojson"),
            36_104,
        ),
        LegacySource(
            "detroit.base-units.buildings.raw",
            Path("data/raw/base-units/2026-08-26/base_units_buildings.geojson"),
            364_096,
        ),
        LegacySource(
            "osm.detroit.pois.raw",
            Path("data/raw/pois/osm/2026-08-26/osm-pois.raw.geojson"),
            15_202,
        ),
    )
}


def register_legacy_source(repository: Path, asset_id: str) -> DataAssetRef:
    """Register existing bytes without fabricating their URL or retrieval timestamp."""
    repository = Path(repository).resolve()
    spec = LEGACY_SOURCES[asset_id]
    path = (repository / spec.path).resolve()
    if not path.exists():
        raise FileNotFoundError(path)
    count = int(read_info(path)["features"])
    if count != spec.expected_count:
        raise ValueError(
            f"legacy baseline mismatch for {asset_id}: expected {spec.expected_count}, got {count}"
        )
    content_hash = sha256_file(path)
    asset = catalog.assets[asset_id]
    for candidate in sorted(
        (repository / asset.storage_root / "snapshots").glob("*/manifest.json")
    ):
        manifest = read_manifest(candidate)
        fingerprint = manifest.get("acquisition_fingerprint") or {}
        if (
            manifest["provenance_grade"] == "legacy"
            and fingerprint.get("content_sha256") == content_hash
            and not validate_snapshot(repository, candidate)
        ):
            return manifest_ref(candidate)
    builder = SnapshotBuilder(repository, asset)
    return builder.finalize(
        artifacts=[
            PendingArtifact("raw", path, "application/geo+json", record_count=count, crs=None)
        ],
        provenance_grade=ProvenanceGrade.LEGACY,
        counts={"input": count, "accepted": count, "rejected": 0},
        acquisition_fingerprint={
            "source_url": None,
            "retrieved_at": None,
            "legacy_path": spec.path.as_posix(),
            "content_sha256": content_hash,
        },
        parameters={"legacy_import": True},
    )
