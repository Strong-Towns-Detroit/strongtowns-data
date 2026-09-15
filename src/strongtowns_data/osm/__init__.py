"""Prepared OSM source features and routing points. Readers never acquire data."""

from pathlib import Path

import geopandas as gpd

from .features import DEFAULT_POI_TAGS, prepare_features, routing_points

__all__ = ["DEFAULT_POI_TAGS", "prepare_features", "read_features", "read_points", "routing_points"]


def read_features(directory):
    """Read explicitly selected local source geometry, without network access."""
    return gpd.read_parquet(Path(directory) / "raw.parquet")


def read_points(directory):
    """Read explicitly selected local routing points, without network access."""
    return gpd.read_parquet(Path(directory) / "accepted.parquet")
