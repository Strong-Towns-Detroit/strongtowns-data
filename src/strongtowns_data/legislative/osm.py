"""Fetch OSM street and water features for a list of municipalities.

Used for state legislative district maps where the district crosses
multiple city boundaries (e.g. MI HD-9 spans Detroit, Hamtramck,
Highland Park, Grosse Pointe Park).
"""

import json
from pathlib import Path

import geopandas as gpd

from strongtowns_data.osm.acquisition import acquire_boundaries, acquire_features, acquire_graph

# Highway types worth rendering on small choropleth panels.
ARTERIAL_HIGHWAYS = {
    "motorway",
    "motorway_link",
    "trunk",
    "trunk_link",
    "primary",
    "primary_link",
    "secondary",
    "secondary_link",
    "tertiary",
    "tertiary_link",
}


def fetch_place_boundaries(places: list[str]) -> gpd.GeoDataFrame:
    """Geocode a list of place names to their administrative boundaries."""
    return acquire_boundaries(place=places).data


def fetch_streets(places: list[str]) -> gpd.GeoDataFrame:
    """Fetch the drive-network for the union of the given places.

    Returns
    -------
    GeoDataFrame of edges with a 'highway' column.
    """
    import osmnx as ox

    graph = acquire_graph(place=places, network_type="drive", simplify=True).data
    # Keep u/v/key and list-valued tags; flatten only in a display interpretation.
    edges = ox.graph_to_gdfs(graph, nodes=False, edges=True).reset_index()
    return edges


def filter_arterials(edges: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """Keep only motorway/trunk/primary/secondary/tertiary edges."""
    if "highway" not in edges.columns:
        return edges

    def arterial(value):
        if isinstance(value, str) and value.startswith("["):
            try:
                value = json.loads(value)
            except json.JSONDecodeError:
                return False
        if isinstance(value, (list, tuple)):
            return any(tag in ARTERIAL_HIGHWAYS for tag in value)
        return isinstance(value, str) and value in ARTERIAL_HIGHWAYS

    return edges[edges["highway"].map(arterial)].copy()


def fetch_water(
    places: list[str], drop_lakes: tuple[str, ...] = ("Lake St. Clair",)
) -> gpd.GeoDataFrame:
    """Fetch water polygons inside the union of place boundaries."""
    bounds = fetch_place_boundaries(places)
    polygon = bounds.geometry.union_all()
    water = acquire_features(boundary=polygon, tags={"natural": "water"}).data
    water = water[water.geometry.type.isin(["Polygon", "MultiPolygon"])]
    if "name" in water.columns and drop_lakes:
        water = water[~water["name"].isin(drop_lakes)]
    return water.reset_index(drop=True)


def save_layer(gdf: gpd.GeoDataFrame, path: str | Path) -> Path:
    """Write a GeoDataFrame to GeoPackage; coerce list-typed columns to strings."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    out = gdf.copy()
    for col in out.columns:
        if col == "geometry":
            continue
        out[col] = out[col].map(
            lambda value: json.dumps(value) if isinstance(value, (list, dict)) else value
        )
    out.to_file(path, driver="GPKG")
    return path
