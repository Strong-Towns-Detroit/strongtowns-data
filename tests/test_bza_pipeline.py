"""Offline pipeline integrity and migration regressions."""

import io
import json
from pathlib import Path

import geopandas as gpd
import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from strongtowns_data import bza
from strongtowns_data.bza import _cache
from strongtowns_data.bza._pipeline.build import build, package
from strongtowns_data.bza._pipeline.merge_cases import run as merge
from strongtowns_data.bza._pipeline.minutes import download_bza_minutes
from tests.test_bza_sdk import bundle


def test_bad_evidence_fails_instead_of_silently_skipping(tmp_path):
    (tmp_path / "per_doc").mkdir()
    path = tmp_path / "per_doc/bad.json"
    for content in ("broken", "{}", "[1]"):
        path.write_text(content)
        with pytest.raises(ValueError):
            merge(tmp_path)
        assert not (tmp_path / "all_cases.csv").exists()


def test_minutes_preview_never_uses_network_or_writes(tmp_path, monkeypatch):
    monkeypatch.setattr("requests.Session", lambda: pytest.fail("preview used network"))
    path = tmp_path / "source"
    assert download_bza_minutes(path)["applied"] is False
    assert not path.exists()


def test_package_fetch_round_trip(tmp_path, monkeypatch):
    source, _ = bundle(tmp_path)
    (source / "release_audit.json").write_text(
        json.dumps({"counts": {"cases": 2, "hearings": 3}})
    )
    archive = package(
        source,
        tmp_path / "release",
        version="new",
        release_url="https://example.org/new.zip",
    )
    index = json.loads((archive.parent / "bza-index.json").read_text())

    def request(url, timeout):
        return io.BytesIO(
            json.dumps(index).encode()
            if url.endswith("bza-index.json")
            else archive.read_bytes()
        )

    monkeypatch.setattr(_cache, "https_open", request)
    selected = bza.open(cache=tmp_path / "cache")
    assert selected.manifest["version"] == "new"
    assert len(selected.cases()) == 2
    assert len(selected.hearings()) == 3
    assert json.loads((source / "bza-manifest.json").read_text())["version"] == "v1"


def test_paid_operations_require_explicit_authorization(tmp_path):
    pytest.importorskip("pydantic")
    from strongtowns_data.bza._pipeline.classify_bza_project_types_with_gemini import (
        run as classify,
    )
    from strongtowns_data.bza._pipeline.extract_bza_with_gemini import run as extract

    with pytest.raises(ValueError, match="allow_paid"):
        extract(pdf_dir=tmp_path, output_dir=tmp_path / "output", dry_run=False)
    with pytest.raises(ValueError, match="allow_paid"):
        classify(
            histories_path=tmp_path / "missing.csv",
            output_dir=tmp_path / "output",
            dry_run=False,
        )
    assert not (tmp_path / "output").exists()


def test_extraction_fingerprint_reuses_legacy_and_detects_changes(
    tmp_path, monkeypatch, capsys
):
    pytest.importorskip("pydantic")
    from strongtowns_data.bza._pipeline.extract_bza_with_gemini import run

    source = tmp_path / "pdf"
    source.mkdir()
    (source / "2025-01-01.pdf").write_bytes(b"%PDF fixture")
    out = tmp_path / "evidence"
    (out / "per_doc").mkdir(parents=True)
    (out / "per_doc/2025-01-01_cases.json").write_text("[]")
    run(pdf_dir=source, output_dir=out, dry_run=True)
    assert "0 document(s)" in capsys.readouterr().out
    (out / "fingerprints").mkdir()
    (out / "fingerprints/2025-01-01.json").write_text("{}")
    run(pdf_dir=source, output_dir=out, dry_run=True)
    assert "1 document(s)" in capsys.readouterr().out


def test_pinned_baseline_unchanged(tmp_path):
    root = Path(__file__).resolve().parents[1]
    source = (
        root
        / "data/datasets/detroit-bza-gemini-source/snapshots/2026-08-26_6233c2f2-1019-4ef7-b68b-961f054c12c0/raw"
    )
    if not source.exists():
        pytest.skip("Pinned historical evidence not materialized")
    audit = build(source, tmp_path / "built", reviews=root / "resources/bza")
    assert audit["counts"] == {"cases": 405, "hearings": 496}
    for name in (
        "all_cases.csv",
        "case_histories.csv",
        "case_occurrences.csv",
        "case_categories.csv",
        "atlas_category_summary.csv",
    ):
        assert_frame_equal(
            pd.read_csv(source / name), pd.read_csv(tmp_path / "built" / name)
        )
    before = gpd.read_file(source / "atlas_category_sites.gpkg")
    after = gpd.read_file(tmp_path / "built/atlas_category_sites.gpkg")
    assert_frame_equal(before.drop(columns="geometry"), after.drop(columns="geometry"))
    assert before.geometry.geom_equals(after.geometry).all()
    assert audit["review_files"]
    assert not (root / "resources/bza/site_review_suggestions.csv").exists()


def test_missing_enrichment_keeps_all_cases(tmp_path):
    # Exercise real build against the pinned source with only extraction evidence.
    root = Path(__file__).resolve().parents[1]
    source = (
        root
        / "data/datasets/detroit-bza-gemini-source/snapshots/2026-08-26_6233c2f2-1019-4ef7-b68b-961f054c12c0/raw"
    )
    if not source.exists():
        pytest.skip("Pinned historical evidence not materialized")
    import shutil

    minimal = tmp_path / "source"
    minimal.mkdir()
    for name in ("all_cases.csv", "all_cases.json"):
        shutil.copyfile(source / name, minimal / name)
    audit = build(minimal, tmp_path / "built", reviews=root / "resources/bza")
    assert audit["counts"]["cases"] == 405
    assert len(audit["enrichment"]["sites"]["unmatched_case_ids"]) == 405
    assert audit["enrichment"]["intake_dates"]["status"] == "unavailable"
    assert len(bza.open(directory=tmp_path / "built").cases()) == 405
    summary = pd.read_csv(tmp_path / "built/atlas_category_summary.csv")
    assert not summary.publication_eligible.any()


def test_extraction_writes_only_explicit_output_and_reuses_cache(tmp_path, monkeypatch):
    pytest.importorskip("google.genai")
    from google import genai

    from strongtowns_data.bza._pipeline import extract_bza_with_gemini as extractor

    monkeypatch.setenv("GEMINI_API_KEY", "unit-test-not-a-real-key")
    monkeypatch.setattr(genai, "Client", lambda **kwargs: object())
    calls = []

    def extract(client, pdf, model, attempts, raw_dir):
        calls.append((pdf, model, raw_dir))
        return extractor.Extraction(meeting_date="2025-01-01", cases=[])

    monkeypatch.setattr(extractor, "extract_one", extract)
    source = tmp_path / "pdf"
    source.mkdir()
    (source / "January_1_2025.pdf").write_bytes(b"%PDF fixture")
    output = tmp_path / "selected-output"
    options = dict(pdf_dir=source, output_dir=output, dry_run=False, allow_paid=True)
    assert extractor.run(**options) == 0
    assert (output / "per_doc/January_1_2025_cases.json").exists()
    assert json.loads((output / "gemini_manifest.jsonl").read_text())["source_sha256"]
    assert extractor.run(**options) == 0
    assert len(calls) == 1
    assert extractor.run(model="changed-model", **options) == 0
    assert len(calls) == 2
    assert calls[-1][2] == output / "gemini_raw"


def test_project_classification_resume_and_explicit_paths(tmp_path, monkeypatch):
    pytest.importorskip("pydantic")
    from strongtowns_data.bza._pipeline import (
        classify_bza_project_types_with_gemini as module,
    )

    source, _ = bundle(tmp_path)
    histories = pd.read_csv(source / "case_histories.csv")
    histories["first_meeting_date"] = "2025-01-01"
    histories.to_csv(source / "case_histories.csv", index=False)
    monkeypatch.setenv("GEMINI_API_KEY", "unit-test-not-a-real-key")
    calls = []

    def classify(rows, model, attempts, raw_dir):
        calls.append(rows)
        return [
            module.ProjectClassification(
                case_history_id=r["case_history_id"],
                project_type_family="housing",
                project_type_label="duplex",
                proposed_action="new_construction",
                intensity_direction="adds_homes_or_activity",
                urban_form_orientation="mixed_or_neutral",
                proposal_language_tone="neutral",
                summary="test",
                confidence="high",
            )
            for r in rows
        ]

    monkeypatch.setattr(module, "classify_batch", classify)
    output = tmp_path / "selected-project-output"
    options = dict(
        histories_path=source / "case_histories.csv",
        output_dir=output,
        all=True,
        dry_run=False,
        allow_paid=True,
    )
    assert module.run(**options) == 0
    assert len(pd.read_csv(output / "project_types.csv")) == 2
    assert module.run(**options) == 0
    assert len(calls) == 1
    assert module.run(model="changed-model", **options) == 0
    assert len(calls) == 2
