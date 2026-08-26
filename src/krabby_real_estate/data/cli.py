"""Core local lifecycle CLI for registered Krabby data assets."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from krabby_real_estate.data.acquisition import (
    fetch_base_units,
    fetch_osm_pois,
    fetch_parcels,
)
from krabby_real_estate.data.catalog import catalog
from krabby_real_estate.data.legacy import LEGACY_SOURCES, register_legacy_source
from krabby_real_estate.data.manifest import resolve_promoted
from krabby_real_estate.data.migration import validate_anchor_migration
from krabby_real_estate.data.pipelines import collect_traveltime_results, run_offline_pipeline
from krabby_real_estate.data.review import export_anchor_review, import_anchor_review
from krabby_real_estate.data.storage import promote_snapshot, validate_snapshot


def repository_root() -> Path:
    return Path.cwd().resolve()


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(prog="krabby-data")
    commands = root.add_subparsers(dest="command", required=True)
    commands.add_parser("list")
    commands.add_parser("graph")
    commands.add_parser("migration-check")
    legacy = commands.add_parser("import-legacy")
    legacy.add_argument("assets", nargs="*", choices=sorted(LEGACY_SOURCES))
    legacy.add_argument("--promote", action="store_true")
    status = commands.add_parser("status")
    status.add_argument("assets", nargs="*")
    validate = commands.add_parser("validate")
    validate.add_argument("target")
    promote = commands.add_parser("promote")
    promote.add_argument("asset_id", choices=sorted(catalog.assets))
    promote.add_argument("manifest", type=Path)
    build = commands.add_parser("build")
    build.add_argument("pipelines", nargs="*")
    build.add_argument("--no-promote", action="store_true")
    build.add_argument("--parameter", action="append", default=[], metavar="KEY=VALUE")
    fetch = commands.add_parser("fetch")
    fetch.add_argument("source", choices=("parcels", "base-units", "osm-pois", "traveltime"))
    fetch.add_argument("--apply", action="store_true")
    fetch.add_argument("--allow-paid", action="store_true")
    fetch.add_argument("--smoke", action="store_true")
    fetch.add_argument("--promote", action="store_true")
    review = commands.add_parser("review")
    review_commands = review.add_subparsers(dest="review_command", required=True)
    review_export = review_commands.add_parser("export")
    review_export.add_argument("output", type=Path)
    review_import = review_commands.add_parser("import")
    review_import.add_argument("review_file", type=Path)
    review_import.add_argument("--promote", action="store_true")
    return root


def _pointer(root: Path, asset_id: str) -> Path:
    return root / catalog.assets[asset_id].storage_root / "PROMOTED.json"


def _status(root: Path, asset_id: str) -> dict:
    pointer = _pointer(root, asset_id)
    asset_root = root / catalog.assets[asset_id].storage_root
    staging = list((asset_root / ".staging").glob("*"))
    completed = list((asset_root / "snapshots").glob("*/manifest.json"))
    context = {
        "completed_snapshot_count": len(completed),
        "staging_attempt_count": len(staging),
        "failed_staging_count": sum((path / "failure-report.json").exists() for path in staging),
    }
    if not pointer.exists():
        status = "unpromoted" if completed else "missing"
        if not completed and staging:
            status = "staged"
        return {"asset_id": asset_id, "status": status, **context}
    try:
        reference = resolve_promoted(pointer)
        errors = validate_snapshot(root, reference.manifest_path)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        return {
            "asset_id": asset_id,
            "status": "invalid",
            "errors": [str(error)],
            **context,
        }
    return {
        "asset_id": asset_id,
        "status": "promoted" if not errors else "invalid",
        "snapshot_id": reference.snapshot_id,
        "manifest_sha256": reference.manifest_sha256,
        "errors": errors,
        **context,
    }


def _parameters(values: list[str]) -> dict[str, str]:
    result = {}
    for value in values:
        if "=" not in value:
            raise ValueError(f"parameter must use KEY=VALUE: {value!r}")
        key, item = value.split("=", 1)
        if not key or key in result:
            raise ValueError(f"invalid or duplicate parameter: {key!r}")
        result[key] = item
    return result


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    root = repository_root()
    load_dotenv(root / ".env")
    if args.command == "list":
        for asset in catalog.assets.values():
            print(
                "\t".join(
                    (
                        asset.asset_id,
                        asset.tier.value,
                        asset.contract.contract_id,
                        asset.contract.version,
                        asset.acquisition_policy.value,
                        asset.producer_pipeline_id or "-",
                    )
                )
            )
        return 0
    if args.command == "graph":
        for pipeline_id in catalog.topological_pipelines():
            pipeline = catalog.pipelines[pipeline_id]
            print(f"{pipeline_id}: {', '.join(pipeline.inputs)} -> {', '.join(pipeline.outputs)}")
        return 0
    if args.command == "migration-check":
        import geopandas as gpd
        import pandas as pd

        from krabby_real_estate.data.artifacts import artifact_path

        anchor_ref = resolve_promoted(_pointer(root, "detroit.parcel-routing-anchors"))
        disposition_ref = resolve_promoted(_pointer(root, "detroit.anchor-dispositions"))
        report = validate_anchor_migration(
            gpd.read_parquet(artifact_path(root, anchor_ref)),
            pd.read_parquet(artifact_path(root, disposition_ref)),
            root / "data/derived/parcel-routing-anchors.gpkg",
        )
        print(json.dumps(report, indent=2))
        return 0
    if args.command == "import-legacy":
        selected = args.assets or sorted(LEGACY_SOURCES)
        for asset_id in selected:
            reference = register_legacy_source(root, asset_id)
            print(f"registered {asset_id} {reference.snapshot_id}")
            if args.promote:
                promote_snapshot(root, catalog.assets[asset_id], reference.manifest_path)
                print(f"promoted {asset_id} {reference.snapshot_id}")
        return 0
    if args.command == "status":
        selected = args.assets or sorted(catalog.assets)
        unknown = sorted(set(selected) - set(catalog.assets))
        if unknown:
            print(f"unknown assets: {', '.join(unknown)}", file=sys.stderr)
            return 2
        reports = [_status(root, asset_id) for asset_id in selected]
        print(json.dumps(reports, indent=2))
        return int(any(report["status"] == "invalid" for report in reports))
    if args.command == "validate":
        target = Path(args.target)
        if args.target in catalog.assets:
            pointer = _pointer(root, args.target)
            if not pointer.exists():
                print(f"asset has no promoted snapshot: {args.target}", file=sys.stderr)
                return 1
            manifest_path = resolve_promoted(pointer).manifest_path
        else:
            manifest_path = target
        errors = validate_snapshot(root, manifest_path)
        if errors:
            print("\n".join(errors), file=sys.stderr)
            return 1
        print(f"valid: {manifest_path}")
        return 0
    if args.command == "promote":
        reference = promote_snapshot(root, catalog.assets[args.asset_id], args.manifest)
        print(f"promoted {reference.asset_id} {reference.snapshot_id}")
        return 0
    if args.command == "build":
        selected = set(args.pipelines) if args.pipelines else None
        unknown = sorted((selected or set()) - set(catalog.pipelines))
        if unknown:
            print(f"unknown pipelines: {', '.join(unknown)}", file=sys.stderr)
            return 2
        ordered = catalog.topological_pipelines(selected)
        if selected is None:
            ordered = [
                name
                for name in ordered
                if name not in {"prepare.traveltime-requests", "collect.traveltime-results"}
            ]
        if "collect.traveltime-results" in ordered:
            print(
                "collect.traveltime-results is paid acquisition; use `krabby-data fetch traveltime`",
                file=sys.stderr,
            )
            return 2
        try:
            parameters = _parameters(args.parameter)
        except ValueError as error:
            print(str(error), file=sys.stderr)
            return 2
        missing = []
        for pipeline_id in ordered:
            pipeline = catalog.pipelines[pipeline_id]
            for input_id in pipeline.inputs:
                if (
                    not _pointer(root, input_id).exists()
                    and catalog.producers.get(input_id) not in ordered
                ):
                    missing.append((pipeline_id, input_id))
        if missing:
            report = {"missing_inputs": missing}
            print(json.dumps(report, indent=2), file=sys.stderr)
            return 1
        built = {}
        for pipeline_id in ordered:
            pipeline = catalog.pipelines[pipeline_id]
            inputs = {}
            for asset_id in pipeline.inputs:
                if asset_id in built:
                    inputs[asset_id] = built[asset_id]
                else:
                    inputs[asset_id] = resolve_promoted(_pointer(root, asset_id))
            try:
                outputs = run_offline_pipeline(root, pipeline_id, inputs, parameters)
            except (OSError, ValueError, KeyError) as error:
                print(f"{pipeline_id} failed: {error}", file=sys.stderr)
                return 1
            for asset_id, reference in outputs.items():
                built[asset_id] = reference
                print(f"built {asset_id} {reference.snapshot_id}")
                if not args.no_promote:
                    promote_snapshot(root, catalog.assets[asset_id], reference.manifest_path)
                    print(f"promoted {asset_id} {reference.snapshot_id}")
        return 0
    if args.command == "fetch":
        if not args.apply:
            print(f"fetch {args.source} is a dry run; pass --apply to contact the provider")
            return 0
        if args.source == "parcels":
            reference = fetch_parcels(root)
            print(f"fetched detroit.parcels.raw {reference.snapshot_id}")
            if args.promote:
                promote_snapshot(
                    root, catalog.assets["detroit.parcels.raw"], reference.manifest_path
                )
            return 0
        if args.source == "base-units":
            outputs = fetch_base_units(root)
            for asset_id, reference in outputs.items():
                print(f"fetched {asset_id} {reference.snapshot_id}")
                if args.promote:
                    promote_snapshot(root, catalog.assets[asset_id], reference.manifest_path)
            return 0
        if args.source == "osm-pois":
            reference = fetch_osm_pois(root)
            print(f"fetched osm.detroit.pois.raw {reference.snapshot_id}")
            if args.promote:
                promote_snapshot(
                    root, catalog.assets["osm.detroit.pois.raw"], reference.manifest_path
                )
            return 0
        if not args.allow_paid:
            print("paid acquisition requires --allow-paid", file=sys.stderr)
            return 2
        request_ref = resolve_promoted(_pointer(root, "traveltime.requests"))
        if args.smoke:
            import pandas as pd

            from krabby_real_estate.data.artifacts import artifact_path

            requests = pd.read_parquet(artifact_path(root, request_ref))
            if requests["anchor_uuid"].nunique() != 1 or len(requests) > 2:
                print(
                    "smoke mode requires a promoted ledger for one anchor and at most two directions",
                    file=sys.stderr,
                )
                return 2
        app_id = os.environ.get("TRAVELTIME_APP_ID")
        api_key = os.environ.get("TRAVELTIME_API_KEY")
        if not app_id or not api_key:
            print("TRAVELTIME_APP_ID and TRAVELTIME_API_KEY are required", file=sys.stderr)
            return 2
        reference = collect_traveltime_results(root, request_ref, app_id=app_id, api_key=api_key)
        print(f"collected traveltime.results {reference.snapshot_id}")
        if args.promote:
            promote_snapshot(root, catalog.assets["traveltime.results"], reference.manifest_path)
            print(f"promoted traveltime.results {reference.snapshot_id}")
        return 0
    if args.command == "review":
        anchor_ref = resolve_promoted(_pointer(root, "detroit.parcel-routing-anchors"))
        disposition_ref = resolve_promoted(_pointer(root, "detroit.anchor-dispositions"))
        if args.review_command == "export":
            output = export_anchor_review(root, anchor_ref, disposition_ref, args.output)
            print(f"exported {output}")
            return 0
        reference = import_anchor_review(root, anchor_ref, disposition_ref, args.review_file)
        print(f"imported detroit.anchor-dispositions {reference.snapshot_id}")
        if args.promote:
            promote_snapshot(
                root, catalog.assets["detroit.anchor-dispositions"], reference.manifest_path
            )
            print(f"promoted detroit.anchor-dispositions {reference.snapshot_id}")
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
