"""Contract-v1 canonicalizers for the registered Detroit legacy sources."""

from __future__ import annotations

import math
import uuid
from collections import Counter
from collections.abc import Callable
from pathlib import Path

import geopandas as gpd
import pandas as pd
import pyarrow.parquet as pq

from krabby_real_estate.base_units.anchors import normalize_relationship_id
from krabby_real_estate.base_units.geometry import normalize_parcel_id
from krabby_real_estate.data.artifacts import artifact_path
from krabby_real_estate.data.catalog import catalog
from krabby_real_estate.data.geoparquet import write_geoparquet, write_rejects
from krabby_real_estate.data.model import DataAssetRef, ProvenanceGrade
from krabby_real_estate.data.storage import PendingArtifact, SnapshotBuilder

POI_NAMESPACE = uuid.UUID("f705649d-1d5c-54fc-904d-34f4e3e70d35")
OSM_CATEGORY_KEYS = ("shop", "amenity", "leisure", "tourism", "office", "craft")


def _text(value) -> str | None:
    if value is None:
        return None
    try:
        if pd.isna(value):
            return None
    except (TypeError, ValueError):
        pass
    result = str(value).strip()
    return result or None


def _values(series: pd.Series, transform) -> list:
    """Map without pandas converting Python None back into floating NaN."""
    return [transform(value) for value in series.tolist()]


def _source_id(frame: pd.DataFrame) -> pd.Series:
    for name in ("objectid", "object_id", "OBJECTID", "ObjectId"):
        if name in frame:
            return frame[name].map(normalize_relationship_id)
    return pd.Series((str(index) for index in frame.index), index=frame.index)


def _reject_records(frame: pd.DataFrame, mask: pd.Series, reason: str) -> list[dict]:
    source_ids = _source_id(frame)
    return [
        {
            "source_row_locator": value or f"row:{index}",
            "reason": reason,
            "detail": None,
        }
        for index, value in source_ids[mask].items()
    ]


def _finalize(
    repository: Path,
    output_asset_id: str,
    parent: DataAssetRef,
    columns: dict,
    geometries: dict[str, tuple[list, tuple[str, ...]]],
    rejects: list[dict],
    input_count: int,
) -> DataAssetRef:
    asset = catalog.assets[output_asset_id]
    builder = SnapshotBuilder(repository, asset)
    try:
        accepted_path = builder.path("accepted.parquet")
        accepted_schema_hash = write_geoparquet(
            columns,
            accepted_path,
            asset.contract,
            geometry_columns=geometries,
        )
        reject_path = builder.path("rejects.parquet")
        reject_schema_hash = write_rejects(rejects, reject_path)
    except Exception as error:
        builder.record_failure("canonicalization_failed", error)
        raise
    count = len(next(iter(columns.values()))) if columns else 0
    geometry_types = tuple(sorted({item for _, types in geometries.values() for item in types}))
    return builder.finalize(
        artifacts=[
            PendingArtifact(
                "accepted",
                accepted_path,
                asset.media_type,
                record_count=count,
                schema_hash=accepted_schema_hash,
                crs=asset.contract.crs,
                geometry_types=geometry_types,
            ),
            PendingArtifact(
                "rejects",
                reject_path,
                "application/vnd.apache.parquet",
                record_count=len(rejects),
                schema_hash=reject_schema_hash,
            ),
        ],
        provenance_grade=ProvenanceGrade.NATIVE,
        parents=[parent],
        counts={"input": input_count, "accepted": count, "rejected": len(rejects)},
        rejection_counts_by_reason=dict(Counter(record["reason"] for record in rejects)),
        parameters={"canonicalizer_contract_version": "1.0.0"},
        crs=asset.contract.crs,
        geometry_types=geometry_types,
    )


def canonicalize_parcels(repository: Path, parent: DataAssetRef) -> DataAssetRef:
    source = gpd.read_file(artifact_path(repository, parent, "raw"))
    source_ids = _source_id(source)
    parcel_ids = source["parcel_id"].map(_text)
    parcel_keys = source["parcel_id"].map(normalize_parcel_id)
    missing = (
        parcel_ids.isna()
        | parcel_keys.isna()
        | source.geometry.isna()
        | source.geometry.is_empty
        | source_ids.isna()
    )
    invalid_geometry = ~missing & (
        ~source.geometry.is_valid | ~source.geometry.geom_type.isin({"Polygon", "MultiPolygon"})
    )
    duplicate = parcel_keys.duplicated(keep=False) & ~(missing | invalid_geometry)
    rejects = _reject_records(source, missing, "missing_required_value")
    rejects += _reject_records(source, invalid_geometry, "invalid_geometry")
    rejects += _reject_records(source, duplicate, "duplicate_parcel_key")
    accepted = ~(missing | invalid_geometry | duplicate)
    frame = source.loc[accepted].to_crs("EPSG:4326")
    return _finalize(
        repository,
        "detroit.parcels",
        parent,
        {
            "parcel_id": parcel_ids[accepted].tolist(),
            "parcel_key": parcel_keys[accepted].tolist(),
            "source_object_id": source_ids[accepted].tolist(),
        },
        {"geometry": (frame.geometry.tolist(), ("Polygon", "MultiPolygon"))},
        rejects,
        len(source),
    )


def _canonicalize_relation_layer(
    repository: Path,
    parent: DataAssetRef,
    *,
    output_asset_id: str,
    identity: str,
    make_columns: Callable[[gpd.GeoDataFrame, pd.Series], dict],
    geometry_types: tuple[str, ...],
    geometry_required: bool = True,
) -> DataAssetRef:
    source = gpd.read_file(artifact_path(repository, parent, "raw"))
    ids = source[identity].map(normalize_relationship_id)
    source_ids = _source_id(source)
    missing = ids.isna() | source_ids.isna()
    if geometry_required:
        missing |= source.geometry.isna() | source.geometry.is_empty
    invalid_geometry = ~missing & (
        ~source.geometry.is_valid | ~source.geometry.geom_type.isin(set(geometry_types))
    )
    if not geometry_required:
        invalid_geometry &= source.geometry.notna() & ~source.geometry.is_empty
    duplicate = ids.duplicated(keep=False) & ~(missing | invalid_geometry)
    rejects = _reject_records(source, missing, "missing_required_value")
    rejects += _reject_records(source, invalid_geometry, "invalid_geometry")
    rejects += _reject_records(source, duplicate, f"duplicate_{identity}")
    accepted = ~(missing | invalid_geometry | duplicate)
    frame = source.loc[accepted].to_crs("EPSG:4326")
    columns = make_columns(frame, ids[accepted])
    columns["source_object_id"] = source_ids[accepted].tolist()
    return _finalize(
        repository,
        output_asset_id,
        parent,
        columns,
        {"geometry": (frame.geometry.tolist(), geometry_types)},
        rejects,
        len(source),
    )


def canonicalize_addresses(repository: Path, parent: DataAssetRef) -> DataAssetRef:
    def columns(frame, ids):
        return {
            "address_id": ids.tolist(),
            "parcel_id": _values(frame["parcel_id"], _text),
            "parcel_key": _values(frame["parcel_id"], normalize_parcel_id),
            "street_id": _values(frame["street_id"], normalize_relationship_id),
            "building_id": _values(frame["building_id"], normalize_relationship_id),
        }

    return _canonicalize_relation_layer(
        repository,
        parent,
        output_asset_id="detroit.base-units.addresses",
        identity="address_id",
        make_columns=columns,
        geometry_types=("Point",),
        geometry_required=False,
    )


def canonicalize_streets(repository: Path, parent: DataAssetRef) -> DataAssetRef:
    def columns(frame, ids):
        return {
            "street_id": ids.tolist(),
            "full_street_name": _values(frame["full_street_name"], _text),
        }

    return _canonicalize_relation_layer(
        repository,
        parent,
        output_asset_id="detroit.base-units.streets",
        identity="street_id",
        make_columns=columns,
        geometry_types=("LineString", "MultiLineString"),
    )


def canonicalize_buildings(repository: Path, parent: DataAssetRef) -> DataAssetRef:
    def columns(frame, ids):
        return {
            "building_id": ids.tolist(),
            "parcel_id": _values(frame["parcel_id"], _text),
            "parcel_key": _values(frame["parcel_id"], normalize_parcel_id),
            "status": _values(frame["status"], _text),
        }

    return _canonicalize_relation_layer(
        repository,
        parent,
        output_asset_id="detroit.base-units.buildings",
        identity="building_id",
        make_columns=columns,
        geometry_types=("Polygon", "MultiPolygon"),
    )


def _plain_tag(value) -> str | None:
    if value is None:
        return None
    try:
        if pd.isna(value):
            return None
    except (TypeError, ValueError):
        pass
    if isinstance(value, float) and not math.isfinite(value):
        return None
    if isinstance(value, (list, tuple, set)):
        return ";".join(sorted(map(str, value)))
    return str(value)


def _first_text(row, names) -> str | None:
    for name in names:
        value = _text(row.get(name))
        if value is not None:
            return value
    return None


def canonicalize_osm_pois(repository: Path, parent: DataAssetRef) -> DataAssetRef:
    source = gpd.read_file(artifact_path(repository, parent, "raw")).to_crs("EPSG:4326")
    element_types = source["element"].map(_text)
    source_ids = source["id"].map(normalize_relationship_id)
    missing = (
        element_types.isna() | source_ids.isna() | source.geometry.isna() | source.geometry.is_empty
    )
    invalid_geometry = ~missing & ~source.geometry.is_valid
    identities = element_types.fillna("") + ":" + source_ids.fillna("")
    duplicate = identities.duplicated(keep=False) & ~(missing | invalid_geometry)
    rejects = _reject_records(source, missing, "missing_required_value")
    rejects += _reject_records(source, invalid_geometry, "invalid_geometry")
    rejects += _reject_records(source, duplicate, "duplicate_osm_identity")
    accepted = ~(missing | invalid_geometry | duplicate)
    frame = source.loc[accepted]
    records = []
    source_geometries = []
    points = []
    for index, row in frame.iterrows():
        geometry = row.geometry
        point = geometry if geometry.geom_type == "Point" else geometry.representative_point()
        element_type = element_types[index]
        source_id = source_ids[index]
        identity = f"osm:{element_type}:{source_id}"
        categories = [
            {"key": key, "value": value}
            for key in OSM_CATEGORY_KEYS
            if (value := _plain_tag(row.get(key))) is not None
        ]
        source_tags = [
            {"key": str(key), "value": value}
            for key in sorted(frame.columns)
            if key != "geometry" and (value := _plain_tag(row.get(key))) is not None
        ]
        records.append(
            {
                "poi_uuid": str(uuid.uuid5(POI_NAMESPACE, f"osm-poi-v1:{identity}")),
                "poi_id": identity,
                "source": "openstreetmap",
                "source_element_type": element_type,
                "source_id": source_id,
                "name": _first_text(row, ("name", "brand", "operator")),
                "categories": categories,
                "source_tags": source_tags,
                "source_geometry_type": geometry.geom_type,
                "routing_point_method": "source_point"
                if geometry.geom_type == "Point"
                else "representative_point",
                "routing_point_status": "ready",
                "longitude": float(point.x),
                "latitude": float(point.y),
            }
        )
        source_geometries.append(geometry)
        points.append(point)
    columns = {name: [record[name] for record in records] for name in records[0]} if records else {}
    return _finalize(
        repository,
        "osm.detroit.pois",
        parent,
        columns,
        {
            "source_geometry": (
                source_geometries,
                ("Point", "LineString", "Polygon", "MultiPolygon"),
            ),
            "geometry": (points, ("Point",)),
        },
        rejects,
        len(source),
    )


CANONICALIZERS = {
    "canonicalize.parcels": canonicalize_parcels,
    "canonicalize.addresses": canonicalize_addresses,
    "canonicalize.streets": canonicalize_streets,
    "canonicalize.buildings": canonicalize_buildings,
    "canonicalize.osm-pois": canonicalize_osm_pois,
}


def parquet_count(path: Path) -> int:
    return pq.ParquetFile(path).metadata.num_rows
