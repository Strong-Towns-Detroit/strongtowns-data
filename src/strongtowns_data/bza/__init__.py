"""Read prepared Detroit BZA cases without running the private pipeline."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

import pandas as pd

from . import _cache
from ._cache import fetch

__all__ = ["BzaDataset", "open", "fetch", "status"]


def _records(frame):
    return json.loads(frame.to_json(orient="records", date_format="iso"))


def _read(root, name):
    path = root / name
    return pd.read_csv(path, keep_default_na=False) if path.exists() else pd.DataFrame()


def status(*, cache=None, version=None, stream=None, notify=True):
    root = _cache.cache_root(cache)
    state = _cache.check(root)
    selected = version or state.get("current")
    manifest = None
    if selected:
        directory = root / "versions" / _cache.version_name(selected)
        if directory.exists():
            manifest = _cache.verify(directory)
    if notify:
        _cache.notice(state, manifest, pinned=version is not None, stream=stream)
    return {
        "installed": manifest,
        "selected_version": selected,
        "latest": state.get("latest"),
        "downloaded": state.get("downloaded", {}),
        "check_error": state.get("check_error"),
    }


class BzaDataset:
    """Prepared tables. Use ``open`` for cached releases or an explicit local pin."""

    def __init__(self, directory, *, manifest=None):
        self.directory = Path(directory)
        self.manifest = manifest or _cache.read_json(
            self.directory / "bza-manifest.json", {}
        )
        self._cases = _read(self.directory, "case_histories.csv")
        self._hearings = _read(self.directory, "case_occurrences.csv")
        if (
            "case_history_id" not in self._cases
            or "occurrence_id" not in self._hearings
        ):
            raise ValueError("BZA dataset lacks case histories or hearing occurrences")
        if (
            self._cases.case_history_id.duplicated().any()
            or self._hearings.occurrence_id.duplicated().any()
        ):
            raise ValueError("BZA dataset contains duplicate identities")
        if (
            self._cases.case_history_id.eq("").any()
            or self._hearings.occurrence_id.eq("").any()
        ):
            raise ValueError("BZA identities must not be empty")
        if set(self._hearings.case_history_id) - set(self._cases.case_history_id):
            raise ValueError("BZA hearings refer to missing case histories")
        for value in self._hearings.meeting_date:
            date.fromisoformat(value)
        enriched = _read(
            self.directory,
            "project_type_enrichment/case_histories_with_project_types.csv",
        )
        if not enriched.empty:
            columns = ["case_history_id"] + [
                c for c in enriched if c not in self._cases
            ]
            self._cases = self._cases.merge(
                enriched[columns],
                on="case_history_id",
                how="left",
                validate="one_to_one",
            )
        classified = _read(self.directory, "classified_cases.csv")
        if not classified.empty:
            columns = ["occurrence_id"] + [
                c for c in classified if c not in self._hearings
            ]
            self._hearings = self._hearings.merge(
                classified[columns],
                on="occurrence_id",
                how="left",
                validate="one_to_one",
            )

    @classmethod
    def open(cls, **kwargs):
        return open(**kwargs)

    def status(self):
        audits = {
            p.name: json.loads(p.read_text())
            for p in self.directory.glob("*audit.json")
        }
        dates = self._hearings.meeting_date
        return {
            "version": self.manifest.get("version"),
            "coverage_start": dates.min(),
            "coverage_end": dates.max(),
            "cases": len(self._cases),
            "hearings": len(self._hearings),
            "audits": audits,
        }

    def _select(
        self,
        *,
        relief=None,
        project_type=None,
        outcome=None,
        search=None,
        date_from=None,
        date_to=None,
    ):
        frame = self._cases.copy()

        def values(value):
            return [value] if isinstance(value, str) else list(value)

        def normalized(value):
            value = str(value).strip().lower().replace("-", "_").replace(" ", "_")
            return {
                "single_family_dwelling": "single_family",
                "single_family_house": "single_family",
                "two_family_dwelling": "duplex",
                "two_family_house": "duplex",
            }.get(value, value)

        for value, columns, aliases in (
            (relief, ["relief_categories"], {}),
            (project_type, ["project_type_family", "project_type_label"], {}),
            (
                outcome,
                ["final_outcome"],
                {"granted": "granted_reversed", "denied": "denied_upheld"},
            ),
        ):
            if value:
                wanted = {
                    aliases.get(normalized(v), normalized(v)) for v in values(value)
                }
                matched = pd.Series(False, index=frame.index)
                for column in columns:
                    if column in frame:
                        matched |= (
                            frame[column]
                            .fillna("")
                            .map(
                                lambda cell: bool(
                                    wanted
                                    & {normalized(v) for v in str(cell).split("|")}
                                )
                            )
                        )
                frame = frame[matched]
        if search:
            ids = set()
            for table in (self._cases, self._hearings):
                columns = [
                    c
                    for c in (
                        "proposal",
                        "location",
                        "petitioner",
                        "decision",
                        "source_text",
                        "relief_evidence",
                        "printed_case_number",
                        "case_number",
                    )
                    if c in table
                ]
                mask = (
                    table[columns]
                    .astype(str)
                    .agg(" ".join, axis=1)
                    .str.contains(search, case=False, regex=False)
                )
                ids.update(table.loc[mask, "case_history_id"])
            frame = frame[frame.case_history_id.isin(ids)]
        if date_from or date_to:
            for value in (date_from, date_to):
                if value:
                    date.fromisoformat(value)
            if date_from and date_to and date_from > date_to:
                raise ValueError("Start date must not follow end date")
            hearing = self._hearings
            if date_from:
                hearing = hearing[hearing.meeting_date >= date_from]
            if date_to:
                hearing = hearing[hearing.meeting_date <= date_to]
            frame = frame[frame.case_history_id.isin(hearing.case_history_id)]
        return frame

    def cases(self, **filters):
        """One row per case; date filters match any hearing in the inclusive range."""
        return self._select(**filters).reset_index(drop=True)

    def hearings(self, **filters):
        cases = self._select(**filters)
        frame = self._hearings[
            self._hearings.case_history_id.isin(cases.case_history_id)
        ]
        if filters.get("date_from"):
            frame = frame[frame.meeting_date >= filters["date_from"]]
        if filters.get("date_to"):
            frame = frame[frame.meeting_date <= filters["date_to"]]
        return frame.sort_values(["meeting_date", "occurrence_id"]).reset_index(
            drop=True
        )

    def case(self, case_history_id):
        frame = self._cases[self._cases.case_history_id == case_history_id]
        if frame.empty:
            raise KeyError(f"Unknown BZA case history: {case_history_id}")
        result = _records(frame)[0]
        result["hearings"] = _records(
            self._hearings[
                self._hearings.case_history_id == case_history_id
            ].sort_values("meeting_date")
        )
        for name, filename in [
            ("relief", "case_categories.csv"),
            ("sites", "case_site_parcels.csv"),
            ("intake_candidates", "intake_date_candidates.csv"),
        ]:
            table = _read(self.directory, filename)
            result[name] = (
                _records(table[table.case_history_id == case_history_id])
                if "case_history_id" in table
                else []
            )
        result["reviews"] = {}
        hearing_ids = {row["occurrence_id"] for row in result["hearings"]}
        site_keys = {row.get("site_key") for row in result["sites"]}
        for path in sorted((self.directory / "reviews").glob("*.csv")):
            table = pd.read_csv(path, keep_default_na=False)
            mask = pd.Series(False, index=table.index)
            if "case_history_id" in table:
                mask |= table.case_history_id.eq(case_history_id)
            if "occurrence_id" in table:
                mask |= table.occurrence_id.isin(hearing_ids)
            if "site_key" in table:
                mask |= table.site_key.isin(site_keys)
            result["reviews"][path.stem] = _records(table[mask])
        return result

    def export(self, output, *, unit="case", **filters):
        if unit not in ("case", "hearing"):
            raise ValueError("unit must be case or hearing")
        path = Path(output)
        if path.suffix.lower() not in (".csv", ".json"):
            raise ValueError("Export output must end in .csv or .json")
        frame = self.hearings(**filters) if unit == "hearing" else self.cases(**filters)
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.suffix.lower() == ".csv":
            frame.to_csv(path, index=False)
        else:
            path.write_text(json.dumps(_records(frame), indent=2) + "\n")
        return path


def open(
    *,
    version=None,
    cache=None,
    directory=None,
    lock=None,
    repository=None,
    stream=None,
    notify=True,
):
    """Open a release, explicit local bundle, or existing repository lock offline.

    Unpinned remote datasets are fetched only if no selected local copy exists.
    Explicit local directories and locks never perform network operations.
    """
    if sum(x is not None for x in (directory, lock, version)) > 1:
        raise ValueError("Choose one of directory, lock, or version")
    if lock is not None:
        from strongtowns_data.pipelines.engine import DataBuildSystem
        from strongtowns_data.repository import DataLock, DataRepository

        data_lock = DataLock.load(lock)
        repo = DataRepository(DataBuildSystem.find(repository or Path(lock).parent))
        ids = {a.dataset_id for a in data_lock.assets}
        asset_id = (
            "detroit.bza.atlas"
            if "detroit.bza.atlas" in ids
            else "detroit.bza.gemini.raw"
        )
        reference = data_lock.asset(asset_id)
        path, manifest = repo.resolve(reference)
        from strongtowns_data.pipelines.snapshots import validate_snapshot

        validate_snapshot(repo.system.assets[asset_id], path)
        return BzaDataset(
            path / "raw" if asset_id.endswith(".raw") else path,
            manifest={"version": reference.snapshot_id, "provenance": manifest},
        )
    if directory is not None:
        path = Path(directory)
        manifest = (
            _cache.verify(path) if (path / "bza-manifest.json").exists() else None
        )
        return BzaDataset(path, manifest=manifest)
    root = _cache.cache_root(cache)
    state = _cache.read_json(root / "state.json", {})
    selected = version or state.get("current")
    if (
        selected is None
        or not (root / "versions" / _cache.version_name(selected)).exists()
    ):
        manifest = fetch(version=version, cache=root, select=version is None)
        selected = manifest["version"]
    path = root / "versions" / _cache.version_name(selected)
    manifest = _cache.verify(path)
    state = _cache.check(root)
    if notify:
        _cache.notice(state, manifest, pinned=version is not None, stream=stream)
    return BzaDataset(path, manifest=manifest)
