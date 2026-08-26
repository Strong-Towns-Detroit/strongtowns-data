import geopandas as gpd
from shapely.geometry import LineString, Point, box

from krabby_real_estate.base_units.anchors import build_parcel_routing_anchors


def fixture_layers():
    parcels = gpd.GeoDataFrame(
        {"parcel_id": ["A.", "B.", "C."]},
        geometry=[box(0, 20, 30, 120), box(40, 20, 70, 120), box(80, 20, 110, 120)],
        crs="EPSG:2898",
    )
    addresses = gpd.GeoDataFrame(
        {
            "objectid": [10, 30, 31],
            "parcel_id": ["A", "C", "C"],
            # Nullable ArcGIS numeric fields are commonly inferred as floats in GeoJSON.
            "street_id": [1.0, 1.0, 2.0],
        },
        geometry=[Point(10, 40), Point(90, 40), Point(100, 80)],
        crs="EPSG:2898",
    )
    streets = gpd.GeoDataFrame(
        {"street_id": [1, 2]},
        geometry=[LineString([(-100, 0), (200, 0)]), LineString([(130, 0), (130, 200)])],
        crs="EPSG:2898",
    )
    buildings = gpd.GeoDataFrame(
        {"building_id": [100], "parcel_id": ["A"], "status": ["Current"]},
        geometry=[box(5, 40, 25, 80)],
        crs="EPSG:2898",
    )
    return parcels, addresses, streets, buildings


def test_builds_linked_fallback_and_multiple_street_anchors():
    parcels, addresses, streets, buildings = fixture_layers()
    anchors, edges, summary = build_parcel_routing_anchors(
        parcels, addresses, streets, buildings=buildings
    )

    assert len(anchors) == 4
    assert len(edges) == 4
    assert anchors.groupby("parcel_key").size().to_dict() == {"A": 1, "B": 1, "C": 2}
    assert summary["parcel_count"] == 3
    assert summary["parcel_count_with_anchor"] == 3
    assert summary["multi_anchor_parcel_count"] == 1
    assert summary["unanchored_parcel_count"] == 0

    linked = anchors[anchors.parcel_key.eq("A")].iloc[0]
    assert linked.routing_anchor_method == "address_linked_front_edge_projection"
    assert linked.frontage_source == "base_units_address_link"
    assert linked.anchor_confidence == "high"
    assert linked.linked_current_building_count == 1
    assert linked.address_objectids_json == '["10"]'

    fallback = anchors[anchors.parcel_key.eq("B")].iloc[0]
    assert fallback.routing_anchor_method == "nearest_street_front_edge_midpoint"
    assert fallback.frontage_source == "nearest_base_units_street"
    assert fallback.anchor_confidence == "low"


def test_requires_declared_relationship_columns():
    parcels, addresses, streets, _buildings = fixture_layers()
    addresses = addresses.drop(columns="street_id")
    try:
        build_parcel_routing_anchors(parcels, addresses, streets)
    except ValueError as error:
        assert "street_id" in str(error)
    else:
        raise AssertionError("missing street_id should fail")


def test_rejects_duplicate_normalized_parcel_ids_instead_of_dropping_one():
    parcels, addresses, streets, _buildings = fixture_layers()
    parcels.loc[1, "parcel_id"] = "A"
    try:
        build_parcel_routing_anchors(parcels, addresses, streets)
    except ValueError as error:
        assert "duplicate normalized parcel identifiers" in str(error)
    else:
        raise AssertionError("duplicate normalized parcel identifiers should fail")
