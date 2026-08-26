"""Manifest schema loading, validation, and immutable reference resolution."""

from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

from krabby_real_estate.data.hashing import sha256_file
from krabby_real_estate.data.model import DataAssetRef

SCHEMA_DIR = Path(__file__).with_name("schemas")


def load_schema(name: str) -> dict:
    return json.loads((SCHEMA_DIR / name).read_text())


def validate_json_document(document: dict, schema_name: str) -> list[str]:
    validator = Draft202012Validator(load_schema(schema_name), format_checker=FormatChecker())
    return [error.message for error in sorted(validator.iter_errors(document), key=str)]


def read_manifest(path: Path) -> dict:
    path = Path(path)
    document = json.loads(path.read_text())
    errors = validate_json_document(document, "snapshot-manifest-v1.json")
    if errors:
        raise ValueError(f"invalid snapshot manifest {path}: {'; '.join(errors)}")
    return document


def manifest_ref(path: Path) -> DataAssetRef:
    path = Path(path).resolve()
    manifest = read_manifest(path)
    return DataAssetRef(
        asset_id=manifest["asset_id"],
        snapshot_id=manifest["snapshot_id"],
        manifest_path=path,
        manifest_sha256=sha256_file(path),
    )


def resolve_promoted(pointer_path: Path) -> DataAssetRef:
    pointer_path = Path(pointer_path).resolve()
    pointer = json.loads(pointer_path.read_text())
    errors = validate_json_document(pointer, "promotion-pointer-v1.json")
    if errors:
        raise ValueError(f"invalid promotion pointer {pointer_path}: {'; '.join(errors)}")
    manifest_path = (pointer_path.parent / pointer["manifest_path"]).resolve()
    if not manifest_path.is_relative_to(pointer_path.parent):
        raise ValueError("promotion pointer manifest path escapes asset root")
    reference = manifest_ref(manifest_path)
    if reference.manifest_sha256 != pointer["manifest_sha256"]:
        raise ValueError("promotion pointer manifest hash does not match")
    if reference.asset_id != pointer["asset_id"]:
        raise ValueError("promotion pointer asset id does not match manifest")
    if reference.snapshot_id != pointer["snapshot_id"]:
        raise ValueError("promotion pointer snapshot id does not match manifest")
    return reference
