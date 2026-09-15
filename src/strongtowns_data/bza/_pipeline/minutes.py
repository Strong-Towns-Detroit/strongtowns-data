"""Internal acquisition of BZA source PDFs with resumable verified writes."""

from __future__ import annotations

import hashlib
import json
import os
import re
import tempfile
from pathlib import Path
from urllib.parse import unquote, urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .._cache import atomic_json


def download_bza_minutes(output_dir: Path, *, apply=False):
    """Acquire sources only when explicitly applied; leave errors in the audit."""
    output = Path(output_dir)
    if not apply:
        return {"applied": False, "output": str(output)}
    output.mkdir(parents=True, exist_ok=True)
    ledger_path = output / "acquisition.json"
    ledger = (
        json.loads(ledger_path.read_text())
        if ledger_path.exists()
        else {"documents": {}}
    )
    failures = []
    session = requests.Session()
    session.mount(
        "https://",
        HTTPAdapter(
            max_retries=Retry(
                total=3, backoff_factor=0.5, status_forcelist=[429, 500, 502, 503, 504]
            )
        ),
    )
    session.headers["User-Agent"] = "StrongTowns-BZA/1.0"
    url = "https://detroitmi.gov/documents"
    params = {
        "name": "",
        "field_department_target_id": "",
        "field_department_target_id_1": "BZA Meeting Minutes (5916)",
        "field_description_value": "",
    }
    visited = set()
    try:
        for page in range(1000):
            response = session.get(url, params={**params, "page": page}, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")
            links = {
                urljoin(url, a["href"])
                for a in soup.select("a[href]")
                if a["href"].startswith("/document/")
            }
            fresh = links - visited
            if links and not fresh:
                raise ValueError("Minutes pagination repeated a page")
            for doc_url in sorted(fresh):
                visited.add(doc_url)
                try:
                    doc = session.get(doc_url, timeout=30)
                    doc.raise_for_status()
                    pdfs = [
                        urljoin(doc_url, a["href"])
                        for a in BeautifulSoup(doc.content, "html.parser").select(
                            "a[href]"
                        )
                        if urlparse(a["href"]).path.lower().endswith(".pdf")
                    ]
                    if len(set(pdfs)) != 1:
                        raise ValueError("Document page must identify exactly one PDF")
                    pdf_url = pdfs[0]
                    old = ledger["documents"].get(doc_url)
                    if old and old.get("url") == pdf_url:
                        existing = output / old["filename"]
                        if (
                            existing.exists()
                            and hashlib.sha256(existing.read_bytes()).hexdigest()
                            == old["sha256"]
                        ):
                            continue
                    filename = re.sub(
                        r"[^a-zA-Z0-9._-]",
                        "_",
                        unquote(Path(urlparse(pdf_url).path).name),
                    )
                    # Keep date-bearing names, disambiguate different source URLs.
                    if any(
                        d["filename"] == filename and key != doc_url
                        for key, d in ledger["documents"].items()
                    ):
                        filename = f"{Path(filename).stem}-{hashlib.sha256(doc_url.encode()).hexdigest()[:10]}.pdf"
                    pdf = session.get(pdf_url, timeout=30)
                    pdf.raise_for_status()
                    if not pdf.content.startswith(b"%PDF"):
                        raise ValueError("Source is not a PDF")
                    fd, temp = tempfile.mkstemp(dir=output, prefix=".pdf-")
                    try:
                        with os.fdopen(fd, "wb") as stream:
                            stream.write(pdf.content)
                        os.replace(temp, output / filename)
                    finally:
                        Path(temp).unlink(missing_ok=True)
                    ledger["documents"][doc_url] = {
                        "url": pdf_url,
                        "filename": filename,
                        "sha256": hashlib.sha256(pdf.content).hexdigest(),
                    }
                    atomic_json(ledger_path, ledger)
                except Exception as error:
                    failures.append({"source": doc_url, "error": str(error)})
            if not soup.select('a[rel="next"], li.pager__item--next'):
                break
        else:
            failures.append({"source": url, "error": "Pagination limit reached"})
    except Exception as error:
        failures.append({"source": url, "error": str(error)})
    finally:
        session.close()
        ledger["failures"] = failures
        atomic_json(ledger_path, ledger)
    if failures:
        raise RuntimeError(
            f"{len(failures)} minutes acquisition failures; see {ledger_path}"
        )
    return ledger
