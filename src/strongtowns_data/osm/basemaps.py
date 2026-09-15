"""Boundary, water, and street evidence with offline graph and map readers."""

import json
from pathlib import Path

import geopandas as gpd
import networkx as nx
import pandas as pd
from shapely.geometry import LineString, Point

from strongtowns_data.models import (
    AcquisitionPolicy,
    ArchiveTier,
    BuildMetadata,
    DataAsset,
    DataPipeline,
    DatasetModel,
)
from strongtowns_data.pipelines.registry import data_pipeline

from .features import json_tags, plain, prepare_features
from .pipelines import _asset

DETROIT = ["Detroit, Michigan, USA"]
HD9 = [
    *DETROIT,
    "Hamtramck, Michigan, USA",
    "Highland Park, Michigan, USA",
    "Grosse Pointe Park, Michigan, USA",
]
WATER_TAGS = {"natural": "water"}


def write_graph(graph, directory):
    """Preserve directed multigraph identities and typed attributes in GeoParquet."""
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    crs = graph.graph.get("crs")
    if crs is None or not graph.is_directed() or not graph.is_multigraph():
        raise ValueError("OSM street source must be a directed multigraph with a CRS")
    nodes = [
        (node, json_tags(plain(attrs)), Point(attrs["x"], attrs["y"]))
        for node, attrs in sorted(graph.nodes(data=True))
    ]
    edges = [
        (
            u,
            v,
            key,
            json_tags(plain({k: val for k, val in attrs.items() if k != "geometry"})),
            attrs.get("geometry")
            or LineString(
                [
                    (graph.nodes[u]["x"], graph.nodes[u]["y"]),
                    (graph.nodes[v]["x"], graph.nodes[v]["y"]),
                ]
            ),
        )
        for u, v, key, attrs in sorted(graph.edges(keys=True, data=True))
    ]
    gpd.GeoDataFrame(nodes, columns=["node_id", "attributes_json", "geometry"], crs=crs).to_parquet(
        directory / "nodes.parquet", index=False
    )
    gpd.GeoDataFrame(
        edges, columns=["u", "v", "key", "attributes_json", "geometry"], crs=crs
    ).to_parquet(directory / "edges.parquet", index=False)
    (directory / "graph.json").write_text(json_tags(plain(dict(graph.graph))) + "\n")


def read_graph(directory):
    """Reconstruct a pinned street graph without OSMnx or network access."""
    directory = Path(directory)
    graph = nx.MultiDiGraph(**json.loads((directory / "graph.json").read_text()))
    nodes = gpd.read_parquet(directory / "nodes.parquet")
    edges = gpd.read_parquet(directory / "edges.parquet")
    if nodes.node_id.duplicated().any() or edges.duplicated(["u", "v", "key"]).any():
        raise ValueError("Duplicate OSM graph identity")
    if (set(edges.u) | set(edges.v)) - set(nodes.node_id):
        raise ValueError("OSM graph edge references missing nodes")
    for row in nodes.itertuples():
        graph.add_node(row.node_id, **json.loads(row.attributes_json))
    for row in edges.itertuples():
        graph.add_edge(
            row.u, row.v, key=row.key, **json.loads(row.attributes_json), geometry=row.geometry
        )
    return graph


def validate_boundary(directory, _manifest):
    from .acquisition import validate_acquisition

    validate_acquisition(directory)


def validate_graph(directory, manifest):
    graph = read_graph(directory)
    if not graph.number_of_nodes() or not graph.number_of_edges():
        raise ValueError("OSM street graph must not be empty")
    counts = manifest.get("counts", {})
    if (
        counts.get("nodes") != graph.number_of_nodes()
        or counts.get("edges") != graph.number_of_edges()
    ):
        raise ValueError("OSM graph counts disagree with manifest")
    for name in ("nodes.parquet", "edges.parquet"):
        frame = gpd.read_parquet(directory / name)
        if frame.crs is None or frame.crs.to_epsg() != 4326 or not frame.geometry.is_valid.all():
            raise ValueError("Invalid OSM graph geometry or CRS")


def validate_street_snapshot(directory, manifest):
    from .acquisition import validate_acquisition

    validate_acquisition(directory)
    validate_graph(directory, manifest)


def assets(region):
    boundary = DataAsset(
        f"{region}.osm.boundaries.raw",
        Path(f"data/datasets/{region}-osm-boundaries-source"),
        DatasetModel(
            f"{region}.osm.boundaries.raw",
            "1.0.0",
            accepted_artifact="boundary.parquet",
            geometry_types=("Polygon", "MultiPolygon"),
            crs="EPSG:4326",
            custom_validator=validate_boundary,
        ),
        ArchiveTier.SOURCE,
    )
    water = _asset(f"{region}.osm.water.raw", f"{region}-osm-water-source")
    streets = DataAsset(
        f"{region}.osm.streets.raw",
        Path(f"data/datasets/{region}-osm-streets-source"),
        DatasetModel(
            f"{region}.osm.streets.raw", "1.0.0", custom_validator=validate_street_snapshot
        ),
        ArchiveTier.SOURCE,
    )
    return {"boundaries": boundary, "water": water, "streets": streets}


def source_pipeline(region, kind, places):
    registered = assets(region)
    asset = registered[kind]
    boundary_asset = registered["boundaries"]

    def fetch(context):
        from .acquisition import (
            acquire_boundaries,
            acquire_features,
            acquire_graph,
            write_provenance,
        )

        out = context.staging[asset.id]
        kwargs = {"cache_root": context.root / "data/.cache/osm"}
        if kind == "boundaries":
            result = acquire_boundaries(place=places, **kwargs)
            counts = {"records": len(result.boundary)}
        else:
            bounds = gpd.read_parquet(context.inputs[boundary_asset.id] / "boundary.parquet")
            if kind == "water":
                result = acquire_features(boundary=bounds, tags=WATER_TAGS, **kwargs)
                source, rejected = prepare_features(result.data)
                source.to_parquet(out / "raw.parquet", index=False)
                rejected.to_parquet(out / "rejects.parquet", index=False)
                counts = {
                    "input": len(result.data),
                    "accepted": len(source),
                    "rejected": len(rejected),
                }
            else:
                result = acquire_graph(
                    boundary=bounds, network_type="drive", simplify=True, **kwargs
                )
                write_graph(result.data, out)
                counts = {
                    "nodes": result.data.number_of_nodes(),
                    "edges": result.data.number_of_edges(),
                }
        write_provenance(result, out)
        return {
            asset.id: BuildMetadata(
                counts=counts, source=result.metadata, transaction_quality="best_effort"
            )
        }

    name = f"{region}-osm-{kind}-source"
    return DataPipeline(
        name,
        () if kind == "boundaries" else (boundary_asset.id,),
        (asset,),
        fetch=fetch,
        acquisition_policy=AcquisitionPolicy.PUBLIC_NETWORK,
        description=f"Explicit {region} OSM {kind} acquisition with preserved evidence.",
    )


@data_pipeline("detroit-osm-boundaries-source")
def detroit_osm_boundaries_source():
    return source_pipeline("detroit", "boundaries", DETROIT)


@data_pipeline("detroit-osm-water-source")
def detroit_osm_water_source():
    return source_pipeline("detroit", "water", DETROIT)


@data_pipeline("detroit-osm-streets-source")
def detroit_osm_streets_source():
    return source_pipeline("detroit", "streets", DETROIT)


@data_pipeline("hd9-osm-boundaries-source")
def hd9_osm_boundaries_source():
    return source_pipeline("hd9", "boundaries", HD9)


@data_pipeline("hd9-osm-water-source")
def hd9_osm_water_source():
    return source_pipeline("hd9", "water", HD9)


@data_pipeline("hd9-osm-streets-source")
def hd9_osm_streets_source():
    return source_pipeline("hd9", "streets", HD9)


def read_map_layers(*, boundaries, water, streets, drop_lakes=("Lake St. Clair",)):
    """Open prepared legislative-map layers; display filtering leaves sources intact."""
    cities = gpd.read_parquet(Path(boundaries) / "boundary.parquet")
    features = gpd.read_parquet(Path(water) / "raw.parquet")
    tags = features.source_tags_json.map(json.loads)
    water_frame = features.copy()
    water_frame["name"] = tags.map(lambda t: t.get("name"))
    water_frame = water_frame[
        water_frame.geometry.geom_type.isin(["Polygon", "MultiPolygon"])
        & ~water_frame.name.isin(drop_lakes)
    ].copy()
    edges = gpd.read_parquet(Path(streets) / "edges.parquet")
    attrs = pd.DataFrame(edges.attributes_json.map(json.loads).tolist(), index=edges.index)
    for column in attrs:
        if column not in edges:
            edges[column] = attrs[column]
    return {"cities": cities, "water": water_frame, "streets": edges}
