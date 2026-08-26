---
artifact_id: DD-013
artifact_type: screen
title: Historic and design-review screen
workstream: due-diligence
service_code: PMT
status: template
template_version: "1.0"
parcel_ids: []
owner_role: contractor_program_manager
decision_role: company_decision_authority
required_reviewer_role: licensed_architect_or_engineer
legal_review_required: false
typst_issue_required: false
typst_source: null
latest_issue_id: null
created_at: 2026-08-26
updated_at: 2026-08-26
source_as_of: null
source_ids: []
depends_on: [DD-001]
supersedes: null
confidentiality: internal
---

# Historic and design-review screen

`DD-013` · due-diligence · service code `PMT`

> **Parcel-specific.** Create one copy per candidate parcel under `working/candidate-parcels/<parcel-id>/`. Do not complete this template in place.

## Purpose

Screens for historic district, design review, or other overlay requirements that add an approval step.

## When to use it

Early — an overlay changes the schedule, not just the design.

## Required inputs

- Parcel dossier `SCR-001`
- `DD-001` deadline calendar
- Relevant third-party product

## Instructions

- Absence of a listing is not confirmation of absence. Confirm with the authority.
- Any conclusion reserved to a licensed discipline comes from that professional, not from this artifact.
- A condition not yet checked is recorded `not_found` or `blocked` — never `verified`, never blank.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Findings traced to a primary source or a named professional
- Envelope, cost or schedule consequences stated
- Unresolved conditions marked `blocked` with an owner

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Sources

_No external requirements cited. If this artifact starts asserting one, add a row to `source-register.csv` first._

## Unresolved questions

_None recorded. Add any question that would change a decision if answered differently._

## Approvals and professional review

- **Required reviewer: `licensed_architect_or_engineer`.** Record the review in `GOV-015` before this artifact is relied on at a gate.
- Conclusions reserved to that discipline must come from that professional, not from this document.

## Dependencies

**Upstream — this cannot be completed without:**

- `DD-001` — Due-diligence plan and deadline calculator


## Typst issue version expected?

**No.** This artifact stays in Markdown. If it ever becomes an external submission, a stage-gate package, or a controlled-distribution PDF, update `typst_issue_required` in `artifact-register.csv` first — the register is the source of truth, not the file.
