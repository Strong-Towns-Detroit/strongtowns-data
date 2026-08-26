---
artifact_id: DSN-005
artifact_type: criteria
title: Sustainability and energy goals
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

# Sustainability and energy goals

`DSN-005` · design-feasibility · service code `DSN`

> **Reusable.** One copy project-wide, under `working/project-wide/`.

## Purpose

Sustainability and energy goals, and the compliance path chosen to demonstrate them.

## When to use it

With the program, before mechanical design.

## Required inputs

- `DSN-001`
- Michigan energy code requirements

## Instructions

- `SRC-017` requires a State of Michigan Energy Code Compliance worksheet for new construction. Decide the compliance path early — it constrains envelope and mechanical selection.
- Distinguish code compliance from elective performance targets.
- Conclusions reserved to a licensed discipline come from that professional, not from this artifact.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Compliance path chosen and recorded
- Energy Code Compliance worksheet path identified
- Elective targets priced separately

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

- **Required reviewer: `licensed_architect_or_engineer`.** Record the review in `GOV-015` before this artifact is relied on at a gate.
- Conclusions reserved to that discipline must come from that professional, not from this document.

## Dependencies

**Upstream — this cannot be completed without:**

- `SCR-003` — Owner's project requirements brief


## Typst issue version expected?

**No.** This artifact stays in Markdown. If it ever becomes an external submission, a stage-gate package, or a controlled-distribution PDF, update `typst_issue_required` in `artifact-register.csv` first — the register is the source of truth, not the file.
