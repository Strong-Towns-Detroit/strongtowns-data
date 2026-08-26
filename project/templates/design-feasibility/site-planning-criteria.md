---
artifact_id: DSN-003
artifact_type: criteria
title: Site-planning criteria
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
source_as_of: null
source_ids: []
depends_on: [SCR-003]
supersedes: null
confidentiality: internal
---

# Site-planning criteria

`DSN-003` · design-feasibility · service code `DSN`

> **Reusable.** One copy project-wide, under `working/project-wide/`.

## Purpose

Site planning criteria: orientation, setbacks, parking, access, drainage, outdoor space.

## When to use it

Alongside concept design.

## Required inputs

- `SCR-006` envelope
- Zoning dimensional standards `DD-011`
- Survey `DD-007`

## Instructions

- Derive setbacks from the ordinance section, not a summary table.
- Drainage is a design constraint on infill lots with unknown fill. Coordinate with `DD-016`.
- Conclusions reserved to a licensed discipline come from that professional, not from this artifact.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Criteria traced to ordinance sections
- Access and drainage addressed
- Consistent with the surveyed envelope

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

- `SCR-003` — Owner's project requirements brief


## Typst issue version expected?

**No.** This artifact stays in Markdown. If it ever becomes an external submission, a stage-gate package, or a controlled-distribution PDF, update `typst_issue_required` in `artifact-register.csv` first — the register is the source of truth, not the file.
