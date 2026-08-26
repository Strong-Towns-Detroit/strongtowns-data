---
artifact_id: DSN-014
artifact_type: register
title: Sealed-drawing trigger register
workstream: design-feasibility
service_code: DSN
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
source_as_of: 2026-08-26
source_ids: [SRC-017]
depends_on: [SCR-003]
supersedes: null
confidentiality: internal
---

# Sealed-drawing trigger register

`DSN-014` · design-feasibility · service code `DSN`

> **Parcel-specific.** Create one copy per candidate parcel under `working/candidate-parcels/<parcel-id>/`. Do not complete this template in place.

## Purpose

Register of elements requiring a sealed architectural or engineering drawing. ICA Exhibit A makes identifying these a Contractor deliverable.

## When to use it

As soon as the structural and envelope concept is known — a late-discovered seal requirement is a schedule event.

## Required inputs

- `SRC-017` submittal checklist
- Concept structural approach
- `DSN-006` consultant scope matrix

## Instructions

- `SRC-017` states the project may have to be designed by Michigan-licensed professional engineers and architects, with drawings prepared under their supervision and signed and sealed by them.
- Two concrete triggers appear in the checklist itself: truss calculations must be signed and sealed by a Michigan-licensed architect or engineer; masonry and concrete basement walls require an engineered design.
- Identify the trigger; do not attempt the sealed work. The Contractor coordinates with the professional the Company retains.
- Every trigger becomes a line in `DSN-006` and a cost in `FIN-003`.
- Conclusions reserved to a licensed discipline come from that professional, not from this artifact.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Every sealed-drawing trigger identified and routed to a retained professional
- Truss and foundation triggers specifically addressed
- Cost and schedule impact reflected in `FIN-003` and `CON-003`

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Sources

Requirements in this artifact trace to the following rows in `source-register.csv`. Re-verify before relying on any of them — agency requirements change without notice.

| Source | Document | Status | Pinpoint |
| --- | --- | --- | --- |
| `SRC-017` | Residential Building Permit/Plan Submittal Checklist | `verified` | Preamble (submittal quantities, sealed-drawing statement, fee deposit); Plot Plan; Foundation Plans; Floor Plans; Elevations; Framing Plans; Electrical; Mechanical; Details and General Notes |

## Unresolved questions

- Which additional elements trigger a seal under the CURRENT code edition, as distinct from the 2013 checklist?

## Approvals and professional review

- **Required reviewer: `licensed_architect_or_engineer`.** Record the review in `GOV-015` before this artifact is relied on at a gate.
- Conclusions reserved to that discipline must come from that professional, not from this document.

## Dependencies

**Upstream — this cannot be completed without:**

- `SCR-003` — Owner's project requirements brief


**Stage gates this is required evidence for:** `SG-06`

## Typst issue version expected?

**No.** This artifact stays in Markdown. If it ever becomes an external submission, a stage-gate package, or a controlled-distribution PDF, update `typst_issue_required` in `artifact-register.csv` first — the register is the source of truth, not the file.
