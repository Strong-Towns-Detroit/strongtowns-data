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
) -> tuple[Path, dict]:
    """Fetch one Base Units layer in resumable pages and write a source manifest."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    page_dir = output_dir / f".{layer.name}_pages"
    page_dir.mkdir(exist_ok=True)
    query_url = f"{BASE_UNITS_SERVICE}/{layer.layer_id}/query"
    object_ids = _post_json(
        session,
        query_url,
        {"where": "1=1", "returnIdsOnly": "true", "f": "json"},
        timeout=timeout,
    ).get("objectIds", [])
    object_ids = sorted(int(object_id) for object_id in object_ids)

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

    destination = output_dir / f"base_units_{layer.name}.geojson"
    feature_count = _write_feature_collection(page_paths, destination)
    manifest = {
        "collected_at": datetime.now(UTC).isoformat(),
        "service": BASE_UNITS_SERVICE,
        "layer": asdict(layer),
        "object_id_count": len(object_ids),
        "feature_count": feature_count,
        "page_size": PAGE_SIZE,
        "downloaded_pages": downloaded_pages,
        "reused_pages": reused_pages,
        "output": str(destination),
        "sha256": _sha256(destination),
    }
    manifest_path = output_dir / f"base_units_{layer.name}.manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")

    if discard_pages:
        import shutil

        shutil.rmtree(page_dir)
    return destination, manifest
