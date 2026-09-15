"""Built-in Strong Towns Detroit data pipelines."""

from strongtowns_data.pipelines import (
    AcquisitionPolicy,
    DataAsset,
    DataPipeline,
    data_pipeline,
)
from strongtowns_data.pipelines.geospatial import canonical_geojson_builder
from strongtowns_data.pipelines.assessments import (
    ASSESSMENT_COLUMNS,
    canonical_assessment_builder,
    canonical_lvt_2023_builder,
)
from strongtowns_data.pipelines.http import download_file
from strongtowns_data.pipelines.land_values import build_parcel_land_values
from strongtowns_data.pipelines.arcgis import collect_layer
from strongtowns_data.pipelines import BuildMetadata
from strongtowns_data.pipelines.routing import build_routing_anchor_tables
import geopandas as gpd
import os
from datetime import datetime
from zoneinfo import ZoneInfo
from strongtowns_data.pipelines.traveltime import (
    build_request_ledger,
    execute_request_ledger,
)
from strongtowns_data.pipelines.osm import collect_osm_pois, normalize_osm_features
from strongtowns_data.pipelines.catalog import build_query_catalog
from strongtowns_data.pipelines.presentation import (
    build_residential_setback_classification,
    preserve_parking_audit,
    preserve_spirit_plaza,
)
from strongtowns_data.models.datasets import (
    ADDRESSES,
    ADDRESSES_RAW,
    ANCHORS,
    ASSESSMENT_REPORTS_RAW,
    ASSESSMENTS,
    ASSESSMENTS_RAW,
    BUILDINGS,
    BUILDINGS_RAW,
    BZA_GEMINI_RAW,
    BZA_MINUTES_RAW,
    DETROIT_BASEMAP_RAW,
    DISPOSITIONS,
    EVIDENCE,
    FRONTAGES,
    LIHTC_QCT_RAW,
    LVT_2023,
    LVT_2023_RAW,
    MUNICODE_RAW,
    OSM_POIS,
    OSM_POIS_RAW,
    PARCELS,
    PARCELS_RAW,
    PARCEL_LAND_VALUES,
    PARCEL_ATTRIBUTES_RAW,
    PARKING_REQUIREMENTS,
    PARKING_REQUIREMENTS_RAW,
    QUERY_CATALOG,
    SPIRIT_TRAVELTIME_RAW,
    SPIRIT_ACCESSIBILITY,
    SPIRIT_PRESENTATION_RAW,
    RESIDENTIAL_SETBACK_ENVELOPE,
    SETBACK_RESULTS_RAW,
    STREETS,
    STREETS_RAW,
    TRAVELTIME_REQUESTS,
    TRAVELTIME_RESULTS,
)


PARCEL_LAYER = (
    "https://services2.arcgis.com/qvkbeam7Wirps6zC/arcgis/rest/services/"
    "parcel_file_current/FeatureServer/0"
)
ASSESSMENT_LAYER = (
    "https://services2.arcgis.com/qvkbeam7Wirps6zC/arcgis/rest/services/"
    "tentative_assessment_roll_2026/FeatureServer/0"
)
LVT_2023_URL = (
    "https://detroit-land-value-tax-maps.us-east-1.linodeobjects.com/"
    "detroit-lvt.csv"
)
BASE_UNITS_SERVICE = (
    "https://services2.arcgis.com/qvkbeam7Wirps6zC/arcgis/rest/services/"
    "BaseUnitFeatures/FeatureServer"
)


def fetch_arcgis_outputs(
    endpoints: dict[str, str], *, out_fields: dict[str, str] | None = None
):
    def fetch(context):
        metadata = {}
        for asset_id, endpoint in endpoints.items():
            collection = collect_layer(
                endpoint,
                context.staging[asset_id] / "raw.geojson",
                cache_root=context.root / "data" / ".cache" / "arcgis",
                out_fields=(out_fields or {}).get(asset_id, "*"),
            )
            metadata[asset_id] = BuildMetadata(
                counts={"records": collection.feature_count},
                source={
                    "provider": "ArcGIS FeatureServer",
                    "url": endpoint,
                    "fingerprint": collection.cache_fingerprint,
                    "before": collection.before,
                    "after": collection.after,
                    "started_at": collection.started_at,
                    "completed_at": collection.completed_at,
                },
            )
        return metadata

    return fetch


@data_pipeline("detroit-parcels-source")
def detroit_parcels_source() -> DataPipeline:
    return DataPipeline(
        "detroit-parcels-source", (), (PARCELS_RAW,),
        fetch=fetch_arcgis_outputs({PARCELS_RAW.id: PARCEL_LAYER}),
        acquisition_policy=AcquisitionPolicy.PUBLIC_NETWORK,
        description="Immutable snapshots of Detroit's current parcel service.",
    )


@data_pipeline("detroit-base-units-source")
def detroit_base_units_source() -> DataPipeline:
    return DataPipeline(
        "detroit-base-units-source", (),
        (ADDRESSES_RAW, STREETS_RAW, BUILDINGS_RAW),
        fetch=fetch_arcgis_outputs({
            ADDRESSES_RAW.id: f"{BASE_UNITS_SERVICE}/0",
            STREETS_RAW.id: f"{BASE_UNITS_SERVICE}/1",
            BUILDINGS_RAW.id: f"{BASE_UNITS_SERVICE}/2",
        }),
        acquisition_policy=AcquisitionPolicy.PUBLIC_NETWORK,
        description="Immutable snapshots of the Detroit Base Units layers.",
    )


@data_pipeline("detroit-assessments-source")
def detroit_assessments_source() -> DataPipeline:
    fields = ",".join(ASSESSMENT_COLUMNS)
    return DataPipeline(
        "detroit-assessments-source",
        (),
        (ASSESSMENTS_RAW,),
        fetch=fetch_arcgis_outputs(
            {ASSESSMENTS_RAW.id: ASSESSMENT_LAYER},
            out_fields={ASSESSMENTS_RAW.id: fields},
        ),
        acquisition_policy=AcquisitionPolicy.PUBLIC_NETWORK,
        description="Immutable snapshots of Detroit's tentative assessment roll.",
    )


@data_pipeline("detroit-lvt-estimator-2023-source")
def detroit_lvt_estimator_2023_source() -> DataPipeline:
    def fetch(context):
        result = download_file(
            LVT_2023_URL, context.staging[LVT_2023_RAW.id] / "raw.csv"
        )
        return {LVT_2023_RAW.id: BuildMetadata(
            counts={"bytes": result.size},
            source={
                "provider": "City of Detroit, republished by DETROITography",
                "url": result.url,
                "sha256": result.sha256,
                "etag": result.etag,
                "last_modified": result.last_modified,
                "started_at": result.started_at,
                "completed_at": result.completed_at,
            },
        )}

    return DataPipeline(
        "detroit-lvt-estimator-2023-source", (), (LVT_2023_RAW,),
        fetch=fetch,
        acquisition_policy=AcquisitionPolicy.PUBLIC_NETWORK,
        description="City-released parcel estimates for Detroit's 2023 LVT plan.",
    )


def canonical_pipeline(
    name: str,
    raw: DataAsset,
    output: DataAsset,
    primary_key: str,
    geometry_types: tuple[str, ...],
) -> DataPipeline:
    return DataPipeline(
        name,
        (raw.id,),
        (output,),
        build=canonical_geojson_builder(
            input_asset=raw.id,
            input_artifact="raw.geojson",
            output_asset=output.id,
            primary_key=primary_key,
            geometry_types=geometry_types,
        ),
        description=f"Canonical GeoParquet for {output.id}.",
    )


@data_pipeline("canonical-detroit-parcels")
def canonical_detroit_parcels() -> DataPipeline:
    return canonical_pipeline(
        "canonical-detroit-parcels", PARCELS_RAW, PARCELS,
        "parcel_id", ("Polygon", "MultiPolygon"),
    )


@data_pipeline("canonical-detroit-assessments")
def canonical_detroit_assessments() -> DataPipeline:
    return DataPipeline(
        "canonical-detroit-assessments",
        (ASSESSMENTS_RAW.id,),
        (ASSESSMENTS,),
        build=canonical_assessment_builder(
            input_asset=ASSESSMENTS_RAW.id,
            output_asset=ASSESSMENTS.id,
            roll_year=2026,
        ),
        description="Typed, record-level Detroit assessment roll.",
    )


@data_pipeline("canonical-detroit-lvt-estimator-2023")
def canonical_detroit_lvt_estimator_2023() -> DataPipeline:
    return DataPipeline(
        "canonical-detroit-lvt-estimator-2023",
        (LVT_2023_RAW.id,),
        (LVT_2023,),
        build=canonical_lvt_2023_builder(
            input_asset=LVT_2023_RAW.id, output_asset=LVT_2023.id
        ),
        description="Typed City-released 2023 residential LVT estimates.",
    )


@data_pipeline("detroit-parcel-land-values")
def detroit_parcel_land_values() -> DataPipeline:
    def build(context):
        return build_parcel_land_values(
            context,
            parcels_asset=PARCELS.id,
            assessments_asset=ASSESSMENTS.id,
            history_asset=LVT_2023.id,
            output_asset=PARCEL_LAND_VALUES.id,
        )

    return DataPipeline(
        "detroit-parcel-land-values",
        (PARCELS.id, ASSESSMENTS.id, LVT_2023.id),
        (PARCEL_LAND_VALUES,),
        build=build,
        description=(
            "Official and spatially smoothed parcel land values with taxable allocations."
        ),
    )


@data_pipeline("canonical-detroit-base-units-addresses")
def canonical_detroit_addresses() -> DataPipeline:
    return canonical_pipeline(
        "canonical-detroit-base-units-addresses", ADDRESSES_RAW, ADDRESSES,
        "address_id", ("Point",),
    )


@data_pipeline("canonical-detroit-base-units-streets")
def canonical_detroit_streets() -> DataPipeline:
    return canonical_pipeline(
        "canonical-detroit-base-units-streets", STREETS_RAW, STREETS,
        "street_id", ("LineString", "MultiLineString"),
    )


@data_pipeline("canonical-detroit-base-units-buildings")
def canonical_detroit_buildings() -> DataPipeline:
    return canonical_pipeline(
        "canonical-detroit-base-units-buildings", BUILDINGS_RAW, BUILDINGS,
        "building_id", ("Polygon", "MultiPolygon"),
    )


def build_detroit_query_catalog(context):
    metadata = build_query_catalog(
        context,
        output_asset=QUERY_CATALOG.id,
        tables={
            PARCELS.id: "parcels",
            ASSESSMENTS.id: "assessments",
            PARCEL_LAND_VALUES.id: "parcel_land_values",
            ADDRESSES.id: "base_units_addresses",
            STREETS.id: "base_units_streets",
            BUILDINGS.id: "base_units_buildings",
        },
    )
    return {QUERY_CATALOG.id: metadata}


@data_pipeline("detroit-query-catalog")
def detroit_query_catalog() -> DataPipeline:
    return DataPipeline(
        "detroit-query-catalog",
        (
            PARCELS.id, ASSESSMENTS.id, PARCEL_LAND_VALUES.id,
            ADDRESSES.id, STREETS.id, BUILDINGS.id,
        ),
        (QUERY_CATALOG,),
        build=build_detroit_query_catalog,
        description=(
            "Portable, read-only DuckDB mirror of promoted Detroit spatial tables."
        ),
    )


def build_routing_datasets(context):
    tables = build_routing_anchor_tables(
        gpd.read_parquet(context.inputs[PARCELS.id] / "accepted.parquet"),
        gpd.read_parquet(context.inputs[ADDRESSES.id] / "accepted.parquet"),
        gpd.read_parquet(context.inputs[STREETS.id] / "accepted.parquet"),
        gpd.read_parquet(context.inputs[BUILDINGS.id] / "accepted.parquet"),
    )
    tables["anchors"].to_parquet(
        context.staging[ANCHORS.id] / "accepted.parquet", index=False
    )
    tables["blocked"].to_parquet(
        context.staging[ANCHORS.id] / "blocked.parquet", index=False
    )
    tables["frontages"].to_parquet(
        context.staging[FRONTAGES.id] / "accepted.parquet", index=False
    )
    tables["evidence"].to_parquet(
        context.staging[EVIDENCE.id] / "accepted.parquet", index=False
    )
    tables["dispositions"].to_parquet(
        context.staging[DISPOSITIONS.id] / "accepted.parquet", index=False
    )
    anchor_counts = {
        "parcels_input": len(tables["anchors"].parcel_key.unique()) + len(tables["blocked"]),
        "anchors": len(tables["anchors"]),
        "multi_anchor_parcels": int(
            (tables["anchors"].groupby("parcel_key").size() > 1).sum()
        ),
        "fallbacks": int(tables["anchors"].method.eq("nearest_street_fallback").sum()),
        "default_ready": int(tables["anchors"].review_status.eq("not_required").sum()),
        "review_required": int(tables["anchors"].review_status.eq("required").sum()),
        "blocked_parcels": len(tables["blocked"]),
    }
    return {
        ANCHORS.id: BuildMetadata(counts=anchor_counts, parameters={"identity": "routing-anchor-v1"}),
        FRONTAGES.id: BuildMetadata(counts={"records": len(tables["frontages"])}),
        EVIDENCE.id: BuildMetadata(counts={"records": len(tables["evidence"])}),
        DISPOSITIONS.id: BuildMetadata(counts={"records": len(tables["dispositions"])}),
    }


@data_pipeline("detroit-routing-anchors")
def detroit_routing_anchors() -> DataPipeline:
    return DataPipeline(
        "detroit-routing-anchors",
        (PARCELS.id, ADDRESSES.id, STREETS.id, BUILDINGS.id),
        (ANCHORS, FRONTAGES, EVIDENCE, DISPOSITIONS),
        build=build_routing_datasets,
        description="Stable parcel routing anchors, evidence, frontages, and review status.",
    )


def build_traveltime_smoke_requests(context):
    anchors = gpd.read_parquet(context.inputs[ANCHORS.id] / "accepted.parquet")
    eligible = anchors[anchors.review_status.isin({"not_required", "approved"})]
    if eligible.empty:
        raise ValueError("no default-ready anchor is available for the smoke request")
    selected = eligible.sort_values("anchor_id", kind="stable").head(1)
    requests, blocked = build_request_ledger(
        selected,
        directions=("arrival", "departure"),
        mode="walking",
        horizon_seconds=3600,
        reference_time=datetime(2026, 8, 26, 12, tzinfo=ZoneInfo("America/Detroit")),
    )
    requests.to_parquet(
        context.staging[TRAVELTIME_REQUESTS.id] / "accepted.parquet", index=False
    )
    blocked.to_parquet(
        context.staging[TRAVELTIME_REQUESTS.id] / "blocked.parquet", index=False
    )
    return {
        TRAVELTIME_REQUESTS.id: BuildMetadata(
            counts={"requests": len(requests), "blocked": len(blocked)},
            parameters={
                "scope": "opt-in-smoke",
                "maximum_anchors": 1,
                "directions": ["arrival", "departure"],
                "mode": "walking",
                "horizon_seconds": 3600,
                "required_override": False,
            },
        )
    }


@data_pipeline("traveltime-smoke-requests")
def traveltime_smoke_requests() -> DataPipeline:
    return DataPipeline(
        "traveltime-smoke-requests", (ANCHORS.id,), (TRAVELTIME_REQUESTS,),
        build=build_traveltime_smoke_requests,
        description="Two opt-in TravelTime requests for one default-ready anchor.",
    )


def fetch_traveltime_smoke(context):
    app_id = os.environ.get("TRAVELTIME_APP_ID")
    api_key = os.environ.get("TRAVELTIME_API_KEY")
    if not app_id or not api_key:
        raise ValueError("TRAVELTIME_APP_ID and TRAVELTIME_API_KEY are required")
    requests = gpd.read_parquet(
        context.inputs[TRAVELTIME_REQUESTS.id] / "accepted.parquet"
    )
    run = execute_request_ledger(
        requests,
        context.staging[TRAVELTIME_RESULTS.id] / "raw",
        app_id=app_id,
        api_key=api_key,
    )
    run.results.to_parquet(
        context.staging[TRAVELTIME_RESULTS.id] / "accepted.parquet", index=False
    )
    run.errors.to_parquet(
        context.staging[TRAVELTIME_RESULTS.id] / "errors.parquet", index=False
    )
    return {
        TRAVELTIME_RESULTS.id: BuildMetadata(
            counts={
                "requests": len(requests),
                "responses": len(run.results),
                "errors": len(run.errors),
                "retries": run.retries,
            },
            source={"provider": "TravelTime", "endpoint": "v4/time-map"},
            transaction_quality="provider_reconciled",
        )
    }


@data_pipeline("traveltime-smoke-results")
def traveltime_smoke_results() -> DataPipeline:
    return DataPipeline(
        "traveltime-smoke-results", (TRAVELTIME_REQUESTS.id,), (TRAVELTIME_RESULTS,),
        fetch=fetch_traveltime_smoke,
        acquisition_policy=AcquisitionPolicy.PAID,
        description="Opt-in, exactly reconciled TravelTime smoke-test results.",
    )


def fetch_osm_pois(context):
    source = collect_osm_pois(
        context.staging[OSM_POIS_RAW.id] / "raw.parquet",
        cache_root=context.root / "data" / ".cache" / "osmnx",
    )
    counts = {key: source.pop(key) for key in ("input", "accepted", "rejected")}
    return {
        OSM_POIS_RAW.id: BuildMetadata(
            counts=counts,
            source=source,
            transaction_quality="best_effort",
        )
    }


@data_pipeline("detroit-osm-pois-source")
def detroit_osm_pois_source() -> DataPipeline:
    return DataPipeline(
        "detroit-osm-pois-source", (), (OSM_POIS_RAW,),
        fetch=fetch_osm_pois,
        acquisition_policy=AcquisitionPolicy.PUBLIC_NETWORK,
        description="Source-faithful Detroit OSM POI geometries and selected tags.",
    )


def build_osm_pois(context):
    source = gpd.read_parquet(context.inputs[OSM_POIS_RAW.id] / "raw.parquet")
    candidates, rejected = normalize_osm_features(source, return_rejected=True)
    candidates.to_parquet(
        context.staging[OSM_POIS.id] / "accepted.parquet", index=False
    )
    rejected.to_parquet(
        context.staging[OSM_POIS.id] / "rejects.parquet", index=False
    )
    return {
        OSM_POIS.id: BuildMetadata(
            counts={"input": len(source), "accepted": len(candidates), "rejected": len(source) - len(candidates)},
            parameters={"routing_interpretation": "osm-poi-v1"},
        )
    }


@data_pipeline("canonical-detroit-osm-pois")
def canonical_detroit_osm_pois() -> DataPipeline:
    return DataPipeline(
        "canonical-detroit-osm-pois", (OSM_POIS_RAW.id,), (OSM_POIS,),
        build=build_osm_pois,
        description="Routing candidates derived from preserved OSM source geometry.",
    )


def source_pipeline(
    name: str,
    outputs: tuple[DataAsset, ...],
    policy: AcquisitionPolicy,
    description: str,
) -> DataPipeline:
    return DataPipeline(
        name, (), outputs, acquisition_policy=policy, description=description
    )


@data_pipeline("detroit-municode-source")
def detroit_municode_source() -> DataPipeline:
    return source_pipeline(
        "detroit-municode-source", (MUNICODE_RAW,), AcquisitionPolicy.PUBLIC_NETWORK,
        "Immutable Detroit Chapter 50 Municode snapshot.",
    )


@data_pipeline("detroit-bza-minutes-source")
def detroit_bza_minutes_source() -> DataPipeline:
    return source_pipeline(
        "detroit-bza-minutes-source", (BZA_MINUTES_RAW,), AcquisitionPolicy.PUBLIC_NETWORK,
        "Scraped Detroit BZA minutes PDFs.",
    )


@data_pipeline("detroit-bza-gemini-source")
def detroit_bza_gemini_source() -> DataPipeline:
    return source_pipeline(
        "detroit-bza-gemini-source", (BZA_GEMINI_RAW,), AcquisitionPolicy.PAID,
        "Raw and consolidated Gemini extraction evidence.",
    )


@data_pipeline("michigan-assessment-history-source")
def michigan_assessment_history_source() -> DataPipeline:
    return source_pipeline(
        "michigan-assessment-history-source", (ASSESSMENT_REPORTS_RAW,),
        AcquisitionPolicy.PUBLIC_NETWORK, "Michigan Treasury levy-report snapshots.",
    )


@data_pipeline("detroit-parcel-attributes-source")
def detroit_parcel_attributes_source() -> DataPipeline:
    return source_pipeline(
        "detroit-parcel-attributes-source", (PARCEL_ATTRIBUTES_RAW,),
        AcquisitionPolicy.PUBLIC_NETWORK, "Detroit parcel attribute snapshot.",
    )


@data_pipeline("hud-lihtc-qct-source")
def hud_lihtc_qct_source() -> DataPipeline:
    return source_pipeline(
        "hud-lihtc-qct-source", (LIHTC_QCT_RAW,), AcquisitionPolicy.PUBLIC_NETWORK,
        "HUD 2026 QCT designation snapshot for Wayne County.",
    )


@data_pipeline("detroit-osm-basemap-source")
def detroit_osm_basemap_source() -> DataPipeline:
    return source_pipeline(
        "detroit-osm-basemap-source", (DETROIT_BASEMAP_RAW,),
        AcquisitionPolicy.PUBLIC_NETWORK, "Detroit boundary and water snapshot.",
    )


@data_pipeline("spirit-plaza-traveltime-legacy-source")
def spirit_plaza_traveltime_legacy_source() -> DataPipeline:
    return source_pipeline(
        "spirit-plaza-traveltime-legacy-source", (SPIRIT_TRAVELTIME_RAW,),
        AcquisitionPolicy.PAID, "Legacy immutable TravelTime response evidence.",
    )


@data_pipeline("spirit-plaza-presentation-legacy-source")
def spirit_plaza_presentation_legacy_source() -> DataPipeline:
    return source_pipeline(
        "spirit-plaza-presentation-legacy-source", (SPIRIT_PRESENTATION_RAW,),
        AcquisitionPolicy.PAID,
        "Exact legacy presentation evidence derived from paid TravelTime and OSM sources.",
    )


@data_pipeline("detroit-bza-parking-requirements-legacy-source")
def detroit_bza_parking_requirements_legacy_source() -> DataPipeline:
    return source_pipeline(
        "detroit-bza-parking-requirements-legacy-source", (PARKING_REQUIREMENTS_RAW,),
        AcquisitionPolicy.PAID,
        "Reviewed parking requirement transcription preserved from the BZA corpus.",
    )


@data_pipeline("detroit-residential-setback-results-legacy-source")
def detroit_residential_setback_results_legacy_source() -> DataPipeline:
    return source_pipeline(
        "detroit-residential-setback-results-legacy-source", (SETBACK_RESULTS_RAW,),
        AcquisitionPolicy.PUBLIC_NETWORK,
        "Computed residential setback evidence preserved from the pre-split repository.",
    )


@data_pipeline("detroit-spirit-plaza-accessibility")
def detroit_spirit_plaza_accessibility() -> DataPipeline:
    def build(context):
        return preserve_spirit_plaza(
            context,
            input_asset=SPIRIT_PRESENTATION_RAW.id,
            output_asset=SPIRIT_ACCESSIBILITY.id,
        )

    return DataPipeline(
        "detroit-spirit-plaza-accessibility",
        (SPIRIT_PRESENTATION_RAW.id,),
        (SPIRIT_ACCESSIBILITY,),
        build=build,
        description="Validated Spirit Plaza travel-time and road-context presentation data.",
    )


@data_pipeline("detroit-bza-parking-requirements")
def detroit_bza_parking_requirements() -> DataPipeline:
    def build(context):
        return preserve_parking_audit(
            context,
            input_asset=PARKING_REQUIREMENTS_RAW.id,
            output_asset=PARKING_REQUIREMENTS.id,
        )

    return DataPipeline(
        "detroit-bza-parking-requirements",
        (PARKING_REQUIREMENTS_RAW.id,),
        (PARKING_REQUIREMENTS,),
        build=build,
        description="Validated, reviewed Detroit BZA parking requirement audit.",
    )


@data_pipeline("detroit-residential-setback-envelope")
def detroit_residential_setback_envelope() -> DataPipeline:
    def build(context):
        return build_residential_setback_classification(
            context,
            parcels_asset=PARCELS.id,
            results_asset=SETBACK_RESULTS_RAW.id,
            output_asset=RESIDENTIAL_SETBACK_ENVELOPE.id,
        )

    return DataPipeline(
        "detroit-residential-setback-envelope",
        (PARCELS.id, SETBACK_RESULTS_RAW.id),
        (RESIDENTIAL_SETBACK_ENVELOPE,),
        build=build,
        description="Parcel geometry joined to preserved residential setback results.",
    )


@data_pipeline("detroit-bza-atlas")
def detroit_bza_atlas() -> DataPipeline:
    """Internal offline assembly; member fetching only downloads releases."""
    from pathlib import Path
    from strongtowns_data.models import DatasetModel
    from strongtowns_data.bza._pipeline.build import validate
    asset = DataAsset("detroit.bza.atlas", Path("data/datasets/detroit-bza-atlas"),
                      DatasetModel(name="detroit.bza.atlas", version="1.0.0", custom_validator=validate))

    def build(context):
        from strongtowns_data.bza._pipeline.build import build as build_atlas
        audit = build_atlas(
            context.inputs[BZA_GEMINI_RAW.id] / "raw",
            context.staging[asset.id], reviews=context.root / "resources/bza",
        )
        return {asset.id: BuildMetadata(counts=audit["counts"], source=audit)}

    return DataPipeline("detroit-bza-atlas", (BZA_GEMINI_RAW.id,),
                        (asset,), build=build, description="Prepared BZA histories and audited atlas tables.")
