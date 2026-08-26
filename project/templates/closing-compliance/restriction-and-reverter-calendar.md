---
artifact_id: CLO-016
artifact_type: calendar
title: Restriction and reverter calendar
workstream: closing-compliance
service_code: LND
status: template
template_version: "1.0"
parcel_ids: []
owner_role: contractor_program_manager
decision_role: company_decision_authority
required_reviewer_role: michigan_licensed_attorney
legal_review_required: true
typst_issue_required: false
typst_source: null
latest_issue_id: null
created_at: 2026-08-26
updated_at: 2026-08-26
source_as_of: 2026-08-26
source_ids: [SRC-007, SRC-014]
depends_on: [CON-019]
supersedes: null
confidentiality: internal
---

# Restriction and reverter calendar

`CLO-016` · closing-compliance · service code `LND`

> **Parcel-specific.** Create one copy per candidate parcel under `working/candidate-parcels/<parcel-id>/`. Do not complete this template in place.

## Purpose

Calendar of restrictions, reverters and repurchase rights, tracked to expiry.

## When to use it

Immediately post-closing.

## Required inputs

- Recorded deed
- Development agreement
- `ACQ-025` abstract

## Instructions

- Track to **expiry**, not to the next milestone. A reverter that lapses is a title improvement worth recording.
- `SRC-014` Sec. III(B) requires Projects-pathway agreements to carry an explicit expiration date. Record it and diary the release.
- Where a Release of Interest is obtainable on completion (`SRC-007`), pursue it actively — it does not arrive on its own.
- An unchecked condition is `not_found` or `blocked` — never `verified`, never blank.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Every restriction and reverter calendared to expiry
- Release of Interest pursued and evidenced
- Counsel review recorded

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Sources

Requirements in this artifact trace to the following rows in `source-register.csv`. Re-verify before relying on any of them — agency requirements change without notice.

| Source | Document | Status | Pinpoint |
| --- | --- | --- | --- |
| `SRC-007` | Compliance | `verified` | Post-sale timeline table (15/45/60 day milestones); evidence rules; Release of Interest |
| `SRC-014` | Neighborhood Development Projects Policy (Procedures Governing the Disposition of Properties to Support City of Detroit Economic Development Projects) | `verified` | Sec. II (Qualified Properties); Sec. III(A) (zoning gate and option agreement); Sec. III(B)(1) (option deposit); Sec. III(C) (FMV, 12-month price expiry); Sec. III(C)(3)(b) (pricing credits); Sec. V(A)-(B) (approval thresholds) |

## Unresolved questions

_None recorded. Add any question that would change a decision if answered differently._

## Approvals and professional review

- **Required reviewer: `michigan_licensed_attorney`.** `legal_review_required: true` — every stage gate this artifact feeds is blocked until that review is recorded in `GOV-015` (professional-review tracker).
- This document is an *issue-spotting tool*. It does not contain legal advice and must not be treated as a substitute for counsel.
- Record the reviewer, the date, and the scope reviewed. A review with no recorded scope does not clear the gate.

## Dependencies

**Upstream — this cannot be completed without:**

- `CON-019` — Final-completion coordination checklist


**Stage gates this is required evidence for:** `SG-12`

## Typst issue version expected?

**No.** This artifact stays in Markdown. If it ever becomes an external submission, a stage-gate package, or a controlled-distribution PDF, update `typst_issue_required` in `artifact-register.csv` first — the register is the source of truth, not the file.
