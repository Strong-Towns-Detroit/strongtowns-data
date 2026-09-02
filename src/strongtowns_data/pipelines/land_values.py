"""Edge-preserving diagnostics and smoothing for parcel land rates."""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum

import numpy as np
import polars as pl
import pyarrow as pa
import pyarrow.parquet as pq
from sklearn.neighbors import NearestNeighbors

from strongtowns_data.models import BuildMetadata, PipelineContext
from strongtowns_data.pipelines.assessments import allocate_taxable_land


class SmoothingMode(str, Enum):
    OFF = "off"
    ISOLATED_SPIKES = "isolated_spikes"


@dataclass(frozen=True)
class LandValueSmoothing:
    mode: SmoothingMode = SmoothingMode.OFF
    neighbors: int = 12
    outlier_factor: float = 4.0
    peer_similarity_factor: float = 1.5
    minimum_peer_count: int = 2
    minimum_parcel_area_sqft: float = 500.0

    def __post_init__(self) -> None:
        if self.neighbors < 3:
            raise ValueError("neighbors must be at least three")
        if self.outlier_factor <= 1:
            raise ValueError("outlier_factor must exceed one")
        if self.peer_similarity_factor <= 1:
            raise ValueError("peer_similarity_factor must exceed one")
        if not 0 <= self.minimum_peer_count <= self.neighbors:
            raise ValueError("minimum_peer_count must be between zero and neighbors")
        if self.minimum_parcel_area_sqft <= 0:
            raise ValueError("minimum_parcel_area_sqft must be positive")


REQUIRED = {"parcel_id", "land_value", "parcel_area_sqft", "x", "y"}


def _prepared(frame: pl.DataFrame) -> pl.DataFrame:
    missing = REQUIRED - set(frame.columns)
    if missing:
        raise ValueError(f"land-value observations are missing: {sorted(missing)}")
    return frame.with_columns(
        pl.col("parcel_id").cast(pl.String),
        pl.col("land_value").cast(pl.Float64, strict=False),
        pl.col("parcel_area_sqft").cast(pl.Float64, strict=False),
        pl.col("x").cast(pl.Float64, strict=False),
        pl.col("y").cast(pl.Float64, strict=False),
    ).with_columns(
        (pl.col("land_value") / pl.col("parcel_area_sqft")).alias(
            "official_land_rate"
        )
    )


def apply_land_value_smoothing(
    frame: pl.DataFrame,
    *,
    config: LandValueSmoothing = LandValueSmoothing(),
) -> pl.DataFrame:
    """Replace only unsupported spatial spikes when smoothing is enabled.

    A parcel is changed only when it differs from the local median by the
    configured factor and lacks the configured number of similarly valued
    neighbors. Nearby parcels are never separated by an administrative area.
    """
    prepared = _prepared(frame).filter(
        pl.col("official_land_rate").is_finite()
        & (pl.col("official_land_rate") > 0)
        & (pl.col("parcel_area_sqft") >= config.minimum_parcel_area_sqft)
        & pl.col("x").is_finite()
        & pl.col("y").is_finite()
    )
    if len(prepared) <= config.neighbors:
        raise ValueError("not enough valid parcels for the configured neighborhood")

    coordinates = prepared.select("x", "y").to_numpy()
    distances, candidates = NearestNeighbors(
        n_neighbors=config.neighbors + 1, algorithm="kd_tree"
    ).fit(coordinates).kneighbors(coordinates)
    row_numbers = np.arange(len(prepared))
    neighbor_indices = np.empty((len(prepared), config.neighbors), dtype="int64")
    neighbor_distances = np.empty((len(prepared), config.neighbors), dtype="float64")
    for row, (candidate_row, distance_row) in enumerate(zip(candidates, distances)):
        keep = candidate_row != row_numbers[row]
        neighbor_indices[row] = candidate_row[keep][: config.neighbors]
        neighbor_distances[row] = distance_row[keep][: config.neighbors]

    rates = prepared["official_land_rate"].to_numpy()
    neighbor_rates = rates[neighbor_indices]
    local_median = np.median(neighbor_rates, axis=1)
    deviation = np.maximum(rates / local_median, local_median / rates)
    peer_ratios = np.maximum(
        neighbor_rates / rates[:, None], rates[:, None] / neighbor_rates
    )
    peer_count = np.sum(
        peer_ratios <= config.peer_similarity_factor, axis=1
    ).astype("int64")
    candidate_spike = (
        (deviation >= config.outlier_factor)
        & (peer_count < config.minimum_peer_count)
    )
    smoothing_applied = (
        candidate_spike
        if config.mode is SmoothingMode.ISOLATED_SPIKES
        else np.zeros(len(prepared), dtype=bool)
    )
    selected_rate = np.where(smoothing_applied, local_median, rates)
    method = np.where(
        smoothing_applied, "isolated spike replaced", "official value retained"
    )

    return prepared.with_columns(
        pl.Series("local_median_land_rate", local_median),
        pl.Series("local_deviation_factor", deviation),
        pl.Series("local_peer_count", peer_count),
        pl.Series("local_neighbor_distance_m", neighbor_distances[:, -1]),
        pl.Series("isolated_spike_candidate", candidate_spike),
        pl.Series("smoothing_applied", smoothing_applied),
        pl.Series("selected_land_rate", selected_rate),
        pl.Series("land_value_method", method, dtype=pl.String),
    ).with_columns(
        (pl.col("selected_land_rate") * pl.col("parcel_area_sqft")).alias(
            "selected_land_value"
        )
    )


def smoothing_sensitivity(
    diagnostics: pl.DataFrame,
    *,
    factors: tuple[float, ...] = (2.0, 3.0, 4.0),
    minimum_peer_count: int = 2,
) -> dict[str, dict[str, float | int]]:
    """Summarize alternative spike thresholds from one neighbor calculation."""
    result: dict[str, dict[str, float | int]] = {}
    for factor in factors:
        selected = diagnostics.with_columns(
            (
                (pl.col("local_deviation_factor") >= factor)
                & (pl.col("local_peer_count") < minimum_peer_count)
            ).alias("_changed")
        ).with_columns(
            pl.when("_changed")
            .then("local_median_land_rate")
            .otherwise("official_land_rate")
            .alias("_rate")
        )
        summary = selected.select(
            pl.col("_changed").sum().alias("changed"),
            pl.col("land_value").sum().alias("official_land_value"),
            (pl.col("_rate") * pl.col("parcel_area_sqft")).sum().alias(
                "filtered_land_value"
            ),
        ).row(0, named=True)
        result[f"{factor:g}x"] = {
            "changed": int(summary["changed"]),
            "official_land_value": float(summary["official_land_value"]),
            "filtered_land_value": float(summary["filtered_land_value"]),
        }
    return result


def constrain_selected_land_values(frame: pl.DataFrame) -> pl.DataFrame:
    """Keep a selected land component within positive true cash value."""
    return frame.with_columns(
        (
            pl.col("smoothing_applied")
            & (pl.col("selected_land_value") > pl.col("true_cash_value"))
        ).alias("smoothed_land_value_was_capped"),
        pl.when(pl.col("true_cash_value") > 0)
        .then(pl.min_horizontal("selected_land_value", "true_cash_value"))
        .otherwise(None)
        .alias("selected_land_value"),
    ).with_columns(
        (pl.col("selected_land_value") / pl.col("parcel_area_sqft")).alias(
            "selected_land_rate"
        )
    )


def build_parcel_land_values(
    context: PipelineContext,
    *,
    parcels_asset: str,
    assessments_asset: str,
    history_asset: str,
    output_asset: str,
    config: LandValueSmoothing = LandValueSmoothing(
        mode=SmoothingMode.ISOLATED_SPIKES
    ),
) -> dict[str, BuildMetadata]:
    """Store official values beside an optional edge-preserving alternative."""
    import geopandas as gpd

    parcels = gpd.read_parquet(
        context.inputs[parcels_asset] / "accepted.parquet",
        columns=["parcel_id", "geometry"],
    ).to_crs("EPSG:3857")
    points = parcels.geometry.centroid
    coordinates = pl.DataFrame({
        "parcel_id": parcels["parcel_id"].astype(str),
        "x": points.x,
        "y": points.y,
    })
    current = pl.read_parquet(
        context.inputs[assessments_asset] / "accepted.parquet"
    ).join(coordinates, on="parcel_id", how="left")
    history = pl.read_parquet(
        context.inputs[history_asset] / "accepted.parquet"
    ).select(
        "parcel_id", "property_class",
        pl.col("assessed_land_value").alias("land_value"),
    ).join(
        current.select("parcel_id", "parcel_area_sqft", "x", "y"),
        on="parcel_id", how="inner",
    ).filter(pl.col("property_class") == 401)

    history_diagnostics = apply_land_value_smoothing(
        history, config=replace(config, mode=SmoothingMode.OFF)
    )
    current_filtered = apply_land_value_smoothing(current, config=config)
    current_sensitivity = smoothing_sensitivity(
        current_filtered, minimum_peer_count=config.minimum_peer_count
    )
    history_sensitivity = smoothing_sensitivity(
        history_diagnostics, minimum_peer_count=config.minimum_peer_count
    )
    filtered = current_filtered.select(
        "object_id", "local_median_land_rate", "local_deviation_factor",
        "local_peer_count", "local_neighbor_distance_m",
        "isolated_spike_candidate", "smoothing_applied",
        "selected_land_rate", "selected_land_value", "land_value_method",
    )
    result = current.join(filtered, on="object_id", how="left").with_columns(
        pl.when(pl.col("parcel_area_sqft") > 0)
        .then(pl.col("land_value") / pl.col("parcel_area_sqft"))
        .otherwise(None)
        .alias("official_land_rate"),
        pl.col("land_value").alias("official_land_value"),
        pl.when(pl.col("true_cash_value") <= 0)
        .then(pl.lit("invalid true cash value"))
        .when(pl.col("land_value") > pl.col("true_cash_value"))
        .then(pl.lit("land share clipped to one"))
        .otherwise(pl.lit("allocated"))
        .alias("taxable_land_allocation_status"),
    ).with_columns(
        pl.col("smoothing_applied").fill_null(False),
        pl.col("isolated_spike_candidate").fill_null(False),
        pl.col("selected_land_rate").fill_null(pl.col("official_land_rate")),
        pl.col("selected_land_value").fill_null(pl.col("land_value")),
        pl.col("land_value_method").fill_null("official value retained"),
    )
    result = constrain_selected_land_values(result).rename({
        "selected_land_rate": "smoothed_land_rate",
        "selected_land_value": "smoothed_land_value",
    })
    result = result.with_columns(
        pl.Series(
            "official_taxable_land_value",
            allocate_taxable_land(
                result_column(result, "taxable_value"),
                result_column(result, "official_land_value"),
                result_column(result, "true_cash_value"),
            ),
        ),
        pl.Series(
            "smoothed_taxable_land_value",
            allocate_taxable_land(
                result_column(result, "taxable_value"),
                result_column(result, "smoothed_land_value"),
                result_column(result, "true_cash_value"),
            ),
        ),
    ).with_columns(
        pl.col("official_taxable_land_value").fill_nan(None),
        pl.col("smoothed_taxable_land_value").fill_nan(None),
    )

    columns = [
        "object_id", "parcel_id", "assessment_roll_year", "property_class",
        "landmap", "parcel_area_sqft", "true_cash_value", "taxable_value",
        "official_land_rate", "official_land_value",
        "official_taxable_land_value", "smoothed_land_rate",
        "smoothed_land_value", "smoothed_taxable_land_value",
        "taxable_land_allocation_status", "smoothed_land_value_was_capped",
        "local_median_land_rate", "local_deviation_factor",
        "local_peer_count", "local_neighbor_distance_m",
        "isolated_spike_candidate", "smoothing_applied", "land_value_method",
    ]
    table = result.select(columns).to_arrow()
    schema = pa.schema([
        pa.field(
            field.name,
            pa.string() if pa.types.is_large_string(field.type) else field.type,
        )
        for field in table.schema
    ])
    pq.write_table(
        table.cast(schema), context.staging[output_asset] / "accepted.parquet"
    )
    return {output_asset: BuildMetadata(
        counts={
            "records": len(result),
            "eligible": len(current_filtered),
            "smoothing_applied": int(result["smoothing_applied"].sum()),
        },
        parameters={
            "smoothing_mode": config.mode.value,
            "neighbors": config.neighbors,
            "outlier_factor": config.outlier_factor,
            "peer_similarity_factor": config.peer_similarity_factor,
            "minimum_peer_count": config.minimum_peer_count,
            "minimum_parcel_area_sqft": config.minimum_parcel_area_sqft,
            "rule": (
                "replace only a parcel that differs from its local median by "
                "the outlier factor and lacks the minimum similar peers"
            ),
            "current_sensitivity": current_sensitivity,
            "historical_2023_residential_sensitivity": history_sensitivity,
            "taxable_land_allocation": (
                "taxable_value * land_value / true_cash_value, bounded to "
                "taxable_value"
            ),
        },
    )}


def result_column(frame: pl.DataFrame, name: str) -> np.ndarray:
    return frame[name].cast(pl.Float64, strict=False).to_numpy()
