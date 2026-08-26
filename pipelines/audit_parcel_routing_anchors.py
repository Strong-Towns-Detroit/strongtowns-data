"""Generate QA statistics and review artifacts for citywide parcel routing anchors."""

from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt

from krabby_real_estate.base_units.geometry import normalize_parcel_id
from krabby_real_estate.base_units.qa import audit_anchors, audit_source_relations


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--anchors-gpkg", type=Path, required=True)
    parser.add_argument("--parcels", type=Path, required=True)
    parser.add_argument("--addresses", type=Path, required=True)
    parser.add_argument("--streets", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    return parser.parse_args()


def _read_attributes(path: Path, columns: list[str]):
    return gpd.read_file(path, columns=columns, ignore_geometry=True)


def _write_map(anchors, review, destination: Path):
    fallback = review[review["routing_anchor_method"].eq("nearest_street_front_edge_midpoint")]
    multi = review[review["qa_reasons"].str.contains("multiple_street_anchors")]
    figure, axis = plt.subplots(figsize=(8, 8))
    axis.scatter(anchors.geometry.x, anchors.geometry.y, s=0.08, c="#B8B8B8", alpha=0.12)
    axis.scatter(multi.geometry.x, multi.geometry.y, s=1.5, c="#2364AA", label="multiple anchors")
    axis.scatter(fallback.geometry.x, fallback.geometry.y, s=2, c="#D1495B", label="fallback")
    axis.set_title("Detroit parcel routing-anchor QA")
    axis.set_axis_off()
    axis.legend(loc="lower right", markerscale=4)
    figure.tight_layout()
    figure.savefig(destination, dpi=180)
    plt.close(figure)


def main():
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    anchors = gpd.read_file(args.anchors_gpkg, layer="anchors")
    parcels = _read_attributes(
        args.parcels,
        [
            "parcel_id",
            "address",
            "is_improved",
            "num_buildings",
            "property_class_description",
        ],
    )
    addresses = _read_attributes(args.addresses, ["parcel_id", "street_id"])
    streets = _read_attributes(args.streets, ["street_id"])

    source_report = audit_source_relations(parcels, addresses, streets)
    parcel_details = parcels.copy()
    parcel_details["parcel_key"] = parcel_details["parcel_id"].map(normalize_parcel_id)
    parcel_details = parcel_details.rename(columns={"address": "parcel_address"}).drop(
        columns="parcel_id"
    )
    anchors = anchors.merge(parcel_details, on="parcel_key", how="left", validate="many_to_one")
    anchor_report, review = audit_anchors(anchors)
    review_path = args.output_dir / "parcel-routing-anchor-review.gpkg"
    temporary_review = review_path.with_name(f"{review_path.stem}.tmp{review_path.suffix}")
    temporary_review.unlink(missing_ok=True)
    review.to_file(temporary_review, layer="review_anchors", driver="GPKG")
    distance_outliers = review.sort_values("edge_to_street_distance_ft", ascending=False).head(250)
    distance_outliers.to_file(temporary_review, layer="distance_outliers", driver="GPKG")
    temporary_review.replace(review_path)
    review.drop(columns="geometry").to_csv(
        args.output_dir / "parcel-routing-anchor-review.csv", index=False
    )
    distance_outliers.drop(columns="geometry").to_csv(
        args.output_dir / "parcel-routing-anchor-distance-outliers.csv", index=False
    )
    _write_map(anchors, review, args.output_dir / "parcel-routing-anchor-qa.png")
    report = {
        "generated_at": datetime.now(UTC).isoformat(),
        "source_relations": source_report,
        "anchors": anchor_report,
    }
    report_path = args.output_dir / "parcel-routing-anchor-qa.json"
    report_path.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
