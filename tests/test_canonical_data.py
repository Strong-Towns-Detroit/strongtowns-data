import json

import geopandas as gpd
import pyarrow.parquet as pq
from shapely.geometry import Polygon

from krabby_real_estate.data.canonical import canonicalize_parcels
from krabby_real_estate.data.catalog import catalog
from krabby_real_estate.data.manifest import read_manifest
from krabby_real_estate.data.model import ProvenanceGrade
from krabby_real_estate.data.storage import PendingArtifact, SnapshotBuilder, validate_snapshot


def test_parcel_canonicalization_reconciles_accepted_and_rejected(tmp_path):
    source = gpd.GeoDataFrame(
        {
            "object_id": [1, 2],
            "parcel_id": ["10-00.1", None],
        },
        geometry=[
            Polygon([(0, 0), (1, 0), (1, 1), (0, 0)]),
            Polygon([(2, 0), (3, 0), (3, 1), (2, 0)]),
        ],
        crs="EPSG:4326",
    )
    raw_path = tmp_path / "legacy.geojson"
    source.to_file(raw_path, driver="GeoJSON")
    raw_builder = SnapshotBuilder(tmp_path, catalog.assets["detroit.parcels.raw"])
    raw_ref = raw_builder.finalize(
        artifacts=[PendingArtifact("raw", raw_path, "application/geo+json", 2)],
        provenance_grade=ProvenanceGrade.LEGACY,
        counts={"input": 2, "accepted": 2, "rejected": 0},
        acquisition_fingerprint={"source_url": None, "retrieved_at": None},
    )

    canonical_ref = canonicalize_parcels(tmp_path, raw_ref)
    manifest = read_manifest(canonical_ref.manifest_path)
    assert manifest["counts"] == {"input": 2, "accepted": 1, "rejected": 1}
    assert manifest["rejection_counts_by_reason"] == {"missing_required_value": 1}
    assert manifest["parents"][0]["manifest_path"] == str(
        raw_ref.manifest_path.relative_to(tmp_path)
    )
    accepted_path = tmp_path / next(
        item["path"] for item in manifest["artifacts"] if item["role"] == "accepted"
    )
    accepted = gpd.read_parquet(accepted_path)
    assert accepted.loc[0, "parcel_id"] == "10-00.1"
    assert accepted.loc[0, "parcel_key"] == "10001"
    rejects_path = tmp_path / next(
        item["path"] for item in manifest["artifacts"] if item["role"] == "rejects"
    )
    assert pq.read_table(rejects_path)["source_row_locator"].to_pylist() == ["2"]
    assert validate_snapshot(tmp_path, canonical_ref.manifest_path) == []


def test_snapshot_manifest_rejects_invalid_uuid_format(tmp_path):
    document = {
        "manifest_contract_version": "1.0.0",
        "dataset_contract_id": "x",
        "dataset_contract_version": "1.0.0",
        "schema_hash": None,
        "asset_id": "x",
        "snapshot_id": "not-a-uuid",
    }
    path = tmp_path / "manifest.json"
    path.write_text(json.dumps(document))
    errors = validate_snapshot(tmp_path, path)
    assert errors
