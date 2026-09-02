"""Parcel grocery-access features and an explainable one-feature land model."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any

import numpy as np
import polars as pl
from sklearn.linear_model import HuberRegressor
from sklearn.neighbors import BallTree

EARTH_RADIUS_M = 6_371_008.8


class GroceryScope(str, Enum):
    SUPERMARKETS = "supermarkets"
    FOOD_MARKETS = "food_markets"


def _required(frame: pl.DataFrame, names: set[str], label: str) -> None:
    missing = names - set(frame.columns)
    if missing:
        raise ValueError(f"{label} is missing columns: {sorted(missing)}")


def _category_pairs(value: Any) -> tuple[tuple[str, str], ...]:
    if value is None:
        return ()
    result = []
    for item in value:
        if isinstance(item, dict):
            key, category = item.get("key"), item.get("value")
        else:
            try:
                key, category = item["key"], item["value"]
            except (KeyError, TypeError):
                continue
        if key is not None and category is not None:
            result.append((str(key).lower(), str(category).lower()))
    return tuple(result)


def classify_grocery_pois(
    pois: pl.DataFrame,
    *,
    scope: GroceryScope = GroceryScope.SUPERMARKETS,
) -> pl.DataFrame:
    """Select exact OSM grocery tags without treating convenience stores as groceries."""
    _required(
        pois,
        {"poi_id", "name", "categories", "longitude", "latitude"},
        "POI data",
    )
    accepted = {"supermarket"}
    if scope is GroceryScope.FOOD_MARKETS:
        accepted.update(("grocery", "greengrocer"))

    rows = []
    for row in pois.iter_rows(named=True):
        matches = [
            category
            for key, category in _category_pairs(row["categories"])
            if key == "shop" and category in accepted
        ]
        if matches:
            rows.append({**row, "grocery_kind": matches[0]})
    if not rows:
        return pois.head(0).with_columns(pl.Series("grocery_kind", [], dtype=pl.String))
    return pl.DataFrame(rows, schema_overrides={"grocery_kind": pl.String})


def nearest_grocery_distance(
    parcels: pl.DataFrame,
    groceries: pl.DataFrame,
) -> pl.DataFrame:
    """Attach the nearest grocery and geodesic point-to-point distance in meters."""
    _required(parcels, {"parcel_id", "longitude", "latitude"}, "parcel data")
    _required(
        groceries,
        {"poi_id", "name", "longitude", "latitude"},
        "grocery data",
    )
    if groceries.is_empty():
        raise ValueError("grocery data is empty")
    if parcels["parcel_id"].n_unique() != len(parcels):
        raise ValueError("parcel_id must be unique")

    stores = groceries.sort("poi_id")
    parcel_coordinates = parcels.select("latitude", "longitude").to_numpy()
    store_coordinates = stores.select("latitude", "longitude").to_numpy()
    for label, coordinates in (
        ("parcel", parcel_coordinates),
        ("grocery", store_coordinates),
    ):
        if not np.isfinite(coordinates).all():
            raise ValueError(f"{label} coordinates must be finite")
        if np.any(np.abs(coordinates[:, 0]) > 90):
            raise ValueError(f"{label} latitude is outside [-90, 90]")
        if np.any(np.abs(coordinates[:, 1]) > 180):
            raise ValueError(f"{label} longitude is outside [-180, 180]")

    tree = BallTree(np.deg2rad(store_coordinates), metric="haversine")
    distance, index = tree.query(np.deg2rad(parcel_coordinates), k=1)
    store_index = index[:, 0]
    names = stores["name"].to_list()
    ids = stores["poi_id"].to_list()
    return parcels.with_columns(
        pl.Series("nearest_grocery_id", [ids[i] for i in store_index]),
        pl.Series("nearest_grocery_name", [names[i] for i in store_index]),
        pl.Series(
            "nearest_grocery_distance_m",
            distance[:, 0] * EARTH_RADIUS_M,
        ),
    )


@dataclass(frozen=True)
class GroceryLandModelConfig:
    half_life_candidates_m: tuple[float, ...] = (
        250.0,
        500.0,
        1_000.0,
        2_000.0,
        4_000.0,
        8_000.0,
    )
    spatial_block_size_m: float = 2_500.0
    folds: int = 5
    minimum_observations: int = 100
    huber_epsilon: float = 1.35

    def __post_init__(self) -> None:
        if not self.half_life_candidates_m or any(
            value <= 0 for value in self.half_life_candidates_m
        ):
            raise ValueError("half-life candidates must be positive")
        if self.spatial_block_size_m <= 0:
            raise ValueError("spatial block size must be positive")
        if self.folds < 2:
            raise ValueError("folds must be at least two")
        if self.minimum_observations < 4:
            raise ValueError("minimum observations must be at least four")
        if self.huber_epsilon < 1:
            raise ValueError("Huber epsilon must be at least one")


def _access(distance_m: np.ndarray, half_life_m: float) -> np.ndarray:
    return np.exp2(-distance_m / half_life_m)


def _fit_huber(access: np.ndarray, log_rate: np.ndarray, epsilon: float):
    estimator = HuberRegressor(
        epsilon=epsilon,
        alpha=0.0,
        fit_intercept=True,
        max_iter=1_000,
    ).fit(access.reshape(-1, 1), log_rate)
    return float(estimator.intercept_), float(estimator.coef_[0])


def _spatial_folds(x: np.ndarray, y: np.ndarray, size: float, count: int) -> np.ndarray:
    column = np.floor((x - x.min()) / size).astype("int64")
    row = np.floor((y - y.min()) / size).astype("int64")
    return ((column * 73_856_093) ^ (row * 19_349_663)) % count


@dataclass(frozen=True)
class GroceryLandModel:
    half_life_m: float
    intercept: float
    grocery_coefficient: float
    reference_access: float
    residual_log_lower: float
    residual_log_upper: float
    cross_validated_median_absolute_percentage_error: float
    candidate_cross_validated_mape: dict[str, float]
    half_life_at_search_boundary: bool
    observations: int
    spatial_blocks: int

    def predict(self, frame: pl.DataFrame) -> pl.DataFrame:
        _required(
            frame,
            {"nearest_grocery_distance_m"},
            "grocery-access data",
        )
        distance = frame["nearest_grocery_distance_m"].cast(pl.Float64).to_numpy()
        if np.any(~np.isfinite(distance)) or np.any(distance < 0):
            raise ValueError("grocery distances must be finite and nonnegative")
        access = _access(distance, self.half_life_m)
        prediction = self.intercept + self.grocery_coefficient * access
        relative = self.grocery_coefficient * (access - self.reference_access)
        return frame.with_columns(
            pl.Series("grocery_access", access),
            pl.Series("grocery_only_estimated_land_rate", np.exp(prediction)),
            pl.Series("grocery_association_multiplier", np.exp(relative)),
            pl.Series("grocery_association_percent", 100.0 * np.expm1(relative)),
            pl.Series(
                "grocery_only_prediction_lower",
                np.exp(prediction + self.residual_log_lower),
            ),
            pl.Series(
                "grocery_only_prediction_upper",
                np.exp(prediction + self.residual_log_upper),
            ),
        )

    def parameters(self) -> dict[str, object]:
        return asdict(self)


def fit_grocery_land_model(
    observations: pl.DataFrame,
    *,
    config: GroceryLandModelConfig | None = None,
) -> tuple[GroceryLandModel, pl.DataFrame]:
    """Fit log land rate to grocery access with spatial-block cross-validation."""
    config = config or GroceryLandModelConfig()
    _required(
        observations,
        {
            "parcel_id",
            "land_rate",
            "nearest_grocery_distance_m",
            "x",
            "y",
        },
        "land observations",
    )
    prepared = observations.with_columns(
        pl.col("land_rate").cast(pl.Float64, strict=False),
        pl.col("nearest_grocery_distance_m").cast(pl.Float64, strict=False),
        pl.col("x").cast(pl.Float64, strict=False),
        pl.col("y").cast(pl.Float64, strict=False),
    ).filter(
        pl.col("land_rate").is_finite()
        & (pl.col("land_rate") > 0)
        & pl.col("nearest_grocery_distance_m").is_finite()
        & (pl.col("nearest_grocery_distance_m") >= 0)
        & pl.col("x").is_finite()
        & pl.col("y").is_finite()
    )
    if len(prepared) < config.minimum_observations:
        raise ValueError(f"need at least {config.minimum_observations} valid observations")
    if prepared["parcel_id"].n_unique() != len(prepared):
        raise ValueError("parcel_id must be unique")

    rate = prepared["land_rate"].to_numpy()
    log_rate = np.log(rate)
    distance = prepared["nearest_grocery_distance_m"].to_numpy()
    x = prepared["x"].to_numpy()
    y = prepared["y"].to_numpy()
    fold = _spatial_folds(x, y, config.spatial_block_size_m, config.folds)
    unique_folds = np.unique(fold)
    if len(unique_folds) < 2:
        raise ValueError("observations occupy fewer than two spatial folds")

    scores: dict[float, float] = {}
    predictions: dict[float, np.ndarray] = {}
    for half_life in sorted(set(config.half_life_candidates_m)):
        access = _access(distance, half_life)
        out_of_fold = np.full(len(prepared), np.nan)
        for held_out in unique_folds:
            train = fold != held_out
            test = ~train
            intercept, coefficient = _fit_huber(
                access[train], log_rate[train], config.huber_epsilon
            )
            out_of_fold[test] = intercept + coefficient * access[test]
        if not np.isfinite(out_of_fold).all():
            raise ValueError("spatial validation did not predict every observation")
        scores[half_life] = float(np.median(np.abs(np.exp(out_of_fold) - rate) / rate))
        predictions[half_life] = out_of_fold

    selected_half_life = min(scores, key=lambda value: (scores[value], value))
    access = _access(distance, selected_half_life)
    intercept, coefficient = _fit_huber(access, log_rate, config.huber_epsilon)
    out_of_fold = predictions[selected_half_life]
    residual = log_rate - out_of_fold
    model = GroceryLandModel(
        half_life_m=float(selected_half_life),
        intercept=intercept,
        grocery_coefficient=coefficient,
        reference_access=float(np.median(access)),
        residual_log_lower=float(np.quantile(residual, 0.10)),
        residual_log_upper=float(np.quantile(residual, 0.90)),
        cross_validated_median_absolute_percentage_error=scores[selected_half_life],
        candidate_cross_validated_mape={
            f"{half_life:g}": scores[half_life] for half_life in sorted(scores)
        },
        half_life_at_search_boundary=selected_half_life
        in {
            min(config.half_life_candidates_m),
            max(config.half_life_candidates_m),
        },
        observations=len(prepared),
        spatial_blocks=len(unique_folds),
    )
    result = model.predict(prepared).with_columns(
        pl.Series("spatial_validation_fold", fold),
        pl.Series("out_of_fold_grocery_land_rate", np.exp(out_of_fold)),
        (pl.col("land_rate") / pl.col("grocery_only_estimated_land_rate")).alias(
            "unexplained_land_rate_multiplier"
        ),
    )
    return model, result
