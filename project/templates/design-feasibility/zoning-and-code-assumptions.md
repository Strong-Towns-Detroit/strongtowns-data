---
artifact_id: DSN-008
artifact_type: assumptions
title: Zoning and code assumptions
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
source_ids: [SRC-015, SRC-017]
depends_on: [SCR-003]
supersedes: null
confidentiality: internal
---

# Zoning and code assumptions

`DSN-008` · design-feasibility · service code `DSN`

> **Parcel-specific.** Create one copy per candidate parcel under `working/candidate-parcels/<parcel-id>/`. Do not complete this template in place.

## Purpose

The zoning and code assumptions the design rests on, each with the test that would confirm it.

## When to use it

As soon as design begins.

## Required inputs

- `DD-010` zoning confirmation
- `DD-011` dimensional matrix
- `SRC-015` codes enforced

## Instructions

- Every assumption gets an owner and a resolving test, and a copy in `GOV-008`.
- `SRC-017` states design must meet codes in effect at time of plan submittal — a long design period can move the target. Record the assumed edition and the submittal date it depends on.
- The current adopted code editions were not established from the BSEED pages. Treat the edition as an assumption until confirmed.
- An unchecked condition is `not_found` or `blocked` — never `verified`, never blank.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Every assumption has an owner and a test
- Assumed code edition stated explicitly
- Copied to `GOV-008`

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Sources

Requirements in this artifact trace to the following rows in `source-register.csv`. Re-verify before relying on any of them — agency requirements change without notice.

| Source | Document | Status | Pinpoint |
| --- | --- | --- | --- |
| `SRC-015` | BSEED Plan Review | `verified` | Codes enforced; ePlans/eLAPS process steps; coordinating departments |
| `SRC-017` | Residential Building Permit/Plan Submittal Checklist | `verified` | Preamble (submittal quantities, sealed-drawing statement, fee deposit); Plot Plan; Foundation Plans; Floor Plans; Elevations; Framing Plans; Electrical; Mechanical; Details and General Notes |

## Unresolved questions

- Which editions of the Michigan Residential Code and related codes has Detroit currently adopted? Not published on `SRC-015` or `SRC-016`.

## Approvals and professional review

- **Required reviewer: `licensed_architect_or_engineer`.** Record the review in `GOV-015` before this artifact is relied on at a gate.
- Conclusions reserved to that discipline must come from that professional, not from this document.

## Dependencies

**Upstream — this cannot be completed without:**

- `SCR-003` — Owner's project requirements brief


## Typst issue version expected?

**No.** This artifact stays in Markdown. If it ever becomes an external submission, a stage-gate package, or a controlled-distribution PDF, update `typst_issue_required` in `artifact-register.csv` first — the register is the source of truth, not the file.
