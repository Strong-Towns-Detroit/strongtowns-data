from datetime import UTC, datetime
from unittest.mock import MagicMock

import pandas as pd
import pytest

from strongtowns_data.traveltime.ledger import (
    LedgerSpec,
    post_batch_with_retry,
    prepare_request_records,
    reconcile_response,
)

NOW = datetime(2026, 8, 26, 16, tzinfo=UTC)


def inputs(status="not_required"):
    anchors = pd.DataFrame(
        [
            {
                "anchor_uuid": "7d72b696-b0a2-5e1d-b267-8d39641c9b0e",
                "parcel_id": "1",
                "latitude": 42.33,
                "longitude": -83.05,
            }
        ]
    )
    dispositions = pd.DataFrame(
        [{"anchor_uuid": anchors.iloc[0].anchor_uuid, "review_status": status}]
    )
    return anchors, dispositions


def spec(direction="departure"):
    return LedgerSpec(direction, "walking", 3600, NOW)


def test_request_ids_are_stable_and_review_gated():
    anchors, dispositions = inputs("required")
    assert prepare_request_records(anchors, dispositions, [spec()]) == []
    records = prepare_request_records(
        anchors,
        dispositions,
        [spec()],
        override_anchor_uuids={anchors.iloc[0].anchor_uuid},
    )
    repeated = prepare_request_records(
        anchors,
        dispositions,
        [spec()],
        override_anchor_uuids={anchors.iloc[0].anchor_uuid},
    )
    assert records == repeated
    assert records[0]["selection_override"] is True


def test_request_preparation_rejects_incomplete_disposition_coverage():
    anchors, dispositions = inputs()
    with pytest.raises(ValueError, match="coverage differs"):
        prepare_request_records(anchors, dispositions.iloc[0:0], [spec()])


def test_reconciliation_requires_exact_success_or_error_ids():
    anchors, dispositions = inputs()
    records = prepare_request_records(anchors, dispositions, [spec()])
    provider_id = records[0]["provider_search_id"]
    response = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"search_id": provider_id},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[[0, 0], [1, 0], [1, 1], [0, 0]]],
                },
            }
        ],
    }
    results = reconcile_response(records, response, NOW)
    assert results[0]["result_status"] == "success"
    with pytest.raises(ValueError, match="missing provider"):
        reconcile_response(records, {"type": "FeatureCollection", "features": []}, NOW)
    response["features"].append(response["features"][0])
    with pytest.raises(ValueError, match="duplicate provider"):
        reconcile_response(records, response, NOW)


def test_provider_errors_reconcile_but_remain_explicit():
    anchors, dispositions = inputs()
    records = prepare_request_records(anchors, dispositions, [spec()])
    response = {
        "type": "FeatureCollection",
        "features": [],
        "errors": [
            {
                "search_id": records[0]["provider_search_id"],
                "code": "NO_ROUTE",
                "message": "No reachable area",
            }
        ],
    }
    results = reconcile_response(records, response, NOW)
    assert results[0]["provider_error_code"] == "NO_ROUTE"


def test_retry_is_bounded_and_honors_retry_after():
    anchors, dispositions = inputs()
    records = prepare_request_records(anchors, dispositions, [spec()])
    session = MagicMock()
    retry = MagicMock(status_code=429, headers={"Retry-After": "0"})
    success = MagicMock(status_code=200, headers={})
    success.json.return_value = {"type": "FeatureCollection", "features": []}
    session.post.side_effect = [retry, success]
    sleep = MagicMock()
    assert (
        post_batch_with_retry(records, app_id="app", api_key="secret", session=session, sleep=sleep)
        == success.json.return_value
    )
    assert session.post.call_count == 2
    sleep.assert_called_once_with(0.0)
