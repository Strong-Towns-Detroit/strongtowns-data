import json
from unittest.mock import MagicMock

import pytest

from krabby_real_estate.base_units.service import LayerDefinition, fetch_layer


def response(payload):
    result = MagicMock()
    result.json.return_value = payload
    return result


def test_fetch_layer_writes_snapshot_manifest_and_reuses_valid_pages(tmp_path):
    session = MagicMock()
    session.post.side_effect = [
        response({"id": 0, "name": "Addresses", "fields": []}),
        response({"objectIds": [1, 2]}),
        response(
            {
                "type": "FeatureCollection",
                "features": [
                    {"type": "Feature", "properties": {"objectid": 1}, "geometry": None},
                    {"type": "Feature", "properties": {"objectid": 2}, "geometry": None},
                ],
            }
        ),
        response({"id": 0, "name": "Addresses", "fields": []}),
        response({"objectIds": [1, 2]}),
    ]
    layer = LayerDefinition("addresses", 0)

    destination, manifest = fetch_layer(layer, tmp_path, session=session, pause_seconds=0)

    assert destination.exists()
    assert manifest["feature_count"] == 2
    assert manifest["downloaded_pages"] == 1
    assert len(manifest["sha256"]) == 64
    assert len(json.loads(destination.read_text())["features"]) == 2

    resumed = MagicMock()
    resumed.post.side_effect = [
        response({"id": 0, "name": "Addresses", "fields": []}),
        response({"objectIds": [1, 2]}),
        response({"id": 0, "name": "Addresses", "fields": []}),
        response({"objectIds": [1, 2]}),
    ]
    _destination, resumed_manifest = fetch_layer(layer, tmp_path, session=resumed, pause_seconds=0)
    assert resumed.post.call_count == 4
    assert resumed_manifest["downloaded_pages"] == 0
    assert resumed_manifest["reused_pages"] == 1


def test_fetch_layer_rejects_incomplete_arcgis_page(tmp_path):
    session = MagicMock()
    session.post.side_effect = [
        response({"id": 0, "name": "Addresses", "fields": []}),
        response({"objectIds": [1, 2]}),
        response(
            {
                "type": "FeatureCollection",
                "features": [{"type": "Feature", "properties": {"objectid": 1}, "geometry": None}],
            }
        ),
    ]

    with pytest.raises(RuntimeError, match="incomplete addresses page"):
        fetch_layer(LayerDefinition("addresses", 0), tmp_path, session=session, pause_seconds=0)


def test_fetch_layer_rejects_source_drift_during_pagination(tmp_path):
    session = MagicMock()
    session.post.side_effect = [
        response({"id": 0, "name": "Addresses", "fields": []}),
        response({"objectIds": [1]}),
        response(
            {
                "type": "FeatureCollection",
                "features": [{"type": "Feature", "properties": {"objectid": 1}, "geometry": None}],
            }
        ),
        response({"id": 0, "name": "Addresses", "fields": []}),
        response({"objectIds": [1, 2]}),
    ]

    with pytest.raises(RuntimeError, match="changed during pagination"):
        fetch_layer(LayerDefinition("addresses", 0), tmp_path, session=session, pause_seconds=0)
