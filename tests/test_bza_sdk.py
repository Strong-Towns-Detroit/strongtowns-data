"""Prepared-data access: offline queries, release integrity, and update UX."""

import hashlib
import io
import json
import zipfile

import pandas as pd
import pytest

from strongtowns_data import bza
from strongtowns_data.bza import _cache


def bundle(tmp_path, version="v1", end="2025-09-20"):
    root = tmp_path / version
    root.mkdir()
    pd.DataFrame(
        [
            dict(
                case_history_id="a",
                printed_case_number="01-25",
                location="Main Street",
                proposal="Relocate house with side setback relief",
                relief_categories="setbacks_yards|lot_dimensions",
                final_outcome="granted_reversed",
            ),
            dict(
                case_history_id="b",
                printed_case_number="01-25",
                location="Other Street",
                proposal="Build duplex",
                relief_categories="lot_dimensions",
                final_outcome="denied_upheld",
            ),
        ]
    ).to_csv(root / "case_histories.csv", index=False)
    pd.DataFrame(
        [
            dict(
                occurrence_id="1",
                case_history_id="a",
                meeting_date="2025-01-01",
                source_file="one.pdf",
                decision="Continued",
            ),
            dict(
                occurrence_id="2",
                case_history_id="a",
                meeting_date=end,
                source_file="two.pdf",
                decision="Granted",
            ),
            dict(
                occurrence_id="3",
                case_history_id="b",
                meeting_date=end,
                source_file="two.pdf",
                decision="Denied",
            ),
        ]
    ).to_csv(root / "case_occurrences.csv", index=False)
    pd.DataFrame(
        [
            dict(case_history_id="a", category="setbacks_yards"),
            dict(case_history_id="b", category="lot_dimensions"),
        ]
    ).to_csv(root / "case_categories.csv", index=False)
    project = root / "project_type_enrichment"
    project.mkdir()
    pd.DataFrame(
        [
            dict(
                case_history_id="a",
                project_type_label="single-family dwelling",
                project_type_family="housing",
            ),
            dict(
                case_history_id="b",
                project_type_label="duplex",
                project_type_family="housing",
            ),
        ]
    ).to_csv(project / "case_histories_with_project_types.csv", index=False)
    manifest = dict(
        version=version,
        schema_version=1,
        coverage_start="2025-01-01",
        coverage_end=end,
        files={
            str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in root.rglob("*.csv")
        },
    )
    (root / "bza-manifest.json").write_text(json.dumps(manifest))
    return root, manifest


def release(root, manifest):
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w") as archive:
        for path in root.rglob("*"):
            if path.is_file():
                archive.write(path, path.relative_to(root))
    data = stream.getvalue()
    item = {
        k: manifest[k]
        for k in ("version", "schema_version", "coverage_start", "coverage_end")
    }
    item.update(
        url=f"https://example.org/{manifest['version']}.zip",
        sha256=hashlib.sha256(data).hexdigest(),
    )
    return item, data


def server(monkeypatch, releases):
    calls = []

    def request(url, timeout):
        calls.append((url, timeout))
        if url.endswith("bza-index.json"):
            return io.BytesIO(
                json.dumps({"releases": [r for r, d in releases]}).encode()
            )
        return io.BytesIO(next(d for r, d in releases if r["url"] == url))

    monkeypatch.setattr(_cache, "https_open", request)
    return calls


def test_queries_export_and_evidence(tmp_path, monkeypatch):
    root, _ = bundle(tmp_path)
    monkeypatch.setattr(
        _cache, "https_open", lambda *a: pytest.fail("local access used network")
    )
    (root / "reviews").mkdir()
    pd.DataFrame([{"occurrence_id": "1", "note": "Reviewed correction"}]).to_csv(
        root / "reviews/history.csv", index=False
    )
    manifest = json.loads((root / "bza-manifest.json").read_text())
    manifest["files"]["reviews/history.csv"] = hashlib.sha256(
        (root / "reviews/history.csv").read_bytes()
    ).hexdigest()
    (root / "bza-manifest.json").write_text(json.dumps(manifest))
    data = bza.open(directory=root)
    assert len(data.cases()) == 2
    assert len(data.hearings()) == 3
    assert data.cases(outcome="granted").case_history_id.tolist() == ["a"]
    assert data.cases(project_type="single-family").case_history_id.tolist() == ["a"]
    assert len(data.cases(relief=["setbacks_yards", "lot_dimensions"])) == 2
    assert len(data.cases(relief="setbacks_yards", outcome="denied")) == 0
    assert data.cases(search="side SETBACK").case_history_id.tolist() == ["a"]
    assert len(data.cases(date_from="2025-09-20")) == 2
    assert len(data.hearings(date_from="2025-09-20")) == 2
    assert len(data.case("a")["hearings"]) == 2
    assert data.case("a")["reviews"]["history"][0]["note"] == "Reviewed correction"
    assert data.case("a")["hearings"][0]["source_file"] == "one.pdf"
    with pytest.raises(KeyError):
        data.case("missing")
    with pytest.raises(ValueError):
        data.cases(date_from="2026-01-01", date_to="2025-01-01")
    with pytest.raises(ValueError):
        data.export(tmp_path / "invalid.txt")
    path = data.export(tmp_path / "cases.json", outcome="granted")
    assert len(json.loads(path.read_text())) == 1
    assert len(pd.read_csv(data.export(tmp_path / "hearings.csv", unit="hearing"))) == 3


def test_first_use_cache_update_and_pin(tmp_path, monkeypatch):
    one = release(*bundle(tmp_path, "v1"))
    two = release(*bundle(tmp_path, "v2", "2026-09-15"))
    cache = tmp_path / "cache"
    calls = server(monkeypatch, [one])
    assert bza.open(cache=cache).manifest["version"] == "v1"
    assert len(calls) == 2
    calls = server(monkeypatch, [two, one])
    assert bza.open(cache=cache).manifest["version"] == "v1"
    assert calls == []
    bza.fetch(cache=cache)
    assert bza.open(cache=cache).manifest["version"] == "v2"
    assert bza.open(cache=cache, version="v1").manifest["version"] == "v1"
    assert _cache.read_json(cache / "state.json")["current"] == "v2"
    assert len(_cache.read_json(cache / "state.json")["downloaded"]) == 2


def test_status_never_downloads_and_pinned_first_use_does_not_select(
    tmp_path, monkeypatch
):
    one = release(*bundle(tmp_path))
    calls = server(monkeypatch, [one])
    cache = tmp_path / "cache"
    assert bza.status(cache=cache)["installed"] is None
    assert len(calls) == 1
    bza.open(cache=cache, version="v1")
    assert _cache.read_json(cache / "state.json").get("current") is None


def test_failed_update_retains_current(tmp_path, monkeypatch):
    one = release(*bundle(tmp_path, "v1"))
    two = release(*bundle(tmp_path, "v2", "2026-09-15"))
    cache = tmp_path / "cache"
    server(monkeypatch, [one])
    bza.fetch(cache=cache)
    server(monkeypatch, [(two[0], b"corrupt"), one])
    with pytest.raises(ValueError, match="checksum"):
        bza.fetch(cache=cache)
    assert _cache.read_json(cache / "state.json")["current"] == "v1"
    assert not (cache / "versions/v2").exists()
    assert bza.open(cache=cache).manifest["version"] == "v1"


def test_daily_failure_throttle_and_offline(tmp_path, monkeypatch):
    one = release(*bundle(tmp_path))
    cache = tmp_path / "cache"
    server(monkeypatch, [one])
    bza.fetch(cache=cache)
    state = _cache.read_json(cache / "state.json")
    state["checked_at"] = 0
    _cache.atomic_json(cache / "state.json", state)
    calls = []

    def offline(*args):
        calls.append(args)
        raise OSError("offline")

    monkeypatch.setattr(_cache, "https_open", offline)
    assert len(bza.open(cache=cache).cases()) == 2
    assert len(bza.open(cache=cache).cases()) == 2
    assert len(calls) == 1
    with pytest.raises(RuntimeError, match="strongtowns bza fetch"):
        bza.open(cache=tmp_path / "empty")


def test_notice_exact_text_color_pin_and_revision(monkeypatch):
    installed = {"version": "v1", "coverage_end": "2025-09-20"}
    newest = {"version": "v2", "coverage_end": "2026-09-15"}
    stream = io.StringIO()
    _cache.notice({"latest": newest}, installed, stream=stream, once=False)
    assert (
        stream.getvalue()
        == "New BZA case coverage is available: 2025-09-20 -> 2026-09-15. To update, run:\n\n    strongtowns bza fetch\n"
    )

    class Terminal(io.StringIO):
        def isatty(self):
            return True

    monkeypatch.delenv("NO_COLOR", raising=False)
    monkeypatch.setenv("TERM", "xterm")
    stream = Terminal()
    _cache.notice({"latest": newest}, installed, stream=stream, once=False)
    assert "\033[32m2026-09-15" in stream.getvalue()
    assert "\033[1;36mstrongtowns bza fetch" in stream.getvalue()
    monkeypatch.setenv("NO_COLOR", "")
    stream = Terminal()
    _cache.notice({"latest": newest}, installed, stream=stream, once=False, pinned=True)
    assert "\033" not in stream.getvalue()
    assert "does not change its pin" in stream.getvalue()
    newest["coverage_end"] = "2025-09-20"
    stream = io.StringIO()
    _cache.notice({"latest": newest}, installed, stream=stream, once=False)
    assert "New BZA case data is available: v1 -> v2." in stream.getvalue()
    _cache._NOTIFIED.clear()
    stream = io.StringIO()
    for _ in range(2):
        _cache.notice({"latest": newest}, installed, stream=stream)
    assert stream.getvalue().count("To update") == 1


def test_incompatible_release_and_local_corruption(tmp_path, monkeypatch):
    one = release(*bundle(tmp_path))
    incompatible = {
        **one[0],
        "version": "v3",
        "schema_version": 9,
        "url": "https://example.org/v3.zip",
    }
    server(monkeypatch, [(incompatible, b""), one])
    cache = tmp_path / "cache"
    assert bza.fetch(cache=cache)["version"] == "v1"
    (cache / "versions/v1/case_histories.csv").write_text("broken")
    with pytest.raises(ValueError, match="checksum"):
        bza.open(cache=cache)


def test_archive_traversal_rejected(tmp_path, monkeypatch):
    root, manifest = bundle(tmp_path)
    item, _ = release(root, manifest)
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w") as archive:
        archive.writestr("../escape", "bad")
    data = stream.getvalue()
    item["sha256"] = hashlib.sha256(data).hexdigest()
    server(monkeypatch, [(item, data)])
    with pytest.raises(ValueError, match="Unsafe"):
        bza.fetch(cache=tmp_path / "cache")
    assert not (tmp_path / "cache/escape").exists()


def test_invalid_version_cannot_escape_cache(tmp_path):
    with pytest.raises(ValueError):
        bza.open(version="../elsewhere", cache=tmp_path)
