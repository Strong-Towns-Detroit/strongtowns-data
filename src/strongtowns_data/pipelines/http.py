"""Immutable acquisition of a public file."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import requests


@dataclass(frozen=True)
class DownloadedFile:
    path: Path
    url: str
    sha256: str
    size: int
    etag: str | None
    last_modified: str | None
    started_at: str
    completed_at: str


def download_file(url: str, output: Path, *, session=None) -> DownloadedFile:
    started_at = datetime.now(timezone.utc).isoformat()
    session = session or requests.Session()
    response = session.get(url, stream=True, timeout=120)
    response.raise_for_status()
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_suffix(output.suffix + ".tmp")
    digest = hashlib.sha256()
    size = 0
    with temporary.open("wb") as handle:
        for block in response.iter_content(chunk_size=8 * 1024 * 1024):
            if not block:
                continue
            handle.write(block)
            digest.update(block)
            size += len(block)
    declared = response.headers.get("content-length")
    if declared is not None and int(declared) != size:
        temporary.unlink(missing_ok=True)
        raise ValueError(f"download size mismatch: {size} != {declared}")
    temporary.replace(output)
    return DownloadedFile(
        output, url, digest.hexdigest(), size,
        response.headers.get("etag"), response.headers.get("last-modified"),
        started_at, datetime.now(timezone.utc).isoformat(),
    )
