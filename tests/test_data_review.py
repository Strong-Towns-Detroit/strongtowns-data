from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from krabby_real_estate.data.model import DataAssetRef
from krabby_real_estate.data.review import export_anchor_review, validate_review_frame


def reference(asset_id, snapshot="8dbb390d-9f3f-4a15-b5db-120af2dfddfb", digest="a"):
    return DataAssetRef(asset_id, snapshot, Path("manifest.json"), digest * 64)


def review_frame(anchor_hash="a", disposition_hash="b"):
    return pd.DataFrame(
        [
            {
                "anchor_uuid": "anchor-1",
                "proposed_review_status": "approved",
                "reviewer": "reviewer@example.com",
                "reviewed_at": "2026-08-26T16:00:00Z",
                "anchor_manifest_sha256": anchor_hash * 64,
                "disposition_manifest_sha256": disposition_hash * 64,
            }
        ]
    )


def test_review_validation_accepts_fresh_complete_disposition():
    frame = review_frame()
    selected = validate_review_frame(
        frame,
        reference("detroit.parcel-routing-anchors", digest="a"),
        reference("detroit.anchor-dispositions", digest="b"),
        {"anchor-1"},
    )
    assert selected.iloc[0].proposed_review_status == "approved"


def test_review_validation_rejects_stale_parent_and_incomplete_decision():
    with pytest.raises(ValueError, match="stale"):
        validate_review_frame(
            review_frame(anchor_hash="c"),
            reference("detroit.parcel-routing-anchors", digest="a"),
            reference("detroit.anchor-dispositions", digest="b"),
            {"anchor-1"},
        )


def test_review_export_serializes_arrow_list_values(tmp_path, monkeypatch):
    import geopandas as gpd
    from shapely.geometry import Point

    anchors = gpd.GeoDataFrame(
        {
            "anchor_uuid": ["anchor-1"],
            "parcel_id": ["1"],
            "street_id": ["2"],
            "longitude": [-83.0],
            "latitude": [42.0],
        },
        geometry=[Point(-83, 42)],
        crs="EPSG:4326",
    )
    dispositions = pd.DataFrame(
        {
            "anchor_uuid": ["anchor-1"],
            "review_status": ["required"],
            "review_reasons": [np.array(["fallback_anchor"], dtype=object)],
            "reviewer": [None],
            "reviewed_at": [None],
            "evidence_uri": [None],
            "notes": [None],
        }
    )
    monkeypatch.setattr(
        "krabby_real_estate.data.review.artifact_path",
        lambda _repository, reference: Path(reference.asset_id),
    )
    monkeypatch.setattr("krabby_real_estate.data.review.gpd.read_parquet", lambda _path: anchors)
    monkeypatch.setattr(
        "krabby_real_estate.data.review.pd.read_parquet", lambda _path: dispositions
    )
    output = tmp_path / "review.csv"
    export_anchor_review(
        tmp_path,
        reference("detroit.parcel-routing-anchors", digest="a"),
        reference("detroit.anchor-dispositions", digest="b"),
        output,
    )
    exported = pd.read_csv(output, dtype=str, keep_default_na=False)
    assert exported.loc[0, "review_reasons"] == '["fallback_anchor"]'
    incomplete = review_frame()
    incomplete.loc[0, "reviewer"] = ""
    with pytest.raises(ValueError, match="require reviewer"):
        validate_review_frame(
            incomplete,
            reference("detroit.parcel-routing-anchors", digest="a"),
            reference("detroit.anchor-dispositions", digest="b"),
            {"anchor-1"},
        )
