---
artifact_id: DSN-012
artifact_type: register
title: Design deliverables register
workstream: design-feasibility
service_code: DSN
status: template
template_version: "1.0"
parcel_ids: []
owner_role: contractor_program_manager
decision_role: company_decision_authority
required_reviewer_role: company_decision_authority
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

# Design deliverables register

`DSN-012` · design-feasibility · service code `DSN`

> **Parcel-specific.** Create one copy per candidate parcel under `working/candidate-parcels/<parcel-id>/`. Do not complete this template in place.

## Purpose

Register of design deliverables: what will be produced, in what format, by whom, when.

## When to use it

At design start.

## Required inputs

- `DSN-006` consultant scope matrix
- `SRC-017` submittal requirements

## Instructions

- `SRC-017` requires three complete plan sets drawn to scale, one set of calculations, and one set of specifications. Plan the deliverable list around what will actually be submitted.
- ICA §5.4 requires delivery in native editable format on request and at end of Term — record the native format for each deliverable, not just the PDF.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Every deliverable has an owner, format, and date
- Native formats recorded for `GOV-023`
- Submittal set composition matches `SRC-017`

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Sources

Requirements in this artifact trace to the following rows in `source-register.csv`. Re-verify before relying on any of them — agency requirements change without notice.

| Source | Document | Status | Pinpoint |
| --- | --- | --- | --- |
| `SRC-017` | Residential Building Permit/Plan Submittal Checklist | `verified` | Preamble (submittal quantities, sealed-drawing statement, fee deposit); Plot Plan; Foundation Plans; Floor Plans; Elevations; Framing Plans; Electrical; Mechanical; Details and General Notes |

## Unresolved questions

_None recorded. Add any question that would change a decision if answered differently._

## Approvals and professional review

- **Required reviewer: `company_decision_authority`.** Record the review in `GOV-015` before this artifact is relied on at a gate.
- Conclusions reserved to that discipline must come from that professional, not from this document.

## Dependencies

**Upstream — this cannot be completed without:**

- `SCR-003` — Owner's project requirements brief

**Downstream — these depend on this:**

- `PRO-001` — Architect and consultant RFP
- `PRO-002` — Builder and general-contractor RFP
- `PRO-003` — Bid instructions
- `PRO-004` — Bidder question log
- `PRO-005` — Bid-leveling schema
- `PRO-006` — Scope-gap matrix
- `PRO-007` — Contractor qualification checklist
- `PRO-008` — Contract commercial-terms checklist
- `PRO-009` — Professional agreement review handoff
- `PRO-010` — Bid comparison record

**Stage gates this is required evidence for:** `SG-06`

## Typst issue version expected?

**No.** This artifact stays in Markdown. If it ever becomes an external submission, a stage-gate package, or a controlled-distribution PDF, update `typst_issue_required` in `artifact-register.csv` first — the register is the source of truth, not the file.
