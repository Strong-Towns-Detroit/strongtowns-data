"""Registered OSM schema-2 pipelines; schema-1 assets remain separately resolvable."""

from pathlib import Path

import geopandas as gpd

from strongtowns_data.models import (
    AcquisitionPolicy,
    ArchiveTier,
    BuildMetadata,
    DataAsset,
    DataPipeline,
    DatasetModel,
)
from strongtowns_data.pipelines.registry import data_pipeline

from .features import POINT_COLUMNS, SOURCE_COLUMNS, prepare_features, routing_points


def validate_source(directory, manifest):
    from .acquisition import validate_acquisition

    validate_acquisition(directory)
    source = gpd.read_parquet(directory / "raw.parquet")
    accepted, rejected = prepare_features(source)
    if len(accepted) != len(source) or len(rejected):
        raise ValueError("Invalid accepted OSM source features")


def _asset(identity, directory, *, points=False):
    return DataAsset(
        identity,
        Path("data/datasets") / directory,
        DatasetModel(
            identity,
            "2.0.0",
            required_columns=dict.fromkeys(POINT_COLUMNS if points else SOURCE_COLUMNS, "string"),
            primary_key=("source_id",),
            allowed_values={"osm_type": ("node", "way", "relation")},
            geometry_types=("Point",)
            if points
            else (
                "Point",
                "MultiPoint",
                "LineString",
                "MultiLineString",
                "Polygon",
                "MultiPolygon",
            ),
            crs="EPSG:4326",
            accepted_artifact="accepted.parquet" if points else "raw.parquet",
            rejects_artifact="rejects.parquet",
            custom_validator=None if points else validate_source,
        ),
        ArchiveTier.DELIVERABLE if points else ArchiveTier.SOURCE,
    )


POIS_RAW = _asset("detroit.osm.pois.raw.v2", "detroit-osm-pois-source-v2")
POIS = _asset("detroit.osm.pois.v2", "detroit-osm-pois-v2", points=True)


def fetch_pois(context):
    from .acquisition import collect_pois

    metadata = collect_pois(
        context.staging[POIS_RAW.id], cache_root=context.root / "data/.cache/osm"
    )
    counts = {key: metadata.pop(key) for key in ("input", "accepted", "rejected")}
    return {
        POIS_RAW.id: BuildMetadata(
            counts=counts, source=metadata, transaction_quality="best_effort"
        )
    }


def build_pois(context):
    source = gpd.read_parquet(context.inputs[POIS_RAW.id] / "raw.parquet")
    points, rejected = routing_points(source)
    out = context.staging[POIS.id]
    points.to_parquet(out / "accepted.parquet", index=False)
    rejected.to_parquet(out / "rejects.parquet", index=False)
    return {
        POIS.id: BuildMetadata(
            counts={"input": len(source), "accepted": len(points), "rejected": len(rejected)},
            parameters={
                "routing_interpretation": "osm-poi-v2",
                "category_precedence": ["amenity", "shop", "office", "tourism", "leisure", "craft"],
            },
        )
    }


@data_pipeline("detroit-osm-pois-source-v2")
def detroit_osm_pois_source_v2():
    return DataPipeline(
        "detroit-osm-pois-source-v2",
        (),
        (POIS_RAW,),
        fetch=fetch_pois,
        acquisition_policy=AcquisitionPolicy.PUBLIC_NETWORK,
        description="OSM POI source geometries, all returned tags and response evidence.",
    )


@data_pipeline("canonical-detroit-osm-pois-v2")
def canonical_detroit_osm_pois_v2():
    return DataPipeline(
        "canonical-detroit-osm-pois-v2",
        (POIS_RAW.id,),
        (POIS,),
        build=build_pois,
        description="Offline routing points derived from schema-2 OSM source evidence.",
    )
