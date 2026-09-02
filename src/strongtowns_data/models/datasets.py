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
    sha256: dict[str, str] | None = None,
) -> DataAsset:
    return DataAsset(
        asset_id,
        Path("data/datasets") / f"{directory}-source",
        raw_model(asset_id),
        tier,
        legacy_artifacts={name: Path(path) for name, path in legacy.items()},
        legacy_counts=counts,
        legacy_sha256=sha256 or {},
    )


def validate_spirit_plaza_accessibility(directory: Path, _manifest) -> None:
    import geopandas as gpd

    isochrones = gpd.read_file(directory / "display_isochrones.geojson")
    roads = gpd.read_file(directory / "road_context.geojson")
    if len(isochrones) != 15:
        raise ValueError("Spirit Plaza accessibility must contain 15 isochrones")
    if set(isochrones["mode"]) != {"driving", "public_transport", "walking"}:
        raise ValueError("Spirit Plaza accessibility has unexpected travel modes")
    if set(isochrones["minutes"]) != {5, 10, 15, 20, 30}:
        raise ValueError("Spirit Plaza accessibility has unexpected minute bands")
    if set(roads["road_class"]) - {"arterial", "major", "local"}:
        raise ValueError("Spirit Plaza road context has unexpected road classes")
    for name, frame in (("isochrones", isochrones), ("roads", roads)):
        if frame.crs is None or frame.crs.to_epsg() != 4326:
            raise ValueError(f"Spirit Plaza {name} must use EPSG:4326")
        if not frame.geometry.is_valid.all():
            raise ValueError(f"Spirit Plaza {name} contains invalid geometry")


def validate_parking_audit(directory: Path, _manifest) -> None:
    import pandas as pd

    frame = pd.read_csv(directory / "parking-case-audit.csv")
    required = {
        "case_history_id", "final_outcome", "required_spaces", "proposed_spaces",
        "numeric_status", "shortfall_spaces", "shortfall_share",
    }
    missing = required - set(frame.columns)
    if missing:
        raise ValueError(f"parking audit is missing columns: {sorted(missing)}")
    if len(frame) != 62 or frame["case_history_id"].duplicated().any():
        raise ValueError("parking audit must contain 62 unique case histories")
    explicit = frame[frame["numeric_status"].eq("explicit_pair")]
    if len(explicit) != 35:
        raise ValueError("parking audit must contain 35 explicit numeric pairs")
    if (explicit["required_spaces"] <= 0).any():
        raise ValueError("parking requirements must be positive")
    if (explicit["proposed_spaces"] < 0).any():
        raise ValueError("proposed parking cannot be negative")
    if (explicit["proposed_spaces"] > explicit["required_spaces"]).any():
        raise ValueError("proposed parking cannot exceed the relief requirement")


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
SPIRIT_PRESENTATION_RAW = legacy_source_asset(
    "detroit.spirit-plaza.presentation.raw", "detroit-spirit-plaza-presentation",
    {
        "display_isochrones.geojson": (
            "projects/detroit-land-use-forum/spirit-plaza-accessibility/output/"
            "display_isochrones.geojson"
        ),
        "road_context.geojson": (
            "projects/detroit-land-use-forum/spirit-plaza-accessibility/output/"
            "road_context.geojson"
        ),
    },
    tier=ArchiveTier.CRITICAL,
    counts={"files": 2},
    sha256={
        "display_isochrones.geojson": "decfcf57a51e98bc3d273fa888f5a5d07d0f61d79501c2128c05e94faa72165f",
        "road_context.geojson": "a23718d25e52642b87e10436e3014c526917738693a473591b00d1d276ef2580",
    },
)
PARKING_REQUIREMENTS_RAW = legacy_source_asset(
    "detroit.bza.parking-requirements.raw", "detroit-bza-parking-requirements",
    {
        "parking-case-audit.csv": (
            "projects/detroit-land-use-forum/parking-requirements/output/"
            "parking-case-audit.csv"
        )
    },
    tier=ArchiveTier.CRITICAL,
    counts={"records": 62},
    sha256={
        "parking-case-audit.csv": "6905cf113e4f3db61b479a04827cc4871b26ef6998bb4817fede248abdb766e8"
    },
)
SETBACK_RESULTS_RAW = legacy_source_asset(
    "detroit.residential-setback-results.raw", "detroit-residential-setback-results",
    {
        "single-family-setback-results.csv": (
            "projects/detroit-land-use-forum/parcel-geometry/output/"
            "single-family-setback-results.csv"
        ),
        "two-family-setback-results.csv": (
            "projects/detroit-land-use-forum/parcel-geometry/output/"
            "two-family-setback-results.csv"
        ),
        "principal_building_site_audit.csv": (
            "projects/detroit-land-use-forum/base-units-geometry/output/"
            "principal_building_site_audit.csv"
        ),
    },
    tier=ArchiveTier.CRITICAL,
    counts={"files": 3},
    sha256={
        "single-family-setback-results.csv": "ef97860b8c31b6b137676609620bbc1b39c03ce0b51c46163249d7da3c75df7a",
        "two-family-setback-results.csv": "980ab61edcb245a2813c0acb438f82689f414d43716cd0910bc1561d638085ac",
        "principal_building_site_audit.csv": "aed2e770f67af14582b8227ac92fd3bdac3eb6df67483df58e4ed6f4b03d78e7",
    },
)

SPIRIT_ACCESSIBILITY = DataAsset(
    "detroit.spirit-plaza.accessibility",
    Path("data/datasets/detroit-spirit-plaza-accessibility"),
    DatasetModel(
        "detroit.spirit-plaza.accessibility", "1.0.0",
        custom_validator=validate_spirit_plaza_accessibility,
    ),
    ArchiveTier.DELIVERABLE,
)
PARKING_REQUIREMENTS = DataAsset(
    "detroit.bza.parking-requirements",
    Path("data/datasets/detroit-bza-parking-requirements"),
    DatasetModel(
        "detroit.bza.parking-requirements", "1.0.0",
        custom_validator=validate_parking_audit,
    ),
    ArchiveTier.DELIVERABLE,
)
RESIDENTIAL_SETBACK_ENVELOPE = DataAsset(
    "detroit.residential-setback-envelope",
    Path("data/datasets/detroit-residential-setback-envelope"),
    DatasetModel(
        "detroit.residential-setback-envelope", "1.0.0",
        required_columns={
            "source_row": "int64",
            "parcel_id": "string",
            "parcel_key": "string",
            "building_type": "string",
            "in_scope": "bool",
            "candidate_multi_parcel_site": "bool",
            "evaluated": "bool",
            "crosses_envelope": "bool",
            "evaluation_reason": "string",
            "frontage_confidence": "string",
        },
        primary_key=("parcel_id",),
        geometry_types=("Polygon", "MultiPolygon"),
        crs="EPSG:4326",
        accepted_artifact="classification.parquet",
    ),
    ArchiveTier.DELIVERABLE,
)
