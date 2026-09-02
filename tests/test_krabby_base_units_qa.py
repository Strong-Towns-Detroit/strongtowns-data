import geopandas as gpd
import pandas as pd
from shapely.geometry import Point

from strongtowns_data.base_units.qa import audit_anchors, audit_source_relations


def test_audit_source_relations_distinguishes_missing_and_broken_links():
    parcels = pd.DataFrame({"parcel_id": ["A.", "B."]})
    streets = pd.DataFrame({"street_id": [1, 2]})
    addresses = pd.DataFrame(
        {
            "parcel_id": ["A", "MISSING", None, "B"],
            "street_id": [1.0, 1.0, 2.0, None],
        }
    )
    report = audit_source_relations(parcels, addresses, streets)
    assert report["usable_address_relation_count"] == 1
    assert report["address_parcel_not_current_count"] == 1
    assert report["address_missing_parcel_id_count"] == 1
    assert report["address_missing_street_id_count"] == 1
    assert report["parcel_without_usable_address_relation_count"] == 1


def test_audit_anchors_flags_fallback_distance_confidence_and_multiple_anchors():
    anchors = gpd.GeoDataFrame(
        {
            "parcel_key": ["A", "B", "B"],
            "anchor_id": ["a", "b1", "b2"],
            "routing_anchor_method": [
                "nearest_street_front_edge_midpoint",
                "address_linked_front_edge_projection",
                "address_linked_front_edge_projection",
            ],
            "anchor_confidence": ["low", "high", "medium"],
            "edge_to_street_distance_ft": [100.0, 10.0, 20.0],
            "angle_difference_degrees": [5.0, 2.0, 20.0],
        },
        geometry=[Point(0, 0), Point(1, 1), Point(2, 2)],
        crs="EPSG:4326",
    )
    report, review = audit_anchors(anchors)
    assert report["multi_anchor_parcel_count"] == 1
    assert report["review_reason_counts"]["nearest_street_fallback"] == 1
    assert report["review_reason_counts"]["street_distance_over_80ft"] == 1
    assert len(review) == 3
