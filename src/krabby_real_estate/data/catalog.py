"""Krabby's explicit Contract-v1 asset and pipeline catalog."""

from __future__ import annotations

from pathlib import Path

import pyarrow as pa

from krabby_real_estate.data.model import (
    AcquisitionPolicy,
    DataAsset,
    DatasetContract,
    PipelineDefinition,
    Tier,
)
from krabby_real_estate.data.registry import AssetRegistry
from krabby_real_estate.data.table_validation import (
    conditional_required_validator,
    enum_validator,
    range_validator,
)

STRING = pa.string()
GEOMETRY = pa.binary()

RAW_CONTRACT = DatasetContract("raw-source-v1", "1.0.0")

PARCEL_SCHEMA = pa.schema(
    [
        pa.field("parcel_id", STRING, nullable=False),
        pa.field("parcel_key", STRING, nullable=False),
        pa.field("source_object_id", STRING, nullable=False),
        pa.field("geometry", GEOMETRY, nullable=False),
    ]
)
ADDRESS_SCHEMA = pa.schema(
    [
        pa.field("address_id", STRING, nullable=False),
        pa.field("source_object_id", STRING, nullable=False),
        pa.field("parcel_id", STRING),
        pa.field("parcel_key", STRING),
        pa.field("street_id", STRING),
        pa.field("building_id", STRING),
        pa.field("geometry", GEOMETRY),
    ]
)
STREET_SCHEMA = pa.schema(
    [
        pa.field("street_id", STRING, nullable=False),
        pa.field("source_object_id", STRING, nullable=False),
        pa.field("full_street_name", STRING),
        pa.field("geometry", GEOMETRY, nullable=False),
    ]
)
BUILDING_SCHEMA = pa.schema(
    [
        pa.field("building_id", STRING, nullable=False),
        pa.field("source_object_id", STRING, nullable=False),
        pa.field("parcel_id", STRING),
        pa.field("parcel_key", STRING),
        pa.field("status", STRING),
        pa.field("geometry", GEOMETRY, nullable=False),
    ]
)
POI_SCHEMA = pa.schema(
    [
        pa.field("poi_uuid", STRING, nullable=False),
        pa.field("poi_id", STRING, nullable=False),
        pa.field("source", STRING, nullable=False),
        pa.field("source_element_type", STRING, nullable=False),
        pa.field("source_id", STRING, nullable=False),
        pa.field("name", STRING),
        pa.field(
            "categories",
            pa.list_(pa.struct([pa.field("key", STRING), pa.field("value", STRING)])),
            nullable=False,
        ),
        pa.field(
            "source_tags",
            pa.list_(pa.struct([pa.field("key", STRING), pa.field("value", STRING)])),
            nullable=False,
        ),
        pa.field("source_geometry_type", STRING, nullable=False),
        pa.field("routing_point_method", STRING, nullable=False),
        pa.field("routing_point_status", STRING, nullable=False),
        pa.field("longitude", pa.float64(), nullable=False),
        pa.field("latitude", pa.float64(), nullable=False),
        pa.field("source_geometry", GEOMETRY, nullable=False),
        pa.field("geometry", GEOMETRY, nullable=False),
    ]
)
ANCHOR_SCHEMA = pa.schema(
    [
        pa.field("anchor_uuid", STRING, nullable=False),
        pa.field("parcel_id", STRING, nullable=False),
        pa.field("parcel_key", STRING, nullable=False),
        pa.field("street_id", STRING, nullable=False),
        pa.field("routing_anchor_method", STRING, nullable=False),
        pa.field("frontage_source", STRING, nullable=False),
        pa.field("frontage_confidence", STRING, nullable=False),
        pa.field("anchor_confidence", STRING, nullable=False),
        pa.field("geometry_frontage_ft", pa.float64(), nullable=False),
        pa.field("edge_to_street_distance_ft", pa.float64(), nullable=False),
        pa.field("angle_difference_degrees", pa.float64(), nullable=False),
        pa.field("linked_current_building_count", pa.int64()),
        pa.field("longitude", pa.float64(), nullable=False),
        pa.field("latitude", pa.float64(), nullable=False),
        pa.field("geometry", GEOMETRY, nullable=False),
    ]
)
EVIDENCE_SCHEMA = pa.schema(
    [
        pa.field("anchor_uuid", STRING, nullable=False),
        pa.field("address_id", STRING, nullable=False),
        pa.field("source_object_id", STRING, nullable=False),
    ]
)
FRONTAGE_SCHEMA = pa.schema(
    [
        pa.field("anchor_uuid", STRING, nullable=False),
        pa.field("geometry", GEOMETRY, nullable=False),
    ]
)
DISPOSITION_SCHEMA = pa.schema(
    [
        pa.field("anchor_uuid", STRING, nullable=False),
        pa.field("review_status", STRING, nullable=False),
        pa.field("review_reasons", pa.list_(STRING), nullable=False),
        pa.field("reviewer", STRING),
        pa.field("reviewed_at", pa.timestamp("us", tz="UTC")),
        pa.field("evidence_uri", STRING),
        pa.field("notes", STRING),
    ]
)
BLOCKED_SCHEMA = pa.schema(
    [
        pa.field("parcel_id", STRING, nullable=False),
        pa.field("parcel_key", STRING, nullable=False),
        pa.field("reason", STRING, nullable=False),
    ]
)
REQUEST_SCHEMA = pa.schema(
    [
        pa.field("request_uuid", STRING, nullable=False),
        pa.field("provider_search_id", STRING, nullable=False),
        pa.field("anchor_uuid", STRING, nullable=False),
        pa.field("parcel_id", STRING, nullable=False),
        pa.field("direction", STRING, nullable=False),
        pa.field("transportation", STRING, nullable=False),
        pa.field("travel_time_seconds", pa.int64(), nullable=False),
        pa.field("reference_time_utc", pa.timestamp("us", tz="UTC"), nullable=False),
        pa.field("latitude", pa.float64(), nullable=False),
        pa.field("longitude", pa.float64(), nullable=False),
        pa.field("selection_override", pa.bool_(), nullable=False),
    ]
)
RESULT_SCHEMA = pa.schema(
    [
        pa.field("request_uuid", STRING, nullable=False),
        pa.field("provider_search_id", STRING, nullable=False),
        pa.field("result_status", STRING, nullable=False),
        pa.field("provider_error_code", STRING),
        pa.field("provider_error_message", STRING),
        pa.field("received_at", pa.timestamp("us", tz="UTC"), nullable=False),
        pa.field("geometry", GEOMETRY),
    ]
)


def _contract(
    contract_id,
    schema,
    primary_key,
    *,
    geometry=False,
    geometry_types=(),
    foreign_keys=None,
    validators=(),
):
    return DatasetContract(
        contract_id,
        "1.0.0",
        schema,
        tuple(primary_key),
        foreign_keys=foreign_keys or {},
        geometry_column="geometry" if geometry else None,
        geometry_types=tuple(geometry_types),
        crs="EPSG:4326" if geometry else None,
        validators=tuple(validators),
    )


def build_registry() -> AssetRegistry:
    result = AssetRegistry()
    assets = [
        DataAsset(
            "detroit.parcels.raw",
            Tier.SOURCE,
            "application/geo+json",
            RAW_CONTRACT,
            Path("data/sources/detroit.parcels.raw"),
            acquisition_policy=AcquisitionPolicy.NETWORK,
        ),
        DataAsset(
            "detroit.base-units.addresses.raw",
            Tier.SOURCE,
            "application/geo+json",
            RAW_CONTRACT,
            Path("data/sources/detroit.base-units.addresses.raw"),
            acquisition_policy=AcquisitionPolicy.NETWORK,
        ),
        DataAsset(
            "detroit.base-units.streets.raw",
            Tier.SOURCE,
            "application/geo+json",
            RAW_CONTRACT,
            Path("data/sources/detroit.base-units.streets.raw"),
            acquisition_policy=AcquisitionPolicy.NETWORK,
        ),
        DataAsset(
            "detroit.base-units.buildings.raw",
            Tier.SOURCE,
            "application/geo+json",
            RAW_CONTRACT,
            Path("data/sources/detroit.base-units.buildings.raw"),
            acquisition_policy=AcquisitionPolicy.NETWORK,
        ),
        DataAsset(
            "osm.detroit.pois.raw",
            Tier.SOURCE,
            "application/geo+json",
            RAW_CONTRACT,
            Path("data/sources/osm.detroit.pois.raw"),
            acquisition_policy=AcquisitionPolicy.NETWORK,
        ),
        DataAsset(
            "detroit.parcels",
            Tier.SOURCE,
            "application/vnd.apache.geoparquet",
            _contract("detroit-parcels-v1", PARCEL_SCHEMA, ["parcel_key"], geometry=True),
            Path("data/sources/detroit.parcels"),
            "canonicalize.parcels",
        ),
        DataAsset(
            "detroit.base-units.addresses",
            Tier.SOURCE,
            "application/vnd.apache.geoparquet",
            _contract("detroit-addresses-v1", ADDRESS_SCHEMA, ["address_id"], geometry=True),
            Path("data/sources/detroit.base-units.addresses"),
            "canonicalize.addresses",
        ),
        DataAsset(
            "detroit.base-units.streets",
            Tier.SOURCE,
            "application/vnd.apache.geoparquet",
            _contract("detroit-streets-v1", STREET_SCHEMA, ["street_id"], geometry=True),
            Path("data/sources/detroit.base-units.streets"),
            "canonicalize.streets",
        ),
        DataAsset(
            "detroit.base-units.buildings",
            Tier.SOURCE,
            "application/vnd.apache.geoparquet",
            _contract("detroit-buildings-v1", BUILDING_SCHEMA, ["building_id"], geometry=True),
            Path("data/sources/detroit.base-units.buildings"),
            "canonicalize.buildings",
        ),
        DataAsset(
            "osm.detroit.pois",
            Tier.SOURCE,
            "application/vnd.apache.geoparquet",
            _contract(
                "osm-pois-v1",
                POI_SCHEMA,
                ["poi_uuid"],
                geometry=True,
                geometry_types=("Point",),
                validators=(
                    enum_validator(
                        "routing_point_method", ("source_point", "representative_point")
                    ),
                    enum_validator("routing_point_status", ("ready", "review_required")),
                    range_validator("longitude", -180, 180),
                    range_validator("latitude", -90, 90),
                ),
            ),
            Path("data/sources/osm.detroit.pois"),
            "canonicalize.osm-pois",
        ),
        DataAsset(
            "detroit.parcel-routing-anchors",
            Tier.DERIVED,
            "application/vnd.apache.geoparquet",
            _contract(
                "parcel-routing-anchors-v1",
                ANCHOR_SCHEMA,
                ["anchor_uuid"],
                geometry=True,
                geometry_types=("Point",),
                validators=(
                    enum_validator(
                        "routing_anchor_method",
                        (
                            "address_linked_front_edge_projection",
                            "address_linked_front_edge_midpoint",
                            "nearest_street_front_edge_midpoint",
                        ),
                    ),
                    enum_validator(
                        "frontage_confidence", ("high", "medium", "low", "not_evaluated")
                    ),
                    enum_validator("anchor_confidence", ("high", "medium", "low", "not_evaluated")),
                    range_validator("longitude", -180, 180),
                    range_validator("latitude", -90, 90),
                ),
            ),
            Path("data/derived/detroit.parcel-routing-anchors"),
            "derive.parcel-routing",
        ),
        DataAsset(
            "detroit.anchor-address-evidence",
            Tier.DERIVED,
            "application/vnd.apache.parquet",
            _contract(
                "anchor-address-evidence-v1",
                EVIDENCE_SCHEMA,
                ["anchor_uuid", "address_id"],
                foreign_keys={
                    ("anchor_uuid",): ("detroit.parcel-routing-anchors", ("anchor_uuid",)),
                    ("address_id",): ("detroit.base-units.addresses", ("address_id",)),
                },
            ),
            Path("data/derived/detroit.anchor-address-evidence"),
            "derive.parcel-routing",
        ),
        DataAsset(
            "detroit.anchor-frontages",
            Tier.DERIVED,
            "application/vnd.apache.geoparquet",
            _contract(
                "anchor-frontages-v1",
                FRONTAGE_SCHEMA,
                ["anchor_uuid"],
                geometry=True,
                geometry_types=("LineString", "MultiLineString"),
                foreign_keys={
                    ("anchor_uuid",): ("detroit.parcel-routing-anchors", ("anchor_uuid",))
                },
            ),
            Path("data/derived/detroit.anchor-frontages"),
            "derive.parcel-routing",
        ),
        DataAsset(
            "detroit.anchor-dispositions",
            Tier.DERIVED,
            "application/vnd.apache.parquet",
            _contract(
                "anchor-dispositions-v1",
                DISPOSITION_SCHEMA,
                ["anchor_uuid"],
                foreign_keys={
                    ("anchor_uuid",): ("detroit.parcel-routing-anchors", ("anchor_uuid",))
                },
                validators=(
                    enum_validator(
                        "review_status", ("not_required", "required", "approved", "rejected")
                    ),
                    conditional_required_validator(
                        "review_status",
                        ("approved", "rejected"),
                        ("reviewer", "reviewed_at"),
                    ),
                ),
            ),
            Path("data/derived/detroit.anchor-dispositions"),
            "derive.parcel-routing",
        ),
        DataAsset(
            "detroit.blocked-routing-parcels",
            Tier.DERIVED,
            "application/vnd.apache.parquet",
            _contract("blocked-routing-parcels-v1", BLOCKED_SCHEMA, ["parcel_key"]),
            Path("data/derived/detroit.blocked-routing-parcels"),
            "derive.parcel-routing",
        ),
        DataAsset(
            "traveltime.requests",
            Tier.PROVIDER,
            "application/vnd.apache.parquet",
            _contract(
                "traveltime-requests-v1",
                REQUEST_SCHEMA,
                ["request_uuid"],
                foreign_keys={
                    ("anchor_uuid",): ("detroit.parcel-routing-anchors", ("anchor_uuid",))
                },
                validators=(
                    enum_validator("direction", ("arrival", "departure")),
                    range_validator("travel_time_seconds", 1, 3600),
                    range_validator("longitude", -180, 180),
                    range_validator("latitude", -90, 90),
                ),
            ),
            Path("data/provider/traveltime.requests"),
            "prepare.traveltime-requests",
            acquisition_policy=AcquisitionPolicy.OFFLINE,
        ),
        DataAsset(
            "traveltime.results",
            Tier.PROVIDER,
            "application/vnd.apache.geoparquet",
            _contract(
                "traveltime-results-v1",
                RESULT_SCHEMA,
                ["request_uuid"],
                geometry=True,
                geometry_types=("Polygon", "MultiPolygon"),
                foreign_keys={("request_uuid",): ("traveltime.requests", ("request_uuid",))},
                validators=(enum_validator("result_status", ("success", "error")),),
            ),
            Path("data/provider/traveltime.results"),
            "collect.traveltime-results",
            acquisition_policy=AcquisitionPolicy.PAID,
        ),
    ]
    for asset in assets:
        result.register_asset(asset)
    pipelines = [
        PipelineDefinition("canonicalize.parcels", ("detroit.parcels.raw",), ("detroit.parcels",)),
        PipelineDefinition(
            "canonicalize.addresses",
            ("detroit.base-units.addresses.raw",),
            ("detroit.base-units.addresses",),
        ),
        PipelineDefinition(
            "canonicalize.streets",
            ("detroit.base-units.streets.raw",),
            ("detroit.base-units.streets",),
        ),
        PipelineDefinition(
            "canonicalize.buildings",
            ("detroit.base-units.buildings.raw",),
            ("detroit.base-units.buildings",),
        ),
        PipelineDefinition(
            "canonicalize.osm-pois", ("osm.detroit.pois.raw",), ("osm.detroit.pois",)
        ),
        PipelineDefinition(
            "derive.parcel-routing",
            (
                "detroit.parcels",
                "detroit.base-units.addresses",
                "detroit.base-units.streets",
                "detroit.base-units.buildings",
            ),
            (
                "detroit.parcel-routing-anchors",
                "detroit.anchor-address-evidence",
                "detroit.anchor-frontages",
                "detroit.anchor-dispositions",
                "detroit.blocked-routing-parcels",
            ),
        ),
        PipelineDefinition(
            "prepare.traveltime-requests",
            ("detroit.parcel-routing-anchors", "detroit.anchor-dispositions"),
            ("traveltime.requests",),
        ),
        PipelineDefinition(
            "collect.traveltime-results", ("traveltime.requests",), ("traveltime.results",)
        ),
    ]
    for pipeline in pipelines:
        result.register_pipeline(pipeline)
    result.validate()
    return result


catalog = build_registry()
