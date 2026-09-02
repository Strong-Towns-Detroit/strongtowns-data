from __future__ import annotations

import numpy as np
import polars as pl
import pytest

from strongtowns_data.pipelines.grocery_access import (
    GroceryLandModelConfig,
    GroceryScope,
    classify_grocery_pois,
    fit_grocery_land_model,
    nearest_grocery_distance,
)


def poi_frame() -> pl.DataFrame:
    return pl.DataFrame(
        {
            "poi_id": ["market", "small", "produce", "corner"],
            "name": ["Market", "Small Market", "Produce", "Corner"],
            "categories": [
                [{"key": "shop", "value": "supermarket"}],
                [{"key": "shop", "value": "grocery"}],
                [{"key": "shop", "value": "greengrocer"}],
                [{"key": "shop", "value": "convenience"}],
            ],
            "longitude": [-83.0, -83.1, -83.2, -83.3],
            "latitude": [42.3, 42.3, 42.3, 42.3],
        }
    )


def test_default_grocery_definition_is_supermarkets_only():
    result = classify_grocery_pois(poi_frame())
    assert result["poi_id"].to_list() == ["market"]
    assert result["grocery_kind"].to_list() == ["supermarket"]


def test_food_market_scope_includes_explicit_food_shops_not_convenience():
    result = classify_grocery_pois(poi_frame(), scope=GroceryScope.FOOD_MARKETS)
    assert result["poi_id"].to_list() == ["market", "small", "produce"]
    assert "corner" not in result["poi_id"].to_list()


def test_nearest_distance_retains_store_identity_and_is_geodesic():
    parcels = pl.DataFrame(
        {
            "parcel_id": ["one", "two"],
            "longitude": [-83.0, -83.1],
            "latitude": [42.3, 42.3],
        }
    )
    groceries = classify_grocery_pois(poi_frame()).vstack(
        pl.DataFrame(
            {
                "poi_id": ["west"],
                "name": ["West Market"],
                "categories": [[{"key": "shop", "value": "supermarket"}]],
                "longitude": [-83.1],
                "latitude": [42.3],
                "grocery_kind": ["supermarket"],
            }
        )
    )
    result = nearest_grocery_distance(parcels, groceries)
    assert result["nearest_grocery_id"].to_list() == ["market", "west"]
    assert result["nearest_grocery_distance_m"].to_list() == pytest.approx([0.0, 0.0], abs=0.01)


def test_nearest_distance_rejects_duplicate_parcels_and_bad_coordinates():
    groceries = classify_grocery_pois(poi_frame())
    duplicate = pl.DataFrame(
        {
            "parcel_id": ["one", "one"],
            "longitude": [-83.0, -83.1],
            "latitude": [42.3, 42.3],
        }
    )
    with pytest.raises(ValueError, match="unique"):
        nearest_grocery_distance(duplicate, groceries)
    bad = pl.DataFrame({"parcel_id": ["one"], "longitude": [-83.0], "latitude": [142.3]})
    with pytest.raises(ValueError, match="latitude"):
        nearest_grocery_distance(bad, groceries)


def synthetic_observations() -> pl.DataFrame:
    rows = []
    for row in range(8):
        for column in range(8):
            distance = 150.0 + column * 550.0 + row * 25.0
            access = 2.0 ** (-distance / 1_000.0)
            noise = 0.025 if (row + column) % 2 else -0.025
            rate = np.exp(1.2 + 0.7 * access + noise)
            rows.append(
                {
                    "parcel_id": f"{row}-{column}",
                    "land_rate": rate,
                    "nearest_grocery_distance_m": distance,
                    "x": column * 1_000.0,
                    "y": row * 1_000.0,
                }
            )
    return pl.DataFrame(rows)


def test_model_separates_grocery_effect_from_unexplained_value():
    model, result = fit_grocery_land_model(
        synthetic_observations(),
        config=GroceryLandModelConfig(
            half_life_candidates_m=(500.0, 1_000.0, 2_000.0),
            spatial_block_size_m=1_000.0,
            folds=4,
            minimum_observations=20,
        ),
    )
    assert model.grocery_coefficient > 0
    assert model.cross_validated_median_absolute_percentage_error < 0.05
    assert model.observations == 64
    assert model.spatial_blocks >= 2
    near = result.sort("nearest_grocery_distance_m").row(0, named=True)
    far = result.sort("nearest_grocery_distance_m").row(-1, named=True)
    assert near["grocery_only_estimated_land_rate"] > far["grocery_only_estimated_land_rate"]
    assert near["grocery_association_percent"] > far["grocery_association_percent"]
    assert result["unexplained_land_rate_multiplier"].is_finite().all()
    assert model.parameters()["half_life_m"] in (500.0, 1_000.0, 2_000.0)
    assert set(model.candidate_cross_validated_mape) == {"500", "1000", "2000"}


def test_model_requires_enough_observations_and_spatial_separation():
    config = GroceryLandModelConfig(minimum_observations=20)
    with pytest.raises(ValueError, match="at least 20"):
        fit_grocery_land_model(synthetic_observations().head(10), config=config)
    one_location = synthetic_observations().with_columns(
        pl.lit(0.0).alias("x"), pl.lit(0.0).alias("y")
    )
    with pytest.raises(ValueError, match="spatial folds"):
        fit_grocery_land_model(one_location, config=config)
