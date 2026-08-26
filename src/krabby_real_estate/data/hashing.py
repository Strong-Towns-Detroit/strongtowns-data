"""Canonical hashing helpers used by contracts and manifests."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pyarrow as pa


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_json(value) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(encoded.encode()).hexdigest()


def schema_hash(schema: pa.Schema | None) -> str | None:
    """Hash semantic Arrow structure, stable across Parquet list-child renaming."""
    if schema is None:
        return None
    return sha256_json([_field_document(field) for field in schema])


def _field_document(field: pa.Field) -> dict:
    return {
        "name": field.name,
        "nullable": field.nullable,
        "type": _type_document(field.type),
    }


def _type_document(data_type: pa.DataType):
    if pa.types.is_list(data_type):
        return {
            "list": _type_document(data_type.value_type),
            "value_nullable": data_type.value_field.nullable,
        }
    if pa.types.is_large_list(data_type):
        return {
            "large_list": _type_document(data_type.value_type),
            "value_nullable": data_type.value_field.nullable,
        }
    if pa.types.is_struct(data_type):
        return {"struct": [_field_document(field) for field in data_type]}
    if pa.types.is_map(data_type):
        return {
            "map": {
                "key": _type_document(data_type.key_type),
                "item": _type_document(data_type.item_type),
                "keys_sorted": data_type.keys_sorted,
            }
        }
    if pa.types.is_timestamp(data_type):
        return {"timestamp": {"unit": data_type.unit, "tz": data_type.tz}}
    if pa.types.is_decimal(data_type):
        return {
            "decimal": {
                "bit_width": data_type.bit_width,
                "precision": data_type.precision,
                "scale": data_type.scale,
            }
        }
    return str(data_type)
