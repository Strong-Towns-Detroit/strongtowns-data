"""Collect a broad OSM POI snapshot for a place or supplied boundary."""

from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path

import geopandas as gpd

from krabby_real_estate.pois.osm import collect_osm_pois, write_osm_snapshot


def parse_args():
    parser = argparse.ArgumentParser()
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--place", help='OSM geocoder place, e.g. "Detroit, Michigan, USA"')
    source.add_argument("--boundary", type=Path, help="GeoJSON/GPKG polygon boundary")
    parser.add_argument("--output-dir", type=Path, required=True)
    return parser.parse_args()


def main():
    args = parse_args()
    boundary = None
    if args.boundary:
        boundary_gdf = gpd.read_file(args.boundary).to_crs("EPSG:4326")
        boundary = boundary_gdf.geometry.union_all()
    raw, normalized = collect_osm_pois(place=args.place, boundary=boundary)
    paths = write_osm_snapshot(raw, normalized, args.output_dir)
    manifest = {
        "collected_at": datetime.now(UTC).isoformat(),
        "source": "openstreetmap",
        "place": args.place,
        "boundary": str(args.boundary) if args.boundary else None,
        "raw_feature_count": len(raw),
        "normalized_feature_count": len(normalized),
        "files": {name: str(path) for name, path in paths.items()},
    }
    (args.output_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")


if __name__ == "__main__":
    main()
