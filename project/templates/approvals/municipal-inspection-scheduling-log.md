---
artifact_id: APR-009
artifact_type: log
title: Municipal inspection scheduling log
workstream: approvals
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
source_ids: [SRC-016, SRC-019]
depends_on: [APR-001]
supersedes: null
confidentiality: internal
---

# Municipal inspection scheduling log

`APR-009` · approvals · service code `INS`

> **Parcel-specific.** Create one copy per candidate parcel under `working/candidate-parcels/<parcel-id>/`. Do not complete this template in place.

## Purpose

Log for scheduling municipal inspections. ICA Exhibit A assigns the Contractor scheduling inspections in coordination with the Company's construction schedule.

## When to use it

Through construction.

## Required inputs

- `CON-003` schedule
- `SRC-019` eLAPS
- Construction Inspection division requirements

## Instructions

- This is scheduling and coordination, not inspection. ICA §7.3 states the Contractor does not inspect construction. Book the municipal inspector; do not inspect the work.
- `SRC-016` lists Construction Inspection covering boilers, buildings, electrical, elevators, mechanical and plumbing — each trade is a separate inspection with its own sequence position.
- Coordinate with the Company's builder for readiness. A failed inspection because the work was not ready is a schedule loss and a fee.
- An unchecked condition is `not_found` or `blocked` — never `verified`, never blank.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Every required inspection identified by trade and sequence position
- Bookings coordinated with the Company's construction schedule
- The scheduling-versus-inspecting boundary respected

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Sources

Requirements in this artifact trace to the following rows in `source-register.csv`. Re-verify before relying on any of them — agency requirements change without notice.

| Source | Document | Status | Pinpoint |
| --- | --- | --- | --- |
| `SRC-016` | Buildings, Safety Engineering and Environmental Department (divisions index) | `verified` | Division list and responsibilities |
| `SRC-019` | Accela Citizen Access / eLAPS permit portal | `listed_not_retrieved` | — |

## Unresolved questions

_None recorded. Add any question that would change a decision if answered differently._

## Approvals and professional review

- **Required reviewer: `internal_peer`.** No licensed professional is required for this artifact.
- The Company still decides; the Contractor recommends (ICA §1.3).

## Dependencies

**Upstream — this cannot be completed without:**

- `APR-001` — Permit and approval matrix


## Typst issue version expected?

**No.** This artifact stays in Markdown. If it ever becomes an external submission, a stage-gate package, or a controlled-distribution PDF, update `typst_issue_required` in `artifact-register.csv` first — the register is the source of truth, not the file.
