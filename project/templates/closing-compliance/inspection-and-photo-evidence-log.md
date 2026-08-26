---
artifact_id: CLO-014
artifact_type: log
title: Inspection and photo evidence log
workstream: closing-compliance
service_code: INS
status: template
template_version: "1.0"
parcel_ids: []
owner_role: contractor_program_manager
decision_role: company_decision_authority
required_reviewer_role: internal_peer
legal_review_required: false
typst_issue_required: false
typst_source: null
latest_issue_id: null
created_at: 2026-08-26
updated_at: 2026-08-26
source_as_of: 2026-08-26
source_ids: [SRC-007]
depends_on: [CON-019]
supersedes: null
confidentiality: internal
---

# Inspection and photo evidence log

`CLO-014` · closing-compliance · service code `INS`

> **Parcel-specific.** Create one copy per candidate parcel under `working/candidate-parcels/<parcel-id>/`. Do not complete this template in place.

## Purpose

Log of inspections and photographic evidence supporting compliance.

## When to use it

Through the compliance period.

## Required inputs

- Compliance requirements
- Dated photographs

## Instructions

- Photographs must be dated and identifiable to the parcel. Undated evidence is not evidence.
- Where the applicable regime specifies a cadence and format, follow it exactly — `SRC-007` shows the DLBA rejects videos and written descriptions for structure sales.
- This is compliance evidence, not construction observation. ICA §7.3 stands.
- An unchecked condition is `not_found` or `blocked` — never `verified`, never blank.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Evidence dated and parcel-identified
- Cadence and format match the applicable requirement
- No construction-evaluation commentary added

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Sources

Requirements in this artifact trace to the following rows in `source-register.csv`. Re-verify before relying on any of them — agency requirements change without notice.

| Source | Document | Status | Pinpoint |
| --- | --- | --- | --- |
| `SRC-007` | Compliance | `verified` | Post-sale timeline table (15/45/60 day milestones); evidence rules; Release of Interest |

## Unresolved questions

_None recorded. Add any question that would change a decision if answered differently._

## Approvals and professional review

- **Required reviewer: `internal_peer`.** No licensed professional is required for this artifact.
- The Company still decides; the Contractor recommends (ICA §1.3).

## Dependencies

**Upstream — this cannot be completed without:**

- `CON-019` — Final-completion coordination checklist


## Typst issue version expected?

**No.** This artifact stays in Markdown. If it ever becomes an external submission, a stage-gate package, or a controlled-distribution PDF, update `typst_issue_required` in `artifact-register.csv` first — the register is the source of truth, not the file.
