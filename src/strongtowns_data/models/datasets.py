"""Built-in dataset definitions."""

from pathlib import Path

from strongtowns_data.pipelines.catalog import validate_query_catalog_snapshot

from . import ArchiveTier, DataAsset, DatasetModel


def raw_model(name: str) -> DatasetModel:
    return DatasetModel(name=name, version="1.0.0")


def geo_model(
    name: str, primary_key: str, geometry_types: tuple[str, ...]
) -> DatasetModel:
    return DatasetModel(
        name=name,
        version="1.0.0",
        required_columns={primary_key: "string", "source_row": "int64"},
        primary_key=(primary_key,),
        geometry_types=geometry_types,
        crs="EPSG:4326",
        accepted_artifact="accepted.parquet",
        rejects_artifact="rejects.parquet",
    )


def canonical_asset(
    asset_id: str, directory: str, primary_key: str, geometry_types: tuple[str, ...]
) -> DataAsset:
    return DataAsset(
        asset_id,
        Path("data/datasets") / directory,
        geo_model(asset_id, primary_key, geometry_types),
    )


def legacy_source_asset(
    asset_id: str,
    directory: str,
    legacy: dict[str, str],
    *,
    tier: ArchiveTier,
    counts: dict[str, int],
) -> DataAsset:
    return DataAsset(
        asset_id,
        Path("data/datasets") / f"{directory}-source",
        raw_model(asset_id),
        tier,
        legacy_artifacts={name: Path(path) for name, path in legacy.items()},
        legacy_counts=counts,
    )


PARCELS_RAW = DataAsset(
    "detroit.parcels.raw",
    Path("data/datasets/detroit-parcels-source"),
    raw_model("detroit.parcels.raw"),
    ArchiveTier.SOURCE,
    legacy_artifacts={"raw.geojson": Path("pipelines/parcel-data/Parcels.geojson")},
    legacy_counts={"records": 378_366},
)
ADDRESSES_RAW = DataAsset(
    "detroit.base-units.addresses.raw",
    Path("data/datasets/detroit-base-units-addresses-source"),
    raw_model("detroit.base-units.addresses.raw"),
    ArchiveTier.SOURCE,
    legacy_artifacts={
        "raw.geojson": Path(
            "projects/detroit-land-use-forum/base-units-geometry/data/base_units_addresses.geojson"
        )
    },
    legacy_counts={"records": 486_540},
)
STREETS_RAW = DataAsset(
    "detroit.base-units.streets.raw",
    Path("data/datasets/detroit-base-units-streets-source"),
    raw_model("detroit.base-units.streets.raw"),
    ArchiveTier.SOURCE,
    legacy_artifacts={
        "raw.geojson": Path(
            "projects/detroit-land-use-forum/base-units-geometry/data/base_units_streets.geojson"
        )
    },
    legacy_counts={"records": 36_104},
)
BUILDINGS_RAW = DataAsset(
    "detroit.base-units.buildings.raw",
    Path("data/datasets/detroit-base-units-buildings-source"),
    raw_model("detroit.base-units.buildings.raw"),
    ArchiveTier.SOURCE,
    legacy_artifacts={
        "raw.geojson": Path(
            "projects/detroit-land-use-forum/base-units-geometry/data/base_units_buildings.geojson"
        )
    },
    legacy_counts={"records": 364_095},
)
ASSESSMENTS_RAW = DataAsset(
    "detroit.assessments.raw",
    Path("data/datasets/detroit-assessments-source"),
    raw_model("detroit.assessments.raw"),
    ArchiveTier.SOURCE,
)
LVT_2023_RAW = DataAsset(
    "detroit.lvt-estimator-2023.raw",
    Path("data/datasets/detroit-lvt-estimator-2023-source"),
    raw_model("detroit.lvt-estimator-2023.raw"),
    ArchiveTier.SOURCE,
)

PARCELS = canonical_asset(
    "detroit.parcels", "detroit-parcels", "parcel_id", ("Polygon", "MultiPolygon")
)
ADDRESSES = canonical_asset(
    "detroit.base-units.addresses", "detroit-base-units-addresses", "address_id", ("Point",)
)
STREETS = canonical_asset(
    "detroit.base-units.streets", "detroit-base-units-streets", "street_id",
    ("LineString", "MultiLineString"),
)
BUILDINGS = canonical_asset(
    "detroit.base-units.buildings", "detroit-base-units-buildings", "building_id",
    ("Polygon", "MultiPolygon"),
)
ASSESSMENTS = DataAsset(
    "detroit.assessments",
    Path("data/datasets/detroit-assessments"),
    DatasetModel(
        "detroit.assessments",
        "1.0.0",
        required_columns={
            "source_row": "int64",
            "assessment_roll_year": "int64",
            "object_id": "int64",
            "parcel_id": "string",
            "assessed_value": "double",
            "taxable_value": "double",
            "true_cash_value": "double",
            "land_value": "double",
            "parcel_area_sqft": "double",
            "landmap": "string",
        },
        primary_key=("object_id",),
        accepted_artifact="accepted.parquet",
        rejects_artifact="rejects.parquet",
    ),
    ArchiveTier.SOURCE,
)
LVT_2023 = DataAsset(
    "detroit.lvt-estimator-2023",
    Path("data/datasets/detroit-lvt-estimator-2023"),
    DatasetModel(
        "detroit.lvt-estimator-2023",
        "1.0.0",
        required_columns={
            "source_row": "int64", "object_id": "int64", "parcel_id": "string",
            "property_class": "int64", "taxable_value": "double",
            "assessed_land_value": "double", "taxable_land_value": "double",
            "tax_classification": "string",
        },
        primary_key=("object_id",),
        accepted_artifact="accepted.parquet",
        rejects_artifact="rejects.parquet",
    ),
    ArchiveTier.SOURCE,
)
PARCEL_LAND_VALUES = DataAsset(
    "detroit.parcel-land-values",
    Path("data/datasets/detroit-parcel-land-values"),
    DatasetModel(
        "detroit.parcel-land-values",
        "1.0.0",
        required_columns={
            "object_id": "int64", "parcel_id": "string",
            "assessment_roll_year": "int64", "property_class": "string",
            "landmap": "string", "parcel_area_sqft": "double",
            "true_cash_value": "double", "taxable_value": "double",
            "official_land_rate": "double", "official_land_value": "double",
            "official_taxable_land_value": "double",
            "smoothed_land_rate": "double", "smoothed_land_value": "double",
            "smoothed_taxable_land_value": "double",
            "taxable_land_allocation_status": "string",
            "smoothed_land_value_was_capped": "bool",
            "local_median_land_rate": "double",
            "local_deviation_factor": "double",
            "local_peer_count": "int64",
            "local_neighbor_distance_m": "double",
            "isolated_spike_candidate": "bool",
            "smoothing_applied": "bool",
            "land_value_method": "string",
        },
        primary_key=("object_id",),
        accepted_artifact="accepted.parquet",
    ),
    ArchiveTier.DELIVERABLE,
)

QUERY_CATALOG = DataAsset(
    "detroit.query.catalog",
    Path("data/datasets/detroit-query-catalog"),
    DatasetModel(
        "detroit.query.catalog", "1.0.0",
        custom_validator=validate_query_catalog_snapshot,
    ),
)

ANCHORS = DataAsset(
    "detroit.routing.anchors",
    Path("data/datasets/detroit-routing-anchors"),
    DatasetModel(
        "detroit.routing.anchors", "1.0.0",
        required_columns={
            "anchor_id": "string", "parcel_id": "string", "parcel_key": "string",
            "street_key": "string", "method": "string", "review_status": "string",
            "street_distance_ft": "double", "parcel_boundary_distance_ft": "double",
        },
        allowed_values={
            "method": ("linked_address", "nearest_street_fallback"),
            "review_status": ("not_required", "required", "approved", "rejected"),
        },
        primary_key=("anchor_id",), geometry_types=("Point",), crs="EPSG:4326",
        accepted_artifact="accepted.parquet", rejects_artifact="blocked.parquet",
    ),
)
FRONTAGES = DataAsset(
    "detroit.routing.frontages",
    Path("data/datasets/detroit-routing-frontages"),
    DatasetModel(
        "detroit.routing.frontages", "1.0.0",
        required_columns={
            "anchor_id": "string", "frontage_length_ft": "double",
            "street_distance_ft": "double", "angle_difference": "double",
        },
        primary_key=("anchor_id",), geometry_types=("LineString",), crs="EPSG:4326",
        accepted_artifact="accepted.parquet",
    ),
)
EVIDENCE = DataAsset(
    "detroit.routing.anchor-evidence",
    Path("data/datasets/detroit-routing-anchor-evidence"),
    DatasetModel(
        "detroit.routing.anchor-evidence", "1.0.0",
        required_columns={
            "evidence_id": "string", "anchor_id": "string", "address_id": "string",
        },
        primary_key=("evidence_id",), accepted_artifact="accepted.parquet",
    ),
)
DISPOSITIONS = DataAsset(
    "detroit.routing.review-dispositions",
    Path("data/datasets/detroit-routing-review-dispositions"),
    DatasetModel(
        "detroit.routing.review-dispositions", "1.0.0",
        required_columns={"anchor_id": "string", "review_status": "string"},
        allowed_values={
            "review_status": ("not_required", "required", "approved", "rejected")
        },
        primary_key=("anchor_id",), accepted_artifact="accepted.parquet",
    ),
)

TRAVELTIME_REQUESTS = DataAsset(
    "detroit.traveltime.requests",
    Path("data/datasets/traveltime-requests"),
    DatasetModel(
        "detroit.traveltime.requests", "1.0.0",
        required_columns={
            "request_id": "string", "provider_search_id": "string",
            "anchor_id": "string", "direction": "string", "mode": "string",
            "horizon_seconds": "int64", "required_override": "bool",
        },
        allowed_values={
            "direction": ("arrival", "departure"),
            "mode": ("walking", "cycling", "driving", "public_transport"),
        },
        primary_key=("request_id",), geometry_types=("Point",), crs="EPSG:4326",
        accepted_artifact="accepted.parquet", rejects_artifact="blocked.parquet",
    ),
)
TRAVELTIME_RESULTS = DataAsset(
    "detroit.traveltime.results",
    Path("data/datasets/traveltime-results"),
    DatasetModel(
        "detroit.traveltime.results", "1.0.0",
        required_columns={
            "request_id": "string", "provider_search_id": "string", "anchor_id": "string",
        },
        primary_key=("request_id",),
        geometry_types=("Polygon", "MultiPolygon"), crs="EPSG:4326",
        accepted_artifact="accepted.parquet", rejects_artifact="errors.parquet",
    ),
    ArchiveTier.CRITICAL,
)

OSM_POIS_RAW = DataAsset(
    "detroit.osm.pois.raw",
    Path("data/datasets/detroit-osm-pois-source"),
    DatasetModel(
        "detroit.osm.pois.raw", "1.0.0",
        required_columns={
            "source_id": "string", "osm_type": "string", "osm_id": "string",
            "tag_keys": "list<element: string>", "tag_values": "list<element: string>",
        },
        primary_key=("source_id",),
        geometry_types=(
            "Point", "MultiPoint", "LineString", "MultiLineString",
            "Polygon", "MultiPolygon",
        ),
        crs="EPSG:4326", accepted_artifact="raw.parquet",
        rejects_artifact="rejects.parquet",
    ),
    ArchiveTier.SOURCE,
)
OSM_POIS = DataAsset(
    "detroit.osm.pois",
    Path("data/datasets/detroit-osm-pois"),
    DatasetModel(
        "detroit.osm.pois", "1.0.0",
        required_columns={
            "source_id": "string", "osm_type": "string", "osm_id": "string",
            "tag_keys": "list<element: string>", "tag_values": "list<element: string>",
            "primary_category": "string", "routing_point_method": "string",
        },
        primary_key=("source_id",), geometry_types=("Point",), crs="EPSG:4326",
        accepted_artifact="accepted.parquet", rejects_artifact="rejects.parquet",
    ),
)

MUNICODE_RAW = legacy_source_asset(
    "detroit.municode.chapter-50.raw", "detroit-municode-chapter-50",
    {"raw": "resources/municode/2025-10-09_job-429936"},
    tier=ArchiveTier.CRITICAL, counts={"files": 153},
)
BZA_MINUTES_RAW = legacy_source_asset(
    "detroit.bza.minutes.raw", "detroit-bza-minutes",
    {"raw": "pipelines/zoning/bza_minutes"},
    tier=ArchiveTier.CRITICAL, counts={"files": 261},
)
BZA_GEMINI_RAW = legacy_source_asset(
    "detroit.bza.gemini.raw", "detroit-bza-gemini",
    {"raw": "pipelines/zoning/bza_dataset_gemini"},
    tier=ArchiveTier.CRITICAL, counts={"files": 798},
)
ASSESSMENT_REPORTS_RAW = legacy_source_asset(
    "michigan.assessment-history.reports.raw", "michigan-assessment-history-reports",
    {"raw": "pipelines/assessment-history/data/pdf"},
    tier=ArchiveTier.SOURCE, counts={"files": 58},
)
PARCEL_ATTRIBUTES_RAW = legacy_source_asset(
    "detroit.parcels.attributes.raw", "detroit-parcel-attributes",
    {"raw.csv": "pipelines/parcel-data/parcel-data.csv"},
    tier=ArchiveTier.SOURCE, counts={"records": 378_366},
)
LIHTC_QCT_RAW = legacy_source_asset(
    "hud.lihtc.qct-2026-wayne.raw", "hud-lihtc-qct-2026-wayne",
    {"raw.geojson": "data/lihtc/qct_2026_wayne.geojson"},
    tier=ArchiveTier.SOURCE, counts={"files": 1},
)
DETROIT_BASEMAP_RAW = legacy_source_asset(
    "detroit.osm.basemap.raw", "detroit-osm-basemap",
    {
        "detroit_boundary.geojson": "pipelines/housingDataAnalysis/street_simplification/output/detroit_boundary.geojson",
        "detroit_water.geojson": "pipelines/housingDataAnalysis/street_simplification/output/detroit_water.geojson",
    },
    tier=ArchiveTier.SOURCE, counts={"files": 2},
)
SPIRIT_TRAVELTIME_RAW = legacy_source_asset(
    "detroit.spirit-plaza.traveltime.raw", "detroit-spirit-plaza-traveltime",
    {"raw": "projects/detroit-land-use-forum/spirit-plaza-accessibility/output/raw"},
    tier=ArchiveTier.CRITICAL, counts={"files": 180},
)
