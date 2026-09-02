from __future__ import annotations

import json

import numpy as np
import pyarrow.parquet as pq

from strongtowns_data.models import PipelineContext
from strongtowns_data.pipelines.assessments import (
    ASSESSMENT_COLUMNS,
    allocate_taxable_land,
    canonical_assessment_builder,
    canonical_lvt_2023_builder,
)


def _properties(**updates):
    values = {name: None for name in ASSESSMENT_COLUMNS}
    values.update({
        "ObjectId": 1,
        "parcel_id": "01000001. ",
        "amt_assessed_value": 50_000,
        "amt_taxable_value": 30_000,
        "amt_estimated_true_cash_value": 100_000,
        "amt_land_value": 20_000,
        "total_square_footage": 5_000,
        "landmap": "004",
    })
    values.update(updates)
    return values


def test_assessment_builder_preserves_records_and_types(tmp_path):
    raw = tmp_path / "raw"
    output = tmp_path / "output"
    raw.mkdir()
    output.mkdir()
    payload = {
        "type": "FeatureCollection",
        "features": [
            {"type": "Feature", "properties": _properties(), "geometry": None},
            {
                "type": "Feature",
                "properties": _properties(ObjectId=2, parcel_id="01000002."),
                "geometry": None,
            },
        ],
    }
    (raw / "raw.geojson").write_text(json.dumps(payload))
    builder = canonical_assessment_builder(
        input_asset="raw", output_asset="output", roll_year=2026
    )
    metadata = builder(PipelineContext(
        tmp_path, "test", {"raw": raw}, {"raw": {}}, {"output": output}
    ))["output"]
    result = pq.read_table(output / "accepted.parquet")
    assert metadata.counts == {"input": 2, "accepted": 2, "rejected": 0}
    assert result.schema.field("object_id").type.bit_width == 64
    assert result.schema.field("land_value").type.bit_width == 64
    assert result.column("parcel_id").to_pylist() == ["01000001.", "01000002."]


def test_assessment_builder_quarantines_bad_identity_and_values(tmp_path):
    raw = tmp_path / "raw"
    output = tmp_path / "output"
    raw.mkdir()
    output.mkdir()
    payload = {
        "type": "FeatureCollection",
        "features": [
            {"type": "Feature", "properties": _properties(), "geometry": None},
            {"type": "Feature", "properties": _properties(ObjectId=1), "geometry": None},
            {
                "type": "Feature",
                "properties": _properties(ObjectId=3, amt_land_value=-1),
                "geometry": None,
            },
        ],
    }
    (raw / "raw.geojson").write_text(json.dumps(payload))
    builder = canonical_assessment_builder(
        input_asset="raw", output_asset="output", roll_year=2026
    )
    metadata = builder(PipelineContext(
        tmp_path, "test", {"raw": raw}, {"raw": {}}, {"output": output}
    ))["output"]
    rejected = pq.read_table(output / "rejects.parquet")
    assert metadata.counts == {"input": 3, "accepted": 1, "rejected": 2}
    assert rejected.column("reason").to_pylist() == [
        "duplicate_object_id", "invalid_land_value"
    ]


def test_taxable_land_allocation_is_proportional_and_bounded():
    result = allocate_taxable_land(
        np.array([30_000, 100, 20, 20]),
        np.array([20_000, 200, 5, 5]),
        np.array([100_000, 100, 0, np.nan]),
    )
    assert result[0] == 6_000
    assert result[1] == 100
    assert np.isnan(result[2])
    assert np.isnan(result[3])


def test_lvt_2023_builder_preserves_city_observations(tmp_path):
    raw = tmp_path / "raw"
    output = tmp_path / "output"
    raw.mkdir()
    output.mkdir()
    (raw / "raw.csv").write_text(
        "ObjectId,parcel_num,property_class,a_tv,land_value,tv_land,tax_classification\n"
        "1,01000001.,401,10000,2000,1250,AD VALOREM\n"
    )
    builder = canonical_lvt_2023_builder(
        input_asset="raw", output_asset="output"
    )
    metadata = builder(PipelineContext(
        tmp_path, "test", {"raw": raw}, {"raw": {}}, {"output": output}
    ))["output"]
    result = pq.read_table(output / "accepted.parquet")
    assert metadata.counts == {"input": 1, "accepted": 1, "rejected": 0}
    assert result.column("assessed_land_value").to_pylist() == [2000.0]
    assert result.column("taxable_land_value").to_pylist() == [1250.0]
