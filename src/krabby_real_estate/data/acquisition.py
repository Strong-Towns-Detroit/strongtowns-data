"""Explicit network acquisition adapters that emit Contract-v1 source snapshots."""

from __future__ import annotations

from datetime import UTC, datetime
from importlib.metadata import version
from pathlib import Path

from pyogrio import read_info

from krabby_real_estate.base_units.service import LAYERS, fetch_layer
from krabby_real_estate.data.catalog import catalog
from krabby_real_estate.data.hashing import sha256_file
from krabby_real_estate.data.model import DataAssetRef, ProvenanceGrade
from krabby_real_estate.data.storage import PendingArtifact, SnapshotBuilder
from krabby_real_estate.parcels.fetcher import ARCGIS_ITEM_ID, FEATURE_SERVICE, fetch_geojson


def fetch_base_units(repository: Path, *, session=None) -> dict[str, DataAssetRef]:
    repository = Path(repository).resolve()
    result = {}
    for name, layer in LAYERS.items():
        asset_id = f"detroit.base-units.{name}.raw"
        asset = catalog.assets[asset_id]
        builder = SnapshotBuilder(repository, asset)
        kwargs = {
            "pause_seconds": 0.05,
            "page_cache_root": repository / "cache/base-units" / name,
        }
        if session is not None:
            kwargs["session"] = session
            kwargs["pause_seconds"] = 0
        try:
            path, provider_manifest = fetch_layer(layer, builder.staging_dir, **kwargs)
            count = int(provider_manifest["feature_count"])
            provider_path = builder.staging_dir / f"base_units_{name}.manifest.json"
            result[asset_id] = builder.finalize(
                artifacts=[
                    PendingArtifact("raw", path, "application/geo+json", count),
                    PendingArtifact("provider_manifest", provider_path, "application/json"),
                ],
                provenance_grade=ProvenanceGrade.NATIVE,
                counts={"input": count, "accepted": count, "rejected": 0},
                acquisition_fingerprint={
                    "service": provider_manifest["service"],
                    "layer": provider_manifest["layer"],
                    "source_state": provider_manifest["source_fingerprint_after"],
                },
                parameters={"page_size": provider_manifest["page_size"]},
            )
        except Exception as error:
            builder.record_failure("acquisition_failed", error)
            raise
    return result


def fetch_parcels(repository: Path) -> DataAssetRef:
    repository = Path(repository).resolve()
    asset = catalog.assets["detroit.parcels.raw"]
    builder = SnapshotBuilder(repository, asset)
    try:
        path = fetch_geojson(builder.path("parcels.geojson"))
        count = int(read_info(path)["features"])
        if count <= 0:
            raise ValueError("parcel export contains no features")
        return builder.finalize(
            artifacts=[PendingArtifact("raw", path, "application/geo+json", count)],
            provenance_grade=ProvenanceGrade.NATIVE,
            counts={"input": count, "accepted": count, "rejected": 0},
            acquisition_fingerprint={
                "arcgis_item_id": ARCGIS_ITEM_ID,
                "feature_service": FEATURE_SERVICE,
                "content_sha256": sha256_file(path),
            },
            parameters={"format": "geojson", "bulk_export": True},
        )
    except Exception as error:
        builder.record_failure("acquisition_failed", error)
        raise


def fetch_osm_pois(repository: Path, *, place: str = "Detroit, Michigan, USA") -> DataAssetRef:
    """Collect a broad, explicitly best-effort OSM source snapshot."""
    from krabby_real_estate.pois.osm import (
        DEFAULT_OSM_TAGS,
        collect_osm_pois,
        write_osm_snapshot,
    )

    repository = Path(repository).resolve()
    asset = catalog.assets["osm.detroit.pois.raw"]
    builder = SnapshotBuilder(repository, asset)
    started_at = datetime.now(UTC)
    try:
        raw, normalized = collect_osm_pois(place=place)
        paths = write_osm_snapshot(raw, normalized, builder.staging_dir)
        count = len(raw)
        if count <= 0:
            raise ValueError("OSM query contains no features")
        return builder.finalize(
            artifacts=[
                PendingArtifact("raw", paths["raw"], "application/geo+json", count),
                PendingArtifact(
                    "normalized_evidence",
                    paths["normalized"],
                    "application/geo+json",
                    len(normalized),
                ),
            ],
            provenance_grade=ProvenanceGrade.BEST_EFFORT,
            counts={"input": count, "accepted": count, "rejected": 0},
            acquisition_fingerprint={
                "source": "openstreetmap",
                "place": place,
                "query_tags": DEFAULT_OSM_TAGS,
                "osmnx_version": version("osmnx"),
                "started_at": started_at.isoformat(),
                "completed_at": datetime.now(UTC).isoformat(),
                "transaction_quality": "best_effort",
            },
            parameters={"routing_points_are_evidence_only": True},
        )
    except Exception as error:
        builder.record_failure("acquisition_failed", error)
        raise
