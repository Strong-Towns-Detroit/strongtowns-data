---
artifact_id: DSN-002
artifact_type: schedule
title: Room and program schedule
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
source_as_of: null
source_ids: []
depends_on: [SCR-003]
supersedes: null
confidentiality: internal
---

# Room and program schedule

`DSN-002` · design-feasibility · service code `DSN`

> **Reusable.** One copy project-wide, under `working/project-wide/`.

## Purpose

Room and space schedule with areas and adjacencies — the quantitative core of the program.

## When to use it

Once `DSN-001` is agreed.

## Required inputs

- `DSN-001`
- Target gross area from the cost plan

## Instructions

- Schedule net areas and state the assumed gross-to-net factor separately. Conflating them hides cost.
- Check the total against `SCR-006` buildable envelope before drawing anything.
- Every figure states its basis (quote, estimate, published figure, placeholder) and a confidence. A placeholder that looks like an estimate is how a cost plan misleads.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Every space has an area and an adjacency
- Gross-to-net factor stated
- Total reconciles to the envelope and the cost plan

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Sources

_No external requirements cited. If this artifact starts asserting one, add a row to `source-register.csv` first._

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
