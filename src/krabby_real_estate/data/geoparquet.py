"""Small, deterministic Arrow and GeoParquet writers used by Contract-v1."""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq
from pyproj import CRS
from shapely import to_wkb

from krabby_real_estate.data.hashing import schema_hash
from krabby_real_estate.data.model import DatasetContract
from krabby_real_estate.data.table_validation import validate_table


def table_from_columns(columns: Mapping[str, Sequence], schema: pa.Schema) -> pa.Table:
    missing = sorted(set(schema.names) - set(columns))
    if missing:
        raise ValueError(f"missing output columns: {missing}")
    arrays = []
    for field in schema:
        try:
            arrays.append(pa.array(columns[field.name], type=field.type))
        except (pa.ArrowInvalid, pa.ArrowTypeError) as error:
            raise ValueError(f"cannot encode output column {field.name}: {error}") from error
    return pa.Table.from_arrays(arrays, schema=schema)


def write_table(table: pa.Table, path: Path, contract: DatasetContract) -> str:
    result = validate_table(table, contract)
    if not result.valid:
        messages = "; ".join(f"{issue.code}: {issue.message}" for issue in result.issues)
        raise ValueError(f"table violates {contract.contract_id}: {messages}")
    pq.write_table(table, path, compression="zstd")
    return schema_hash(pq.ParquetFile(path).schema_arrow)


def write_geoparquet(
    columns: Mapping[str, Sequence],
    path: Path,
    contract: DatasetContract,
    *,
    geometry_columns: Mapping[str, tuple[Sequence, tuple[str, ...]]],
) -> str:
    """Write WKB GeoParquet with one primary and optional evidence geometry columns."""
    if contract.arrow_schema is None or contract.geometry_column is None or contract.crs is None:
        raise ValueError("GeoParquet output requires a geometry contract")
    encoded = dict(columns)
    geo_columns = {}
    for name, (values, geometry_types) in geometry_columns.items():
        allowed_types = set(geometry_types)
        for index, geometry in enumerate(values):
            if geometry is None or not hasattr(geometry, "is_empty") or geometry.is_empty:
                continue
            if not geometry.is_valid:
                raise ValueError(f"invalid geometry in {name} at output row {index}")
            if geometry.geom_type not in allowed_types:
                raise ValueError(f"unexpected {geometry.geom_type} in {name} at output row {index}")
        encoded[name] = [
            None
            if geometry is None or not hasattr(geometry, "is_empty") or geometry.is_empty
            else to_wkb(geometry)
            for geometry in values
        ]
        geo_columns[name] = {
            "encoding": "WKB",
            "geometry_types": list(geometry_types),
            "crs": CRS.from_user_input(contract.crs).to_json_dict(),
        }
    table = table_from_columns(encoded, contract.arrow_schema)
    metadata = dict(table.schema.metadata or {})
    metadata[b"geo"] = json.dumps(
        {
            "version": "1.1.0",
            "primary_column": contract.geometry_column,
            "columns": geo_columns,
        },
        sort_keys=True,
        separators=(",", ":"),
    ).encode()
    return write_table(table.replace_schema_metadata(metadata), path, contract)


REJECT_SCHEMA = pa.schema(
    [
        pa.field("source_row_locator", pa.string(), nullable=False),
        pa.field("reason", pa.string(), nullable=False),
        pa.field("detail", pa.string()),
    ]
)


def write_rejects(records: list[dict], path: Path) -> str:
    columns = {
        field.name: [record.get(field.name) for record in records] for field in REJECT_SCHEMA
    }
    table = table_from_columns(columns, REJECT_SCHEMA)
    pq.write_table(table, path, compression="zstd")
    return schema_hash(pq.ParquetFile(path).schema_arrow)
