"""Collect arrival/departure time-map polygons for parcel routing anchors."""

from __future__ import annotations

import argparse
import csv
import json
import os
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

from krabby_real_estate.traveltime.client import ParcelAnchor, TimeMapSpec, collect_time_maps


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--parcels",
        type=Path,
        required=True,
        help="CSV with parcel_id/anchor_id/latitude/longitude",
    )
    parser.add_argument(
        "--direction", action="append", choices=("departure", "arrival"), required=True
    )
    parser.add_argument("--transportation", default="walking")
    parser.add_argument("--travel-time-seconds", type=int, default=3600)
    parser.add_argument("--reference-time", required=True, help="Timezone-aware ISO-8601 timestamp")
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def read_parcels(path: Path) -> list[ParcelAnchor]:
    with path.open(newline="") as handle:
        return [
            ParcelAnchor(
                parcel_id=row["parcel_id"],
                anchor_id=row["anchor_id"],
                latitude=float(row["latitude"]),
                longitude=float(row["longitude"]),
            )
            for row in csv.DictReader(handle)
        ]


def main():
    load_dotenv()
    args = parse_args()
    reference_time = datetime.fromisoformat(args.reference_time)
    parcels = read_parcels(args.parcels)
    specs = [
        TimeMapSpec(
            direction=direction,
            transportation=args.transportation,
            travel_time_seconds=args.travel_time_seconds,
            reference_time=reference_time,
        )
        for direction in args.direction
    ]
    feature_collection, manifest = collect_time_maps(
        parcels,
        specs,
        app_id=os.environ.get("TRAVELTIME_APP_ID", ""),
        api_key=os.environ.get("TRAVELTIME_API_KEY", ""),
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(feature_collection) + "\n")
    manifest_path = args.output.with_suffix(".manifest.json")
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")


if __name__ == "__main__":
    main()
