"""Neighborhood acquisition uses the city source and standard snapshot metadata."""

from types import SimpleNamespace

from strongtowns_data.models import AcquisitionPolicy
from strongtowns_data.pipelines import builtin


def test_neighborhood_source_records_city_endpoint_and_count(tmp_path, monkeypatch):
    calls = []

    def collect(endpoint, destination, **kwargs):
        calls.append((endpoint, destination))
        return SimpleNamespace(
            feature_count=208, cache_fingerprint="test-fingerprint",
            before={"object_id_count": 208}, after={"object_id_count": 208},
            started_at="2026-10-26T00:00:00Z", completed_at="2026-10-26T00:00:01Z",
        )

    monkeypatch.setattr(builtin, "collect_layer", collect)
    pipeline = builtin.detroit_neighborhoods_source()
    assert pipeline.acquisition_policy is AcquisitionPolicy.PUBLIC_NETWORK
    assert pipeline.inputs == ()
    context = SimpleNamespace(root=tmp_path, staging={"detroit.neighborhoods.raw": tmp_path})
    result = pipeline.fetch(context)["detroit.neighborhoods.raw"]
    endpoint, destination = calls[0]
    assert endpoint.endswith("Current_City_of_Detroit_Neighborhoods/FeatureServer/0")
    assert "qvkbeam7Wirps6zC" in endpoint
    assert destination == tmp_path / "raw.geojson"
    assert result.counts == {"records": 208}
    assert result.source["url"] == endpoint
