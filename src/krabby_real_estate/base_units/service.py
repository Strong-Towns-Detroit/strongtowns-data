"""Resumable, auditable retrieval of Detroit Base Units ArcGIS layers."""

from __future__ import annotations

import hashlib
import json
import time
from collections.abc import Iterable
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path

import requests

BASE_UNITS_SERVICE = (
    "https://services2.arcgis.com/qvkbeam7Wirps6zC/arcgis/rest/services/"
    "BaseUnitFeatures/FeatureServer"
)
PAGE_SIZE = 2_000


@dataclass(frozen=True)
class LayerDefinition:
    name: str
    layer_id: int
    out_fields: str = "*"
    return_geometry: bool = True


LAYERS = {
    "addresses": LayerDefinition("addresses", 0),
    "streets": LayerDefinition("streets", 1),
    "buildings": LayerDefinition("buildings", 2),
}


def _post_json(session, url: str, data: dict, *, timeout: int) -> dict:
    response = session.post(url, data=data, timeout=timeout)
    response.raise_for_status()
    payload = response.json()
    if "error" in payload:
        raise RuntimeError(f"ArcGIS error: {payload['error']}")
    return payload


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _returned_ids(payload: dict) -> set[int]:
    if not isinstance(payload.get("features"), list):
        return set()
    returned = set()
    for feature in payload["features"]:
        value = feature.get("properties", {}).get("objectid")
        if value is None:
            value = feature.get("properties", {}).get("OBJECTID")
        try:
            returned.add(int(value))
        except (TypeError, ValueError):
            continue
    return returned


def _layer_fingerprint(metadata: dict, object_ids: list[int]) -> dict:
    """Capture only source facts that must remain stable throughout pagination."""
    fields = [
        {
            "name": field.get("name"),
            "type": field.get("type"),
            "alias": field.get("alias"),
        }
        for field in metadata.get("fields", [])
    ]
    stable = {
        "id": metadata.get("id"),
        "name": metadata.get("name"),
        "type": metadata.get("type"),
        "geometryType": metadata.get("geometryType"),
        "objectIdField": metadata.get("objectIdField"),
        "fields": fields,
        "spatialReference": metadata.get("extent", {}).get("spatialReference"),
        "lastEditDate": metadata.get("editingInfo", {}).get("lastEditDate"),
        "object_id_count": len(object_ids),
        "object_ids_sha256": hashlib.sha256(",".join(map(str, object_ids)).encode()).hexdigest(),
    }
    stable["fingerprint_sha256"] = hashlib.sha256(
        json.dumps(stable, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    return stable


def _source_state(session, layer_url: str, *, timeout: int) -> tuple[dict, list[int]]:
    metadata = _post_json(session, layer_url, {"f": "json"}, timeout=timeout)
    payload = _post_json(
        session,
        f"{layer_url}/query",
        {"where": "1=1", "returnIdsOnly": "true", "f": "json"},
        timeout=timeout,
    )
    raw_ids = payload.get("objectIds")
    if not isinstance(raw_ids, list):
        raise TypeError("ArcGIS object-ID response is malformed")
    object_ids = [int(object_id) for object_id in raw_ids]
    if len(set(object_ids)) != len(object_ids):
        raise RuntimeError("ArcGIS object-ID response contains duplicates")
    return metadata, sorted(object_ids)


def _valid_page(path: Path, expected_ids: set[int]) -> bool:
    if not path.exists():
        return False
    try:
        payload = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError):
        return False
    # Object-ID batches can shift when the source changes. Reuse is safe only when the cache
    # contains exactly this batch; partial intersection would silently mix snapshot versions.
    return _returned_ids(payload) == expected_ids


def _write_feature_collection(page_paths: Iterable[Path], destination: Path) -> int:
    temporary = destination.with_suffix(destination.suffix + ".tmp")
    count = 0
    with temporary.open("w", encoding="utf-8") as stream:
        stream.write('{"type":"FeatureCollection","features":[')
        first = True
        for page_path in page_paths:
            page = json.loads(page_path.read_text(encoding="utf-8"))
            for feature in page.get("features", []):
                if not first:
                    stream.write(",")
                json.dump(feature, stream, separators=(",", ":"))
                first = False
                count += 1
        stream.write("]}")
    temporary.replace(destination)
    return count


def fetch_layer(
    layer: LayerDefinition,
    output_dir: Path,
    *,
    session=requests,
    timeout: int = 120,
    pause_seconds: float = 0.05,
    discard_pages: bool = False,
    page_cache_root: Path | None = None,
) -> tuple[Path, dict]:
    """Fetch one Base Units layer in resumable pages and write a source manifest."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    page_dir = Path(page_cache_root or output_dir / f".{layer.name}_pages")
    layer_url = f"{BASE_UNITS_SERVICE}/{layer.layer_id}"
    query_url = f"{layer_url}/query"
    metadata_before, object_ids = _source_state(session, layer_url, timeout=timeout)
    fingerprint_before = _layer_fingerprint(metadata_before, object_ids)
    page_dir = page_dir / fingerprint_before["fingerprint_sha256"]
    page_dir.mkdir(parents=True, exist_ok=True)

    page_paths = []
    downloaded_pages = 0
    reused_pages = 0
    for start in range(0, len(object_ids), PAGE_SIZE):
        batch = object_ids[start : start + PAGE_SIZE]
        page_path = page_dir / f"{start:09d}.json"
        page_paths.append(page_path)
        if _valid_page(page_path, set(batch)):
            reused_pages += 1
            continue
        payload = _post_json(
            session,
            query_url,
            {
                "objectIds": ",".join(map(str, batch)),
                "outFields": layer.out_fields,
                "returnGeometry": str(layer.return_geometry).lower(),
                "outSR": 4326,
                "f": "geojson",
            },
            timeout=timeout,
        )
        returned_ids = _returned_ids(payload)
        if returned_ids != set(batch):
            missing = sorted(set(batch) - returned_ids)
            unexpected = sorted(returned_ids - set(batch))
            raise RuntimeError(
                f"ArcGIS returned an incomplete {layer.name} page at offset {start}: "
                f"missing={missing[:5]}, unexpected={unexpected[:5]}"
            )
        temporary = page_path.with_suffix(".tmp")
        temporary.write_text(json.dumps(payload, separators=(",", ":")))
        temporary.replace(page_path)
        downloaded_pages += 1
        time.sleep(pause_seconds)

    metadata_after, object_ids_after = _source_state(session, layer_url, timeout=timeout)
    fingerprint_after = _layer_fingerprint(metadata_after, object_ids_after)
    if fingerprint_before != fingerprint_after:
        raise RuntimeError(
            f"ArcGIS {layer.name} layer changed during pagination; snapshot rejected"
        )

    destination = output_dir / f"base_units_{layer.name}.geojson"
    feature_count = _write_feature_collection(page_paths, destination)
    manifest = {
        "collected_at": datetime.now(UTC).isoformat(),
        "service": BASE_UNITS_SERVICE,
        "layer": asdict(layer),
        "object_id_count": len(object_ids),
        "source_fingerprint_before": fingerprint_before,
        "source_fingerprint_after": fingerprint_after,
        "feature_count": feature_count,
        "page_size": PAGE_SIZE,
        "downloaded_pages": downloaded_pages,
        "reused_pages": reused_pages,
        "output": destination.name,
        "sha256": _sha256(destination),
    }
    manifest_path = output_dir / f"base_units_{layer.name}.manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")

    if discard_pages:
        import shutil

        shutil.rmtree(page_dir)
    return destination, manifest
