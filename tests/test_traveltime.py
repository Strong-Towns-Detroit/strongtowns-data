from datetime import datetime
from unittest.mock import MagicMock

import pytest

from krabby_real_estate.traveltime.client import (
    TIME_MAP_URL,
    ParcelAnchor,
    TimeMapSpec,
    build_time_map_payload,
    collect_time_maps,
)

REFERENCE_TIME = datetime.fromisoformat("2026-08-26T12:00:00-04:00")


def parcel(number):
    return ParcelAnchor(str(number), f"anchor-{number}", 42.33 + number / 10000, -83.05)


def spec(direction="departure"):
    return TimeMapSpec(direction, "walking", 3600, REFERENCE_TIME)


def test_payload_is_parcel_keyed_and_directional():
    payload = build_time_map_payload([parcel(1)], spec("arrival"))
    search = payload["arrival_searches"][0]
    assert search["id"] == "parcel:1:anchor:anchor-1:arrival:walking:3600"
    assert search["arrival_time"] == REFERENCE_TIME.isoformat()
    assert "departure_time" not in search


def test_payload_enforces_api_batch_limit():
    with pytest.raises(ValueError, match="at most 10"):
        build_time_map_payload([parcel(i) for i in range(11)], spec())


def test_collect_batches_parcels_and_preserves_manifest():
    session = MagicMock()
    response = MagicMock()
    response.json.return_value = {
        "type": "FeatureCollection",
        "features": [{"type": "Feature", "properties": {}, "geometry": None}],
    }
    session.post.return_value = response

    geojson, manifest = collect_time_maps(
        [parcel(i) for i in range(11)],
        [spec("departure"), spec("arrival")],
        app_id="app",
        api_key="key",
        session=session,
    )

    assert session.post.call_count == 4
    assert all(call.args[0] == TIME_MAP_URL for call in session.post.call_args_list)
    assert len(geojson["features"]) == 4
    assert manifest["parcel_count"] == 11
    assert manifest["anchor_count"] == 11
    assert manifest["feature_count"] == 4
    headers = session.post.call_args.kwargs["headers"]
    assert headers["Accept"] == "application/geo+json"
    assert "key" not in str(manifest)
