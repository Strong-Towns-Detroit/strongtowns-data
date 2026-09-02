import geopandas as gpd
import pandas as pd
import pytest
from shapely.geometry import Point, Polygon

from strongtowns_data.pois.osm import normalize_osm_pois


def test_normalize_osm_pois_preserves_identity_tags_and_point_geometry():
    index = pd.MultiIndex.from_tuples([("node", 100), ("way", 200)], names=("element", "id"))
    raw = gpd.GeoDataFrame(
        {
            "name": ["Market", "Cafe"],
            "shop": ["supermarket", None],
            "amenity": [None, "cafe"],
            "geometry": [
                Point(-83.05, 42.33),
                Polygon(
                    [
                        (-83.04, 42.33),
                        (-83.039, 42.33),
                        (-83.039, 42.331),
                        (-83.04, 42.331),
                    ]
                ),
            ],
        },
        index=index,
        crs="EPSG:4326",
    )

    result = normalize_osm_pois(raw)

    assert list(result.poi_id) == ["osm:node:100", "osm:way:200"]
    assert list(result.primary_category) == ["shop", "amenity"]
    assert list(result.category_value) == ["supermarket", "cafe"]
    assert result.geometry.geom_type.tolist() == ["Point", "Point"]
    assert '"shop": "supermarket"' in result.iloc[0].source_tags_json


def test_normalize_requires_source_crs():
    raw = gpd.GeoDataFrame({"geometry": [Point(0, 0)]})
    with pytest.raises(ValueError, match="CRS"):
        normalize_osm_pois(raw)
