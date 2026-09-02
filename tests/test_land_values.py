from __future__ import annotations

import polars as pl
import pytest

from strongtowns_data.pipelines.land_values import (
    LandValueSmoothing,
    SmoothingMode,
    apply_land_value_smoothing,
    constrain_selected_land_values,
    smoothing_sensitivity,
)


def observations(rates: list[float]) -> pl.DataFrame:
    return pl.DataFrame({
        "parcel_id": [str(index) for index in range(len(rates))],
        "land_value": [rate * 1_000 for rate in rates],
        "parcel_area_sqft": [1_000.0] * len(rates),
        "x": [float(index) for index in range(len(rates))],
        "y": [0.0] * len(rates),
    })


def config(mode=SmoothingMode.ISOLATED_SPIKES, **updates):
    values = {
        "mode": mode,
        "neighbors": 6,
        "outlier_factor": 4,
        "peer_similarity_factor": 1.5,
        "minimum_peer_count": 2,
    }
    values.update(updates)
    return LandValueSmoothing(**values)


def test_isolated_spike_is_replaced_by_local_median():
    frame = observations([1, 1, 1, 1, 1, 20, 1, 1, 1, 1, 1])
    result = apply_land_value_smoothing(frame, config=config())
    spike = result.filter(pl.col("parcel_id") == "5").row(0, named=True)
    assert spike["isolated_spike_candidate"] is True
    assert spike["smoothing_applied"] is True
    assert spike["local_peer_count"] == 0
    assert spike["selected_land_rate"] == 1


def test_toggle_off_retains_an_identified_spike():
    frame = observations([1, 1, 1, 1, 1, 20, 1, 1, 1, 1, 1])
    result = apply_land_value_smoothing(
        frame, config=config(SmoothingMode.OFF)
    )
    spike = result.filter(pl.col("parcel_id") == "5").row(0, named=True)
    assert spike["isolated_spike_candidate"] is True
    assert spike["smoothing_applied"] is False
    assert spike["selected_land_rate"] == 20


def test_shared_cliff_and_plateaus_are_preserved():
    frame = observations([1, 1, 1, 1, 1, 10, 10, 10, 10, 10, 10, 10])
    result = apply_land_value_smoothing(frame, config=config())
    assert result["smoothing_applied"].sum() == 0
    assert result["selected_land_rate"].to_list() == [
        1, 1, 1, 1, 1, 10, 10, 10, 10, 10, 10, 10
    ]


def test_three_parcel_plateau_has_enough_peer_support():
    frame = observations([1, 1, 1, 1, 10, 10, 10, 1, 1, 1, 1])
    result = apply_land_value_smoothing(frame, config=config())
    plateau = result.filter(pl.col("parcel_id").is_in(["4", "5", "6"]))
    assert plateau["smoothing_applied"].sum() == 0
    assert plateau["local_peer_count"].min() >= 2


def test_sensitivity_reuses_diagnostics_for_multiple_thresholds():
    frame = observations([1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1])
    diagnostics = apply_land_value_smoothing(
        frame, config=config(SmoothingMode.OFF)
    )
    result = smoothing_sensitivity(diagnostics)
    assert result["2x"]["changed"] == 1
    assert result["3x"]["changed"] == 1
    assert result["4x"]["changed"] == 0


def test_constraint_caps_only_selected_land_and_preserves_missing_cash_value():
    frame = pl.DataFrame({
        "selected_land_value": [120.0, 80.0, 10.0],
        "true_cash_value": [100.0, 100.0, 0.0],
        "parcel_area_sqft": [10.0, 10.0, 10.0],
        "smoothing_applied": [True, False, True],
    })
    result = constrain_selected_land_values(frame)
    assert result["selected_land_value"].to_list() == [100.0, 80.0, None]
    assert result["selected_land_rate"].to_list() == [10.0, 8.0, None]
    assert result["smoothed_land_value_was_capped"].to_list() == [
        True, False, True
    ]


def test_configuration_rejects_invalid_free_parameters():
    with pytest.raises(ValueError, match="neighbors"):
        LandValueSmoothing(neighbors=2)
    with pytest.raises(ValueError, match="outlier_factor"):
        LandValueSmoothing(outlier_factor=1)
    with pytest.raises(ValueError, match="minimum_peer_count"):
        LandValueSmoothing(neighbors=4, minimum_peer_count=5)
