import builtins

import geopandas as gpd
import networkx as nx
import pytest
from shapely.geometry import LineString, Point

from strongtowns_data.legislative.osm import filter_arterials
from strongtowns_data.osm.basemaps import read_graph, validate_graph, write_graph


def test_directed_multigraph_roundtrip_retains_topology_and_tags(tmp_path, monkeypatch):
    graph = nx.MultiDiGraph(crs="EPSG:4326", simplified=True)
    graph.add_node(1, x=-83.0, y=42.0, highway="crossing")
    graph.add_node(2, x=-83.01, y=42.01)
    line = LineString([(-83, 42), (-83.005, 42.007), (-83.01, 42.01)])
    graph.add_edge(
        1,
        2,
        key=0,
        highway=["residential", "primary"],
        osmid=[77, 78],
        length=100,
        oneway=True,
        geometry=line,
    )
    graph.add_edge(1, 2, key=1, highway="service", osmid=79, length=120)
    original = builtins.__import__

    def guarded(name, *args, **kwargs):
        if name == "osmnx":
            pytest.fail("offline graph IO imported provider")
        return original(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", guarded)
    write_graph(graph, tmp_path)
    restored = read_graph(tmp_path)
    assert set(restored.edges(keys=True)) == {(1, 2, 0), (1, 2, 1)}
    assert not restored.has_edge(2, 1)
    assert restored[1][2][0]["highway"] == ["residential", "primary"]
    assert restored[1][2][0]["osmid"] == [77, 78]
    assert restored[1][2][0]["geometry"].equals_exact(line, 0)
    validate_graph(tmp_path, {"counts": {"nodes": 2, "edges": 2}})
    with pytest.raises(ValueError, match="counts"):
        validate_graph(tmp_path, {"counts": {"nodes": 2, "edges": 1}})
    nodes = gpd.read_parquet(tmp_path / "nodes.parquet").iloc[:1]
    nodes.to_parquet(tmp_path / "nodes.parquet", index=False)
    with pytest.raises(ValueError, match="missing nodes"):
        read_graph(tmp_path)


def test_arterial_filter_checks_every_highway_tag_and_keeps_original_values():
    frame = gpd.GeoDataFrame(
        {"highway": [["residential", "primary"], "service", None, "trunk"]},
        geometry=[Point(0, 0)] * 4,
        crs=4326,
    )
    result = filter_arterials(frame)
    assert result.index.tolist() == [0, 3]
    assert result.iloc[0].highway == ["residential", "primary"]
