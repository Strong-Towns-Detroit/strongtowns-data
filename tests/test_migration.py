import geopandas as gpd
import pandas as pd
import pytest
from shapely.geometry import Point

from krabby_real_estate.data import migration


def test_migration_gate_detects_count_regression(tmp_path, monkeypatch):
    current = gpd.GeoDataFrame(
        {
            "parcel_key": ["1"],
            "street_id": ["2"],
            "routing_anchor_method": ["nearest_street_front_edge_midpoint"],
            "frontage_source": ["nearest_base_units_street"],
        },
        geometry=[Point(-83, 42)],
        crs="EPSG:4326",
    )
    dispositions = pd.DataFrame([{"anchor_uuid": "a", "review_status": "required"}])
    monkeypatch.setattr(gpd, "read_file", lambda *_args, **_kwargs: current.copy())
    with pytest.raises(ValueError, match="migration gates failed"):
        migration.validate_anchor_migration(current, dispositions, tmp_path / "legacy.gpkg")
