"""Fetch versioned Detroit Base Units source layers with resumable page caches."""

from __future__ import annotations

import argparse
from pathlib import Path

from krabby_real_estate.base_units.service import LAYERS, fetch_layer


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument(
        "--layer",
        action="append",
        choices=sorted(LAYERS),
        help="Layer to fetch; repeat as needed (default: all)",
    )
    parser.add_argument("--discard-pages", action="store_true")
    return parser.parse_args()


def main():
    args = parse_args()
    for name in args.layer or LAYERS:
        path, manifest = fetch_layer(
            LAYERS[name], args.output_dir, discard_pages=args.discard_pages
        )
        print(f"{name}: {manifest['feature_count']:,} features -> {path}")


if __name__ == "__main__":
    main()
