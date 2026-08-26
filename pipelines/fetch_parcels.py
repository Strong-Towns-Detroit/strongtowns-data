"""Fetch a versioned snapshot of Detroit's current assessor parcels."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path

from krabby_real_estate.parcels.fetcher import (
    ARCGIS_ITEM_ID,
    FEATURE_SERVICE,
    fetch_csv,
    fetch_geojson,
)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--format", choices=("geojson", "csv"), default="geojson")
    return parser.parse_args()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    destination = args.output_dir / f"parcels.{args.format}"
    fetch = fetch_geojson if args.format == "geojson" else fetch_csv
    fetch(destination)
    manifest = {
        "collected_at": datetime.now(UTC).isoformat(),
        "arcgis_item_id": ARCGIS_ITEM_ID,
        "feature_service": FEATURE_SERVICE,
        "format": args.format,
        "output": str(destination),
        "bytes": destination.stat().st_size,
        "sha256": sha256(destination),
    }
    manifest_path = destination.with_suffix(".manifest.json")
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"parcels: {manifest['bytes']:,} bytes -> {destination}")


if __name__ == "__main__":
    main()
