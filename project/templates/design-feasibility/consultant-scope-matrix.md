---
artifact_id: DSN-006
artifact_type: matrix
title: Consultant scope matrix
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

# Consultant scope matrix

`DSN-006` · design-feasibility · service code `DSN`

> **Reusable.** One copy project-wide, under `working/project-wide/`.

## Purpose

Matrix of which consultant is responsible for which scope, and where the gaps are.

## When to use it

Before engaging any consultant.

## Required inputs

- `DSN-014` sealed-drawing triggers
- Program scope

## Instructions

- Map every deliverable to exactly one responsible party. Scope gaps between consultants are the most common source of unbudgeted change.
- ICA Exhibit A requires the Contractor to identify elements needing a sealed drawing and coordinate with the professional the Company retains — this matrix is where that identification lands.
- Record who the Company has retained versus who still must be engaged.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Every deliverable assigned to one party
- Gaps identified explicitly
- Retained versus to-be-engaged distinguished

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


## Typst issue version expected?

**No.** This artifact stays in Markdown. If it ever becomes an external submission, a stage-gate package, or a controlled-distribution PDF, update `typst_issue_required` in `artifact-register.csv` first — the register is the source of truth, not the file.
