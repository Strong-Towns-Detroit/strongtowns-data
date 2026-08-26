from datetime import UTC, datetime
from pathlib import Path
from unittest.mock import MagicMock

import pandas as pd

from krabby_real_estate.data.manifest import read_manifest
from krabby_real_estate.data.model import DataAssetRef
from krabby_real_estate.data.pipelines import collect_traveltime_results
from krabby_real_estate.data.storage import validate_snapshot


def test_collection_batches_arrival_and_departure_separately(tmp_path, monkeypatch):
    request_path = tmp_path / "requests.parquet"
    records = []
    for direction in ("arrival", "departure"):
        records.append(
            {
                "request_uuid": f"request-{direction}",
                "provider_search_id": f"provider-{direction}",
                "anchor_uuid": "anchor-1",
                "parcel_id": "1",
                "direction": direction,
                "transportation": "walking",
                "travel_time_seconds": 3600,
                "reference_time_utc": datetime(2026, 8, 26, 16, tzinfo=UTC),
                "latitude": 42.0,
                "longitude": -83.0,
                "selection_override": False,
            }
        )
    pd.DataFrame(records).to_parquet(request_path, index=False)
    monkeypatch.setattr(
        "krabby_real_estate.data.pipelines.artifact_path",
        lambda _repository, _reference: request_path,
    )
    session = MagicMock()

    def response_for(_url, *, json, **_kwargs):
        searches = next(iter(json.values()))
        response = MagicMock(status_code=200, headers={})
        response.json.return_value = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {"search_id": search["id"]},
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[[0, 0], [1, 0], [1, 1], [0, 0]]],
                    },
                }
                for search in searches
            ],
        }
        return response

    session.post.side_effect = response_for
    parent = DataAssetRef(
        "traveltime.requests",
        "42178d46-82ce-47ab-bd45-c77231ffca90",
        Path(tmp_path / "parent-manifest.json"),
        "a" * 64,
    )
    reference = collect_traveltime_results(
        tmp_path, parent, app_id="app", api_key="secret", session=session
    )
    manifest = read_manifest(reference.manifest_path)
    assert session.post.call_count == 2
    assert manifest["counts"] == {"input": 2, "accepted": 2, "rejected": 0}
    assert sum(item["role"] == "raw_response" for item in manifest["artifacts"]) == 2
    assert validate_snapshot(tmp_path, reference.manifest_path, recursive=False) == []
