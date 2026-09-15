#!/usr/bin/env python3
"""Classify the real-world projects behind Detroit BZA cases with Gemini.

This is deliberately separate from the legal-relief classifier. It asks what
the applicant proposed to build, open, expand, retain, or alter—not which
internally inconsistent zoning-code category brought the matter to the Board.

Safe defaults select at most one batch of denied cases. Use --all only after
reviewing the pilot output and accepting API cost.
"""

from __future__ import annotations

import concurrent.futures
import hashlib
import json
import os
import random
import threading
import time
from pathlib import Path
from types import SimpleNamespace
from typing import Literal

import pandas as pd
from pydantic import BaseModel, Field, model_validator

from .._cache import atomic_json

DEFAULT_MODEL = "gemini-3.1-pro-preview"
WRITE_LOCK = threading.Lock()


class ProjectClassification(BaseModel):
    case_history_id: str
    project_type_family: Literal[
        "housing",
        "mixed_use",
        "retail_or_personal_service",
        "food_or_beverage",
        "office_or_medical",
        "industrial_or_logistics",
        "vehicle_oriented",
        "cannabis_or_controlled_use",
        "institutional_or_civic",
        "religious",
        "recreation_or_open_space",
        "signage",
        "parking_only",
        "other",
        "unclear",
    ]
    project_type_label: str = Field(
        description=(
            "Concise ordinary-language type, e.g. duplex, apartment building, "
            "restaurant, daycare, trucking yard, or digital billboard."
        )
    )
    proposed_action: Literal[
        "new_construction",
        "change_of_use",
        "expansion",
        "site_or_building_alteration",
        "continue_or_legalize_existing_condition",
        "signage_installation",
        "demolition",
        "other",
        "unclear",
    ]
    intensity_direction: Literal[
        "adds_homes_or_activity",
        "maintains_existing_activity",
        "reduces_homes_or_activity",
        "unclear_or_not_applicable",
    ]
    urban_form_orientation: Literal[
        "pedestrian_or_transit_supportive",
        "mixed_or_neutral",
        "automobile_oriented",
        "industrial_or_freight_oriented",
        "unclear_or_not_applicable",
    ]
    proposal_language_tone: Literal[
        "favorable",
        "neutral",
        "adverse",
        "mixed",
        "insufficient_text",
    ] = Field(
        description=(
            "Tone of the minutes' language about the proposed project—not a "
            "judgment of whether the project is socially desirable."
        )
    )
    housing_units: int | None = Field(default=None, ge=0)
    summary: str
    evidence: list[str] = Field(
        default_factory=list,
        description="One to three short phrases copied from the supplied text.",
    )
    confidence: Literal["high", "medium", "low"]
    alternative_type: str | None = Field(
        default=None,
        description="A plausible competing project type when ambiguity matters.",
    )


class BatchResult(BaseModel):
    classifications: list[ProjectClassification]

    @model_validator(mode="after")
    def unique_ids(self):
        ids = [item.case_history_id for item in self.classifications]
        if len(ids) != len(set(ids)):
            raise ValueError("duplicate case_history_id in response")
        return self


PROMPT = """You are classifying proposed real-world land uses in Detroit Board
of Zoning Appeals case summaries.

This is NOT a zoning-code classification task. Ignore the formal variance,
appeal, district, section number, and legal-relief label except where they help
you understand the physical proposal. Detroit's code categories are not the
taxonomy. Classify what the proposal would create, operate, expand, retain, or
alter in ordinary civic and urban-development language.

Important distinctions:
- project_type_family is a broad analytic family; project_type_label is the
  specific ordinary-language use.
- housing covers projects whose primary context is a residence or residential
  development, including new dwellings, residential additions, and accessory
  work such as a garage or carport serving a residence.
- mixed_use requires a material residential and nonresidential combination;
  do not use housing for those projects.
- parking_only means parking is itself the project. Do not classify an
  apartment, store, or restaurant as parking_only merely because its case
  requests parking relief.
- proposal_language_tone describes how the supplied minutes characterize the
  project. It is not your opinion of the project and not the Board outcome.
- Use adverse only where the text itself alleges harms, incompatibility,
  nuisance, danger, or similar concerns; use neutral for ordinary procedural
  description.
- Do not infer housing-unit counts or facts absent from the supplied text.
- Evidence must quote only short phrases present in the supplied record.
- The output must contain exactly one classification for every supplied
  case_history_id and no others.

Cases:
{cases_json}
"""


def case_payload(row: pd.Series) -> dict:
    def value(key):
        cell = row.get(key)
        return None if cell is None or pd.isna(cell) else cell

    return {
        "case_history_id": value("case_history_id"),
        "case_number": value("printed_case_number"),
        "petitioner": value("petitioner"),
        "location": value("location"),
        "proposal": str(value("proposal") or "")[:9000],
        "recorded_outcome": value("final_outcome"),
    }


def classify_batch(
    rows: list[dict],
    model: str,
    attempts: int,
    raw_dir: Path,
) -> list[ProjectClassification]:
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    expected = {row["case_history_id"] for row in rows}
    prompt = PROMPT.format(cases_json=json.dumps(rows, ensure_ascii=False, indent=2))
    for attempt in range(1, attempts + 1):
        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=BatchResult,
                    temperature=0,
                ),
            )
            parsed = BatchResult.model_validate_json(response.text)
            returned = {item.case_history_id for item in parsed.classifications}
            if returned != expected:
                raise ValueError(
                    f"ID mismatch; missing={sorted(expected - returned)}, "
                    f"unexpected={sorted(returned - expected)}"
                )
            digest = rows[0]["case_history_id"].replace("/", "_")
            raw_dir.mkdir(parents=True, exist_ok=True)
            with WRITE_LOCK:
                (raw_dir / f"{digest}.json").write_text(response.text, encoding="utf-8")
            return parsed.classifications
        except Exception:
            if attempt == attempts:
                raise
            time.sleep((2**attempt) + random.random())
    raise RuntimeError("unreachable")


def write_results(items: list[ProjectClassification], per_case_dir: Path) -> None:
    per_case_dir.mkdir(parents=True, exist_ok=True)
    with WRITE_LOCK:
        for item in items:
            path = per_case_dir / f"{item.case_history_id}.json"
            atomic_json(path, item.model_dump())


def merge_results(histories_path: Path, output_dir: Path) -> None:
    per_case_dir = output_dir / "per_case"
    merged = output_dir / "project_types.csv"
    joined_path = output_dir / "case_histories_with_project_types.csv"
    review_path = output_dir / "review_medium_low_confidence.csv"
    audit_path = output_dir / "project_type_audit.json"
    records = [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted(per_case_dir.glob("*.json"))
    ]
    output_dir.mkdir(parents=True, exist_ok=True)
    classifications = pd.DataFrame(
        records, columns=list(ProjectClassification.model_fields)
    )
    classifications.to_csv(merged, index=False)
    histories = pd.read_csv(histories_path)
    joined = histories.merge(
        classifications,
        on="case_history_id",
        how="left",
        validate="one_to_one",
    )
    joined.to_csv(joined_path, index=False)
    review = joined[joined["confidence"].isin(["medium", "low"])]
    review.to_csv(review_path, index=False)
    audit = {
        "case_histories": int(len(histories)),
        "classifications": int(len(classifications)),
        "unique_classified_ids": int(classifications["case_history_id"].nunique()),
        "unmatched_histories": int(joined["project_type_family"].isna().sum()),
        "project_type_families": {
            str(key): int(value)
            for key, value in classifications["project_type_family"]
            .value_counts()
            .items()
        },
        "confidence": {
            str(key): int(value)
            for key, value in classifications["confidence"].value_counts().items()
        },
        "review_records": int(len(review)),
    }
    audit_path.write_text(json.dumps(audit, indent=2), encoding="utf-8")
    print(f"Merged {len(records)} classifications -> {merged}")
    print(f"Joined case histories -> {joined_path}")
    print(f"Review queue: {len(review)} -> {review_path}")


def run(
    *,
    histories_path: Path,
    output_dir: Path,
    model=None,
    outcomes="",
    batch_size=12,
    limit=12,
    all=False,
    force=False,
    dry_run=True,
    workers=1,
    attempts=3,
    allow_paid=False,
) -> int:
    if not dry_run and not allow_paid:
        raise ValueError("Paid classification requires explicit allow_paid=True")
    if batch_size < 1 or workers < 1 or attempts < 1 or limit < 0:
        raise ValueError("Invalid classification limits")
    args = SimpleNamespace(
        model=model,
        outcomes=outcomes,
        batch_size=batch_size,
        limit=limit,
        all=all,
        force=force,
        dry_run=dry_run,
        workers=workers,
        attempts=attempts,
    )
    per_case_dir = output_dir / "per_case"
    model = args.model or os.getenv("GEMINI_MODEL", DEFAULT_MODEL)
    outcomes = {value.strip() for value in args.outcomes.split(",") if value.strip()}
    histories = pd.read_csv(histories_path)
    selected = (
        histories[histories["final_outcome"].isin(outcomes)].copy()
        if outcomes
        else histories.copy()
    )

    def fingerprint(row):
        return {
            "payload": case_payload(row),
            "model": model,
            "prompt_sha256": hashlib.sha256(PROMPT.encode()).hexdigest(),
            "schema_sha256": hashlib.sha256(
                json.dumps(BatchResult.model_json_schema(), sort_keys=True).encode()
            ).hexdigest(),
        }

    def cached(row):
        case_id = row["case_history_id"]
        path = per_case_dir / f"{case_id}.json"
        meta = output_dir / "fingerprints" / f"{case_id}.json"
        if not path.exists():
            return False
        ProjectClassification.model_validate_json(path.read_text())
        return not meta.exists() or json.loads(meta.read_text()) == fingerprint(row)

    if not args.force:
        selected = selected[~selected.apply(cached, axis=1)]
    selected = selected.sort_values(["first_meeting_date", "case_history_id"])
    if not args.all:
        selected = selected.head(max(args.limit, 0))
    payloads = [case_payload(row) for _, row in selected.iterrows()]
    batches = [
        payloads[index : index + args.batch_size]
        for index in range(0, len(payloads), args.batch_size)
    ]
    print(
        f"{len(payloads)} case(s) in {len(batches)} batch(es); "
        f"model={model}; outcomes={sorted(outcomes)}"
    )
    if args.dry_run:
        for payload in payloads:
            print(
                f"  {payload['case_history_id']} · "
                f"{payload['case_number']} · {payload['location']}"
            )
        return 0
    if not batches:
        merge_results(histories_path, output_dir)
        return 0
    if not os.getenv("GEMINI_API_KEY"):
        raise SystemExit("GEMINI_API_KEY is not set in .env or environment")

    failures = 0
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=max(1, args.workers)
    ) as executor:
        futures = {
            executor.submit(
                classify_batch, batch, model, args.attempts, output_dir / "raw"
            ): batch
            for batch in batches
        }
        for future in concurrent.futures.as_completed(futures):
            batch = futures[future]
            try:
                results = future.result()
                write_results(results, per_case_dir)
                for item in results:
                    row = histories[
                        histories.case_history_id == item.case_history_id
                    ].iloc[0]
                    atomic_json(
                        output_dir / "fingerprints" / f"{item.case_history_id}.json",
                        fingerprint(row),
                    )
                print(f"{len(results)} classified: {batch[0]['case_history_id']} …")
            except Exception as exc:
                failures += 1
                print(
                    f"FAILED batch beginning {batch[0]['case_history_id']}: "
                    f"{type(exc).__name__}: {exc}"
                )
    merge_results(histories_path, output_dir)
    return 1 if failures else 0
