"""Offline BZA release assembly. All paths are explicit; no provider calls."""

from __future__ import annotations

import hashlib
import json
import shutil
import zipfile
from pathlib import Path

import geopandas as gpd
import pandas as pd

from . import build_bza_atlas_dataset as atlas
from . import build_bza_case_histories as histories
from . import classify_bza_relief as relief
from . import merge_cases
from . import normalize_bza_outcomes as outcomes
from .bza_site_matching import build_matches
from .recover_bza_sites_from_base_units import build_recoveries


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build(
    source: Path,
    output: Path,
    *,
    reviews: Path,
    parcels: Path | None = None,
    addresses: Path | None = None,
) -> dict:
    source, output, reviews = Path(source), Path(output), Path(reviews)
    if output.exists() and any(output.iterdir()):
        raise ValueError("BZA output must be an empty staging directory")
    if output.resolve() == source.resolve() or output.resolve().is_relative_to(
        source.resolve()
    ):
        raise ValueError("BZA output must be separate from source evidence")
    output.mkdir(parents=True, exist_ok=True)
    audit = {"enrichment": {}, "source_files": {}, "review_files": {}}
    for path in sorted(source.rglob("*")):
        if path.is_file() and not path.is_symlink():
            audit["source_files"][str(path.relative_to(source))] = sha(path)
    for name in (
        "bza_case_history_overrides.csv",
        "bza_relief_case_reviews.csv",
        "bza_site_overrides.csv",
    ):
        path = reviews / name
        audit["review_files"][name] = sha(path)
        (output / "reviews").mkdir(exist_ok=True)
        shutil.copy2(path, output / "reviews" / name)
    if (source / "per_doc").is_dir():
        shutil.copytree(source / "per_doc", output / "per_doc")
        merge_cases.run(output)
    else:
        # Existing immutable imports may contain aggregate evidence only.
        for name in ("all_cases.csv", "all_cases.json"):
            shutil.copy2(source / name, output / name)
    relief.run(output / "all_cases.csv", output)
    histories.run(
        output / "classified_cases.csv",
        reviews / "bza_case_history_overrides.csv",
        reviews / "bza_relief_case_reviews.csv",
        output,
    )
    outcomes.run(output / "case_occurrences.csv", output / "case_histories.csv", output)
    cases = pd.read_csv(output / "case_histories.csv")
    occurrences = pd.read_csv(output / "case_occurrences.csv")
    if parcels is not None:
        parcels = Path(parcels)
        audit["spatial_inputs"] = {
            "parcels": {"path": str(parcels), "sha256": sha(parcels)}
        }
        parcel_frame = (
            gpd.read_parquet(parcels)
            if parcels.suffix == ".parquet"
            else gpd.read_file(parcels)
        )
        candidates, sites, matching = build_matches(
            pd.read_csv(output / "classified_cases.csv"),
            occurrences,
            parcel_frame,
            pd.read_csv(reviews / "bza_site_overrides.csv"),
        )
        candidates.to_csv(output / "case_site_candidates.csv", index=False)
        audit["enrichment"]["sites"] = {"status": "computed", **matching}
        if addresses is not None:
            addresses = Path(addresses)
            audit["spatial_inputs"]["addresses"] = {
                "path": str(addresses),
                "sha256": sha(addresses),
            }
            units = (
                gpd.read_parquet(addresses)
                if addresses.suffix == ".parquet"
                else gpd.read_file(addresses)
            )
            suggestions, recovered = build_recoveries(
                candidates, sites, units, parcel_frame
            )
            suggestions.to_csv(output / "site_review_suggestions.csv", index=False)
            recovered.to_csv(output / "base_units_second_pass_audit.csv", index=False)
            audit["enrichment"]["base_units"] = {
                "status": "review_required",
                "suggestions": len(suggestions),
            }
        else:
            audit["enrichment"]["base_units"] = {"status": "unavailable"}
    elif (source / "map_sites.gpkg").exists():
        sites = gpd.read_file(source / "map_sites.gpkg")
        sites = sites[sites.case_history_id.isin(cases.case_history_id)]
        audit["enrichment"]["sites"] = {
            "status": "reused_source_evidence",
            "review_application": "Recorded matches retained; site overrides require parcel inputs to recompute.",
        }
        audit["enrichment"]["base_units"] = {"status": "unavailable"}
        for name in ("case_site_candidates.csv", "base_units_second_pass_audit.csv"):
            if (source / name).exists():
                shutil.copy2(source / name, output / name)
    else:
        sites = gpd.GeoDataFrame(
            columns=[
                "case_history_id",
                "site_id",
                "site_key",
                "parcel_id",
                "address",
                "match_method",
                "geometry",
            ],
            geometry="geometry",
            crs="EPSG:4326",
        )
        audit["enrichment"]["sites"] = {"status": "unavailable"}
        audit["enrichment"]["base_units"] = {"status": "unavailable"}
    sites.to_file(output / "map_sites.gpkg", driver="GPKG")
    sites.drop(columns="geometry").to_csv(output / "case_site_parcels.csv", index=False)
    audit["enrichment"]["sites"]["unmatched_case_ids"] = sorted(
        set(cases.case_history_id) - set(sites.case_history_id)
    )
    project_source = source / "project_type_enrichment"
    project_output = output / "project_type_enrichment"
    project_output.mkdir()
    classifications_path = project_source / "project_types.csv"
    if classifications_path.exists():
        classifications = pd.read_csv(classifications_path)
        if (
            "case_history_id" not in classifications
            or classifications.case_history_id.duplicated().any()
        ):
            raise ValueError("Invalid project-type evidence identities")
        extra = [c for c in classifications if c == "case_history_id" or c not in cases]
        enriched = cases.merge(
            classifications[extra],
            on="case_history_id",
            how="left",
            validate="one_to_one",
        )
        classifications.to_csv(project_output / "project_types.csv", index=False)
        audit["enrichment"]["project_types"] = {"status": "reused_source_evidence"}
    else:
        enriched = cases.assign(
            project_type_family=pd.NA, project_type_label=pd.NA, confidence=pd.NA
        )
        audit["enrichment"]["project_types"] = {"status": "unavailable"}
    enriched.to_csv(
        project_output / "case_histories_with_project_types.csv", index=False
    )
    pending = enriched[
        enriched.project_type_family.isna()
        | enriched.confidence.isin(["medium", "low"])
    ]
    pending.to_csv(project_output / "review_medium_low_confidence.csv", index=False)
    audit["enrichment"]["project_types"]["review_case_ids"] = (
        pending.case_history_id.tolist()
    )
    intake = source / "intake_date_candidates.csv"
    if intake.exists():
        shutil.copy2(intake, output / intake.name)
        audit["enrichment"]["intake_dates"] = {"status": "candidates_require_review"}
    else:
        pd.DataFrame(
            columns=["case_history_id", "accela_opened_date", "suggested_disposition"]
        ).to_csv(output / "intake_date_candidates.csv", index=False)
        audit["enrichment"]["intake_dates"] = {"status": "unavailable"}
    atlas.run(output, output)
    audit["counts"] = {"cases": len(cases), "hearings": len(occurrences)}
    (output / "release_audit.json").write_text(json.dumps(audit, indent=2) + "\n")
    return audit


def package(
    directory: Path,
    destination: Path,
    *,
    version: str,
    release_url: str,
    prior_releases: tuple = (),
) -> Path:
    """Create reviewable GitHub assets locally; never publish or alter input."""
    from .._cache import validate_release, verify, version_name

    version_name(version)
    destination.mkdir(parents=True, exist_ok=True)
    archive = destination / f"bza-{version}.zip"
    if archive.exists() or (destination / "bza-index.json").exists():
        raise FileExistsError("Release output already exists; use a new destination")
    occurrence = pd.read_csv(directory / "case_occurrences.csv")
    files = {
        str(p.relative_to(directory)): sha(p)
        for p in sorted(directory.rglob("*"))
        if p.is_file()
        and not p.is_symlink()
        and p.name not in ("manifest.json", "bza-manifest.json")
    }
    manifest = {
        "schema_version": 1,
        "version": version,
        "coverage_start": occurrence.meeting_date.min(),
        "coverage_end": occurrence.meeting_date.max(),
        "files": files,
        "provenance": json.loads((directory / "release_audit.json").read_text()),
    }
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        for name in files:
            (work / name).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(directory / name, work / name)
        (work / "bza-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
        verify(work)
        with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
            for path in sorted(work.rglob("*")):
                if path.is_file():
                    bundle.write(path, path.relative_to(work))
    release = {
        k: manifest[k]
        for k in ("version", "schema_version", "coverage_start", "coverage_end")
    }
    release.update(url=release_url, sha256=sha(archive))
    validate_release(release)
    (destination / "bza-index.json").write_text(
        json.dumps({"releases": [release, *prior_releases]}, indent=2) + "\n"
    )
    return archive


def validate(directory: Path, _manifest: dict) -> None:
    """Validate the complete internal atlas artifact contract before promotion."""
    from .. import BzaDataset

    dataset = BzaDataset(directory)
    categories = pd.read_csv(directory / "case_categories.csv")
    if categories.duplicated(["case_history_id", "category"]).any():
        raise ValueError("Duplicate BZA case/category assignments")
    if set(categories.case_history_id) - set(dataset.cases().case_history_id):
        raise ValueError("Relief categories refer to missing BZA histories")
    for name in ("map_sites.gpkg", "atlas_category_sites.gpkg"):
        table = gpd.read_file(directory / name)
        if set(table.case_history_id) - set(dataset.cases().case_history_id):
            raise ValueError(f"{name} refers to missing BZA histories")
    audit = json.loads((directory / "release_audit.json").read_text())
    if audit["counts"] != {
        "cases": len(dataset.cases()),
        "hearings": len(dataset.hearings()),
    }:
        raise ValueError("BZA release counts disagree with its tables")
    for name in (
        "atlas_applications.csv",
        "atlas_category_summary.csv",
        "atlas_dataset_audit.json",
        "project_type_enrichment/case_histories_with_project_types.csv",
        "intake_date_candidates.csv",
    ):
        if not (directory / name).is_file():
            raise ValueError(f"Missing BZA atlas artifact: {name}")
