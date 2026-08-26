"""Build parcel/street routing anchors from assessor parcels and Base Units."""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
from datetime import UTC, datetime
from pathlib import Path

import geopandas as gpd

from krabby_real_estate.base_units.anchors import (
    OUTPUT_CRS,
    PROJECTED_CRS,
    build_parcel_routing_anchors,
)

logger = logging.getLogger(__name__)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--parcels", type=Path, required=True)
    parser.add_argument("--addresses", type=Path, required=True)
    parser.add_argument("--streets", type=Path, required=True)
    parser.add_argument("--buildings", type=Path)
    parser.add_argument("--output-gpkg", type=Path, required=True)
    parser.add_argument("--output-csv", type=Path, required=True)
    return parser.parse_args()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_record(path: Path) -> dict:
    return {"path": str(path), "bytes": path.stat().st_size, "sha256": sha256(path)}


def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    args = parse_args()
    logger.info("Reading parcel and Base Units snapshots")
    parcels = gpd.read_file(args.parcels)
    addresses = gpd.read_file(args.addresses)
    streets = gpd.read_file(args.streets)
    buildings = gpd.read_file(args.buildings) if args.buildings else None
    anchors, edges, summary = build_parcel_routing_anchors(
        parcels, addresses, streets, buildings=buildings
    )

    args.output_gpkg.parent.mkdir(parents=True, exist_ok=True)
    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    temporary_gpkg = args.output_gpkg.with_name(
        f"{args.output_gpkg.stem}.tmp{args.output_gpkg.suffix}"
    )
    temporary_csv = args.output_csv.with_name(f"{args.output_csv.stem}.tmp{args.output_csv.suffix}")
    temporary_gpkg.unlink(missing_ok=True)
    logger.info("Writing %s anchors and frontage geometries", len(anchors))
    anchors.to_file(temporary_gpkg, layer="anchors", driver="GPKG")
    edges.to_file(temporary_gpkg, layer="front_edges", driver="GPKG")
    anchors.drop(columns="geometry").to_csv(temporary_csv, index=False)
    temporary_gpkg.replace(args.output_gpkg)
    temporary_csv.replace(args.output_csv)

    sources = {
        "parcels": source_record(args.parcels),
        "addresses": source_record(args.addresses),
        "streets": source_record(args.streets),
    }
    if args.buildings:
        sources["buildings"] = source_record(args.buildings)
    manifest = {
        "generated_at": datetime.now(UTC).isoformat(),
        "projected_crs": PROJECTED_CRS,
        "output_crs": OUTPUT_CRS,
        "sources": sources,
        "outputs": {
            "geopackage": str(args.output_gpkg),
            "travel_time_csv": str(args.output_csv),
        },
        "summary": summary,
    }
    manifest_path = args.output_gpkg.with_suffix(".manifest.json")
    temporary_manifest = manifest_path.with_name(f"{manifest_path.stem}.tmp{manifest_path.suffix}")
    temporary_manifest.write_text(json.dumps(manifest, indent=2) + "\n")
    temporary_manifest.replace(manifest_path)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
