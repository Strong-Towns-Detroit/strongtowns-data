"""Verified prepared-release cache. No pipeline or provider imports."""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import tempfile
import time
import urllib.request
import zipfile
from contextlib import contextmanager
from pathlib import Path, PurePosixPath

INDEX_URL = "https://github.com/Strong-Towns-Detroit/strongtowns-data/releases/latest/download/bza-index.json"
SCHEMA_VERSION = 1
_NOTIFIED: set[tuple] = set()


def cache_root(path=None) -> Path:
    return Path(
        path
        or os.environ.get("STRONGTOWNS_BZA_CACHE")
        or Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache"))
        / "strongtowns/bza"
    )


def read_json(path, default=None):
    try:
        return json.loads(Path(path).read_text())
    except FileNotFoundError:
        return default


def atomic_json(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(dir=path.parent, prefix=".state-")
    try:
        with os.fdopen(fd, "w") as stream:
            json.dump(value, stream, indent=2)
            stream.write("\n")
        os.replace(temporary, path)
    finally:
        Path(temporary).unlink(missing_ok=True)


@contextmanager
def locked(root):
    root.mkdir(parents=True, exist_ok=True)
    with (root / ".lock").open("a+b") as stream:
        if os.name == "nt":
            import msvcrt

            if stream.tell() == 0:
                stream.write(b"0")
                stream.flush()
            stream.seek(0)
            msvcrt.locking(stream.fileno(), msvcrt.LK_LOCK, 1)
            try:
                yield
            finally:
                stream.seek(0)
                msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
        else:
            import fcntl

            fcntl.flock(stream, fcntl.LOCK_EX)
            try:
                yield
            finally:
                fcntl.flock(stream, fcntl.LOCK_UN)


def version_name(value):
    if not isinstance(value, str) or not re.fullmatch(
        r"[A-Za-z0-9][A-Za-z0-9._-]{0,100}", value
    ):
        raise ValueError("Invalid BZA release version")
    return value


def https_open(url, timeout):
    if not url.startswith("https://"):
        raise ValueError("BZA releases require HTTPS")
    response = urllib.request.urlopen(
        urllib.request.Request(
            url,
            headers={
                "User-Agent": "strongtowns-data-bza",
            },
        ),
        timeout=timeout,
    )
    if not response.geturl().startswith("https://"):
        response.close()
        raise ValueError("BZA release redirected away from HTTPS")
    return response


def validate_release(item):
    from datetime import date

    version_name(item["version"])
    for key in ("coverage_start", "coverage_end"):
        date.fromisoformat(item[key])
    if item["coverage_start"] > item["coverage_end"]:
        raise ValueError("Invalid BZA coverage range")
    if not re.fullmatch("[0-9a-f]{64}", item["sha256"]):
        raise ValueError("Invalid BZA checksum")
    if not item["url"].startswith("https://"):
        raise ValueError("BZA releases require HTTPS")
    return item


def check(root: Path, *, force=False):
    """Index releases are newest first; unsupported schemas are skipped."""
    with locked(root):
        state = read_json(root / "state.json", {})
        if not force and time.time() - state.get("checked_at", 0) < 86400:
            return state
        state["checked_at"] = time.time()
        try:
            with https_open(
                os.environ.get("STRONGTOWNS_BZA_INDEX_URL", INDEX_URL), 2
            ) as response:
                payload = json.loads(response.read(1024 * 1024))
            releases = [
                validate_release(item)
                for item in payload["releases"]
                if item.get("schema_version") == SCHEMA_VERSION
            ]
            if not releases:
                raise ValueError("No compatible BZA release is available")
            state.update(releases=releases, latest=releases[0])
            state.pop("check_error", None)
        except Exception as error:
            state["check_error"] = str(error)
            if force:
                atomic_json(root / "state.json", state)
                raise RuntimeError(
                    "Could not check BZA releases. Retry: strongtowns bza fetch"
                ) from error
        atomic_json(root / "state.json", state)
        return state


def verify(directory: Path):
    manifest = read_json(directory / "bza-manifest.json")
    if not manifest or manifest.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("Unsupported or missing BZA manifest")
    version_name(manifest["version"])
    files = manifest["files"]
    actual = {
        str(p.relative_to(directory)) for p in directory.rglob("*") if p.is_file()
    }
    if actual != set(files) | {"bza-manifest.json"}:
        raise ValueError("BZA archive contains missing or undeclared files")
    for required in (
        "case_histories.csv",
        "case_occurrences.csv",
        "case_categories.csv",
    ):
        if required not in files:
            raise ValueError(f"Missing BZA artifact: {required}")
    for name, digest in files.items():
        relative = PurePosixPath(name)
        if relative.is_absolute() or ".." in relative.parts or "\\" in name:
            raise ValueError("Unsafe BZA artifact path")
        path = directory / name
        if path.is_symlink() or not path.resolve().is_relative_to(directory.resolve()):
            raise ValueError("Unsafe BZA artifact")
        if hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            raise ValueError(f"BZA checksum mismatch: {name}")
    return manifest


def fetch(*, version=None, cache=None, select=True):
    root = cache_root(cache)
    state = check(root, force=True)
    release = (
        next((r for r in state["releases"] if r["version"] == version), None)
        if version
        else state["latest"]
    )
    if release is None:
        raise ValueError(f"BZA version is unavailable: {version}")
    name = version_name(release["version"])
    with locked(root):
        target = root / "versions" / name
        if not target.exists():
            target.parent.mkdir(parents=True, exist_ok=True)
            with tempfile.TemporaryDirectory(
                dir=root, prefix=".download-"
            ) as temporary:
                work = Path(temporary)
                archive = work / "data.zip"
                digest = hashlib.sha256()
                with (
                    https_open(release["url"], 30) as source,
                    archive.open("wb") as output,
                ):
                    size = 0
                    while chunk := source.read(1024 * 1024):
                        size += len(chunk)
                        if size >= 2 * 1024**3:
                            raise ValueError("BZA archive exceeds release size limit")
                        digest.update(chunk)
                        output.write(chunk)
                if digest.hexdigest() != release["sha256"]:
                    raise ValueError(
                        "BZA archive checksum mismatch; installed data unchanged"
                    )
                unpacked = work / "unpacked"
                unpacked.mkdir()
                with zipfile.ZipFile(archive) as bundle:
                    if sum(i.file_size for i in bundle.infolist()) > 4 * 1024**3:
                        raise ValueError("BZA archive expands beyond size limit")
                    names = set()
                    for member in bundle.infolist():
                        path = PurePosixPath(member.filename)
                        if (
                            path.is_absolute()
                            or ".." in path.parts
                            or "\\" in member.filename
                            or member.filename in names
                            or member.external_attr >> 16 & 0o170000 == 0o120000
                        ):
                            raise ValueError("Unsafe BZA archive member")
                        names.add(member.filename)
                    bundle.extractall(unpacked)
                manifest = verify(unpacked)
                if any(
                    manifest.get(k) != release.get(k)
                    for k in (
                        "version",
                        "schema_version",
                        "coverage_start",
                        "coverage_end",
                    )
                ):
                    raise ValueError("BZA release and manifest disagree")
                from . import BzaDataset

                BzaDataset(unpacked, manifest=manifest)
                os.replace(unpacked, target)
        manifest = verify(target)
        state = read_json(root / "state.json", {})
        state.setdefault("downloaded", {})[name] = release["sha256"]
        if select:
            state["current"] = name
        atomic_json(root / "state.json", state)
    return manifest


def notice(state, installed, *, pinned=False, stream=None, once=True):
    stream = stream if stream is not None else sys.stderr
    latest = state.get("latest")
    if not latest or not installed or latest["version"] == installed.get("version"):
        return
    # Do not advertise a rollback when the index is stale or a pin is newer.
    versions = [r["version"] for r in state.get("releases", [])]
    if (
        installed.get("version") not in versions
        and installed.get("coverage_end", "") > latest["coverage_end"]
    ):
        return
    key = (installed.get("version"), latest["version"], pinned)
    if once and key in _NOTIFIED:
        return
    _NOTIFIED.add(key)
    coverage = latest["coverage_end"] > installed.get("coverage_end", "")
    old = installed.get("coverage_end") if coverage else installed.get("version")
    new = latest["coverage_end"] if coverage else latest["version"]
    command = "strongtowns bza fetch"
    color = (
        getattr(stream, "isatty", lambda: False)()
        and "NO_COLOR" not in os.environ
        and os.environ.get("TERM") != "dumb"
    )
    if color:
        new = f"\033[32m{new}\033[0m"
        command = f"\033[1;36m{command}\033[0m"
    kind = "coverage" if coverage else "data"
    print(
        f"New BZA case {kind} is available: {old} -> {new}. To update, run:\n\n    {command}",
        file=stream,
    )
    if pinned:
        print("This dataset is pinned; fetching does not change its pin.", file=stream)
