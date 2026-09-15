#!/usr/bin/env python3
"""Extract Detroit BZA case records from PDFs with Gemini native PDF vision.

Safe defaults process one unextracted document. Use --all only after reviewing a
pilot and accepting API cost. Every response is schema-validated and written per
document; existing outputs are never overwritten unless --force is supplied.
"""

from __future__ import annotations

import concurrent.futures
import hashlib
import json
import os
import random
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace
from typing import Literal

from pydantic import BaseModel, Field, model_validator

from .._cache import atomic_json

DEFAULT_MODEL = "gemini-3.8-flash"
MANIFEST_LOCK = threading.Lock()


class BzaCase(BaseModel):
    case_number: str | None
    meeting_date: str
    hearing_time: str | None
    council_district: int | None = Field(default=None, ge=1, le=7)
    petitioner: str | None
    location: str | None
    legal_description: str | None
    proposal: str | None
    bseed_refs: list[str] = Field(default_factory=list)
    action: str | None
    affirmative_votes: list[str] = Field(default_factory=list)
    affirmative_count: int = Field(ge=0)
    negative_votes: list[str] = Field(default_factory=list)
    negative_count: int = Field(ge=0)
    abstentions: list[str] = Field(default_factory=list)
    decision: str | None
    decision_status: Literal[
        "decided",
        "under_advisement",
        "tabled",
        "postponed",
        "withdrawn",
        "dismissed",
        "not_recorded",
        "no_action",
        "unknown",
    ]
    confidence: Literal["high", "medium", "low"]
    confidence_note: str | None

    @model_validator(mode="after")
    def check_counts(self):
        if self.affirmative_count != len(self.affirmative_votes):
            raise ValueError("affirmative_count does not match names")
        if self.negative_count != len(self.negative_votes):
            raise ValueError("negative_count does not match names")
        return self


class Extraction(BaseModel):
    meeting_date: str
    cases: list[BzaCase]
    document_notes: str | None = None


PROMPT = """You are extracting official Detroit Board of Zoning Appeals meeting
minutes. Read the PDF visually, respecting its two-column and labeled layout.
Return every CASE NO. block, including cases continued, adjourned, dismissed, or
taken under advisement. Skip roll call, procedural boilerplate, and approval of
prior minutes.

Critical rules:
- APPLICANT and BZA PETITIONER both map to petitioner.
- Never return a printed label such as APPLICANT, LOCATION, or BZA as a value.
- Council district may appear beside CASE NO. or inside LOCATION; check both.
- Preserve legal description, proposal, action, and final decision faithfully.
- A blank Negative line means an empty list and count 0.
- Count vote-name lists exactly. Do not include mover/seconder as votes unless
  they appear in the vote list.
- Keep each case occurrence in this meeting, even if it appeared previously.
- Do not invent absent values. Use null and lower confidence, explaining why.
- The final bold/capitalized disposition is decision. Classify it using the
  supplied decision_status enum.
- meeting_date must be {meeting_date}, derived from the source filename.

Perform a second pass before answering: enumerate visible CASE NO. blocks and
ensure the output has exactly one record for each."""


def date_from_name(path: Path) -> str:
    from .filenames import parse_date

    value = parse_date(path.name)
    if value is None:
        raise ValueError(f"No valid meeting date in PDF filename: {path.name}")
    return value.isoformat()


def append_manifest(record: dict, manifest: Path) -> None:
    manifest.parent.mkdir(parents=True, exist_ok=True)
    with MANIFEST_LOCK:
        with manifest.open("a") as handle:
            handle.write(json.dumps(record) + "\n")


def extract_one(
    client, pdf: Path, model: str, attempts: int, raw_dir: Path
) -> Extraction:
    from google.genai import types

    uploaded = client.files.upload(
        file=pdf,
        config={"mime_type": "application/pdf", "display_name": pdf.name},
    )
    try:
        for attempt in range(1, attempts + 1):
            try:
                response = client.models.generate_content(
                    model=model,
                    contents=[
                        types.Part.from_uri(
                            file_uri=uploaded.uri, mime_type="application/pdf"
                        ),
                        PROMPT.format(meeting_date=date_from_name(pdf)),
                    ],
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        response_schema=Extraction,
                    ),
                )
                raw_dir.mkdir(parents=True, exist_ok=True)
                (raw_dir / f"{pdf.stem}.json").write_text(response.text)
                return Extraction.model_validate_json(response.text)
            except Exception:
                if attempt == attempts:
                    raise
                time.sleep((2**attempt) + random.random())
    finally:
        try:
            client.files.delete(name=uploaded.name)
        except Exception:
            pass


def run(
    *,
    pdf_dir: Path,
    output_dir: Path,
    model=None,
    limit=1,
    all=False,
    force=False,
    dry_run=True,
    attempts=3,
    workers=1,
    allow_paid=False,
) -> int:
    args = SimpleNamespace(
        pdf_dir=pdf_dir,
        output_dir=output_dir / "per_doc",
        model=model,
        limit=limit,
        all=all,
        force=force,
        dry_run=dry_run,
        attempts=attempts,
        workers=workers,
        pdf=None,
    )
    if not dry_run and not allow_paid:
        raise ValueError("Paid extraction requires explicit allow_paid=True")
    if attempts < 1 or workers < 1 or limit < 0:
        raise ValueError("Invalid extraction limits")
    raw_dir = output_dir / "gemini_raw"
    manifest = output_dir / "gemini_manifest.jsonl"
    model = args.model or DEFAULT_MODEL
    queue = [args.pdf] if args.pdf is not None else sorted(args.pdf_dir.glob("*.pdf"))
    if args.pdf is not None and not args.pdf.exists():
        raise SystemExit(f"PDF does not exist: {args.pdf}")

    def fingerprint(pdf):
        return {
            "source_sha256": hashlib.sha256(pdf.read_bytes()).hexdigest(),
            "model": model,
            "prompt_sha256": hashlib.sha256(PROMPT.encode()).hexdigest(),
            "schema_sha256": hashlib.sha256(
                json.dumps(Extraction.model_json_schema(), sort_keys=True).encode()
            ).hexdigest(),
        }

    def needed(pdf):
        target = args.output_dir / f"{pdf.stem}_cases.json"
        meta = output_dir / "fingerprints" / f"{pdf.stem}.json"
        if force or not target.exists():
            return True
        json.loads(target.read_text())
        return meta.exists() and json.loads(meta.read_text()) != fingerprint(pdf)

    queue = [pdf for pdf in queue if needed(pdf)]
    if not args.all:
        queue = queue[: max(args.limit, 0)]
    print(f"{len(queue)} document(s) selected with model {model}")
    for pdf in queue:
        date_from_name(pdf)
        print(pdf)
    if args.dry_run or not queue:
        return 0
    if not os.getenv("GEMINI_API_KEY"):
        raise SystemExit("GEMINI_API_KEY is not set in .env or the environment")

    from google import genai

    args.output_dir.mkdir(parents=True, exist_ok=True)

    def process(pdf: Path) -> tuple[Path, bool, str]:
        started = datetime.now(timezone.utc)
        # One client per task avoids relying on undocumented client thread safety.
        client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
        try:
            extraction = extract_one(client, pdf, model, args.attempts, raw_dir)
            output = args.output_dir / f"{pdf.stem}_cases.json"
            atomic_json(output, [case.model_dump() for case in extraction.cases])
            atomic_json(
                output_dir / "fingerprints" / f"{pdf.stem}.json", fingerprint(pdf)
            )
            append_manifest(
                {
                    "source_file": pdf.name,
                    **fingerprint(pdf),
                    "model": model,
                    "started_at": started.isoformat(),
                    "finished_at": datetime.now(timezone.utc).isoformat(),
                    "case_count": len(extraction.cases),
                    "status": "success",
                    "document_notes": extraction.document_notes,
                },
                manifest,
            )
            return pdf, True, f"{len(extraction.cases)} cases -> {output}"
        except Exception as exc:
            append_manifest(
                {
                    "source_file": pdf.name,
                    **fingerprint(pdf),
                    "model": model,
                    "started_at": started.isoformat(),
                    "finished_at": datetime.now(timezone.utc).isoformat(),
                    "status": "failed",
                    "error": repr(exc),
                },
                manifest,
            )
            return pdf, False, f"FAILED: {exc}"

    failures = 0
    workers = max(1, args.workers)
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(process, pdf): pdf for pdf in queue}
        completed = 0
        for future in concurrent.futures.as_completed(futures):
            completed += 1
            pdf, ok, message = future.result()
            failures += not ok
            print(f"[{completed}/{len(queue)}] {pdf.name}: {message}")

    return 1 if failures else 0
