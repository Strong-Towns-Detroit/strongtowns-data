import json

from krabby_real_estate.data.acquisition import fetch_parcels
from krabby_real_estate.data.catalog import catalog
from krabby_real_estate.data.legacy import (
    LEGACY_SOURCES,
    LegacySource,
    register_legacy_source,
)
from krabby_real_estate.data.manifest import read_manifest
from krabby_real_estate.data.storage import validate_snapshot


def test_parcel_acquisition_stages_native_snapshot(tmp_path, monkeypatch):
    def fake_fetch(path):
        path.write_text(
            json.dumps(
                {
                    "type": "FeatureCollection",
                    "features": [
                        {
                            "type": "Feature",
                            "properties": {"object_id": 1, "parcel_id": "1"},
                            "geometry": {
                                "type": "Polygon",
                                "coordinates": [[[0, 0], [1, 0], [1, 1], [0, 0]]],
                            },
                        }
                    ],
                }
            )
        )
        return path

    monkeypatch.setattr("krabby_real_estate.data.acquisition.fetch_geojson", fake_fetch)
    reference = fetch_parcels(tmp_path)
    manifest = read_manifest(reference.manifest_path)
    assert manifest["provenance_grade"] == "native"
    assert manifest["counts"] == {"input": 1, "accepted": 1, "rejected": 0}
    assert manifest["acquisition_fingerprint"]["arcgis_item_id"]
    assert not validate_snapshot(tmp_path, reference.manifest_path)


def test_legacy_registration_is_idempotent_for_identical_bytes(tmp_path, monkeypatch):
    raw_path = tmp_path / "legacy.geojson"
    raw_path.write_text(
        json.dumps(
            {
                "type": "FeatureCollection",
                "features": [
                    {
                        "type": "Feature",
                        "properties": {"object_id": 1, "parcel_id": "1"},
                        "geometry": {"type": "Point", "coordinates": [0, 0]},
                    }
                ],
            }
        )
    )
    monkeypatch.setitem(
        LEGACY_SOURCES,
        "detroit.parcels.raw",
        LegacySource("detroit.parcels.raw", raw_path.relative_to(tmp_path), 1),
    )
    first = register_legacy_source(tmp_path, "detroit.parcels.raw")
    second = register_legacy_source(tmp_path, "detroit.parcels.raw")
    assert second == first
    snapshots = tmp_path / catalog.assets["detroit.parcels.raw"].storage_root / "snapshots"
    assert len(list(snapshots.glob("*/manifest.json"))) == 1
