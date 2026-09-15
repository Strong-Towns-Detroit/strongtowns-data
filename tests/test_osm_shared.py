"""Shared OSM contract, adapter, and acquisition-boundary regressions."""

import json
from types import SimpleNamespace

import geopandas as gpd
import pandas as pd
import pytest
from shapely.geometry import Point, Polygon

from strongtowns_data.osm import prepare_features, read_features, routing_points
from strongtowns_data.osm.acquisition import acquire_features, fingerprint
from strongtowns_data.pipelines.osm import normalize_osm_features
from strongtowns_data.pois.osm import normalize_osm_pois


def fixture():
    return gpd.GeoDataFrame(
        {
            "amenity": ["cafe", None],
            "shop": ["bakery", None],
            "craft": [None, "carpenter"],
            "name": ["Cafe", "Maker"],
            "custom:tag": [["one", None, "two"], None],
        },
        index=pd.MultiIndex.from_tuples([("way", 22), ("node", 11)], names=["element", "id"]),
        geometry=[Polygon([(0, 0), (0, 1), (1, 1), (0, 0)]), Point(1, 1)],
        crs=4326,
    )


def test_source_roundtrip_keeps_tags_geometry_and_stable_order(tmp_path):
    raw = fixture()
    source, rejects = prepare_features(raw)
    assert rejects.empty
    assert source.source_id.tolist() == ["osm:node:11", "osm:way:22"]
    assert json.loads(source.iloc[1].source_tags_json)["custom:tag"] == ["one", None, "two"]
    assert source.iloc[1].geometry.equals_exact(raw.iloc[0].geometry, 0)
    source.to_parquet(tmp_path / "raw.parquet")
    pd.testing.assert_frame_equal(read_features(tmp_path), source)
    again, _ = prepare_features(source)
    pd.testing.assert_frame_equal(again, source)
    reverse, _ = prepare_features(raw.iloc[::-1])
    pd.testing.assert_frame_equal(reverse, source)
    points, _ = routing_points(source)
    assert points.iloc[1].routing_point_method == "representative_point"
    assert raw.iloc[0].geometry.covers(points.iloc[1].geometry)
    assert points.iloc[0].primary_category == "craft"


def test_adapters_keep_distinct_category_precedence():
    raw = fixture().iloc[:1]
    assert normalize_osm_features(raw).iloc[0].primary_category == "amenity"
    assert normalize_osm_pois(raw).iloc[0].primary_category == "shop"


def test_empty_and_all_rejected_have_typed_columns(tmp_path):
    for raw in (fixture().iloc[:0], fixture().assign(geometry=None)):
        source, rejects = prepare_features(raw)
        assert source.empty
        assert len(rejects) == len(raw)
        source.to_parquet(tmp_path / "raw.parquet")
        assert read_features(tmp_path).source_id.dtype == "string"
        points, _ = routing_points(source)
        assert points.empty and str(points.primary_category.dtype) == "string"


def test_invalid_geometry_is_preserved_as_rejection_evidence():
    raw = fixture().iloc[:1].copy()
    raw.geometry = [Polygon([(0, 0), (1, 1), (1, 0), (0, 1), (0, 0)])]
    source, rejects = prepare_features(raw)
    assert source.empty
    assert rejects.iloc[0].reason == "invalid_geometry"
    assert rejects.iloc[0].geometry_wkb == raw.iloc[0].geometry.wkb_hex
    assert '"name": "Cafe"' in rejects.iloc[0].source_tags_json


def test_missing_crs_and_duplicate_identity_fail():
    raw = fixture()
    with pytest.raises(ValueError, match="CRS"):
        prepare_features(raw.set_crs(None, allow_override=True))
    with pytest.raises(ValueError, match="duplicate"):
        prepare_features(pd.concat([raw, raw]))
    source, _ = prepare_features(raw)
    source.loc[0, "source_id"] = "osm:way:wrong"
    with pytest.raises(ValueError, match="disagrees"):
        prepare_features(source)


def fake_osmnx(monkeypatch):
    import sys

    settings = SimpleNamespace(
        use_cache=False,
        cache_folder="original",
        overpass_url="https://osm.test",
        overpass_settings="[out:json]",
        overpass_memory=None,
        requests_timeout=30,
        max_query_area_size=2500000000,
        default_access="",
        bidirectional_network_types=["walk"],
        useful_tags_node=["highway"],
        useful_tags_way=["highway"],
        nominatim_url="https://geo.test",
    )
    ox = SimpleNamespace(
        settings=settings, __version__="test", features_from_polygon=lambda *a, **k: fixture()
    )
    monkeypatch.setitem(sys.modules, "osmnx", ox)
    return ox


def test_query_fingerprints_include_boundary_tags_endpoint_and_restore_settings(
    tmp_path, monkeypatch
):
    ox = fake_osmnx(monkeypatch)
    poly = fixture().iloc[0].geometry
    a = acquire_features(boundary=poly, cache_root=tmp_path)
    b = acquire_features(boundary=poly.buffer(0.01), cache_root=tmp_path)
    c = acquire_features(boundary=poly, tags={"shop": True}, cache_root=tmp_path)
    d = acquire_features(boundary=poly, endpoint="https://different.test", cache_root=tmp_path)
    assert len({r.metadata["cache_fingerprint"] for r in (a, b, c, d)}) == 4
    assert ox.settings.cache_folder == "original" and ox.settings.use_cache is False
    assert ox.settings.overpass_url == "https://osm.test"
    assert fingerprint(a.metadata["query"]) == a.metadata["cache_fingerprint"]


def test_acquisition_failure_restores_settings_and_cannot_write_snapshot(tmp_path, monkeypatch):
    ox = fake_osmnx(monkeypatch)

    def fail(*args, **kwargs):
        raise RuntimeError("provider failed")

    ox.features_from_polygon = fail
    with pytest.raises(RuntimeError, match="provider failed"):
        acquire_features(boundary=fixture().iloc[0].geometry, cache_root=tmp_path)
    assert ox.settings.cache_folder == "original"
    assert not list(tmp_path.rglob("raw.parquet"))


def test_build_and_read_do_not_import_provider(tmp_path, monkeypatch):
    import builtins

    from strongtowns_data.osm.pipelines import POIS, POIS_RAW, build_pois

    source, _ = prepare_features(fixture())
    source.to_parquet(tmp_path / "raw.parquet")
    out = tmp_path / "out"
    out.mkdir()
    original = builtins.__import__

    def guarded(name, *args, **kwargs):
        if name == "osmnx":
            pytest.fail("offline build imported provider")
        return original(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", guarded)
    metadata = build_pois(SimpleNamespace(inputs={POIS_RAW.id: tmp_path}, staging={POIS.id: out}))
    assert metadata[POIS.id].counts == {"input": 2, "accepted": 2, "rejected": 0}
    assert len(read_features(tmp_path)) == 2
