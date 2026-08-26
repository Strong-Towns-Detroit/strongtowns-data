---
artifact_id: DSN-001
artifact_type: brief
title: Owner's project requirements
workstream: design-feasibility
service_code: DSN
status: template
template_version: "1.0"
parcel_ids: []
owner_role: contractor_program_manager
decision_role: company_decision_authority
required_reviewer_role: company_decision_authority
legal_review_required: false
typst_issue_required: true
typst_source: publication/typst/templates/report.typ
latest_issue_id: null
created_at: 2026-08-26
updated_at: 2026-08-26
source_as_of: null
source_ids: []
depends_on: [SCR-003]
supersedes: null
confidentiality: internal
---

# Owner's project requirements

`DSN-001` · design-feasibility · service code `DSN`

> **Reusable.** One copy project-wide, under `working/project-wide/`.

## Purpose

The owner's project requirements in design terms — the brief the drawings answer to. ICA §6 measures the standard of care partly against Company's written program, so this must exist in writing.

## When to use it

Before concept design begins; re-baselined on any Company-directed change.

## Required inputs

- `SCR-003` owner's project requirements brief
- Company's stated priorities
- Budget envelope

## Instructions

- Restate the program as design criteria, not aspirations. 'Family-friendly' is not a requirement; a stated bedroom count and separation is.
- Mark each requirement fixed or negotiable. A brief with no priorities cannot resolve a trade-off.
- Version it. Changes after design begins are Company-directed scope changes, billable under ICA §6, and provable only from version history.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Every requirement decidable from the drawings
- Fixed and negotiable separated
- Company agreement recorded in writing
- Version history intact

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


**Stage gates this is required evidence for:** `SG-01`

## Typst issue version expected?

**Yes.** A paired Typst issue document is expected before this leaves the project. Base template: `publication/typst/templates/report.typ`.

Transfer reviewed content to the `.typ` deliberately — there is no automatic Markdown→Typst conversion. The Markdown draft and the Typst issue share this `artifact_id`; the Typst metadata records the draft path and its SHA-256.

Compilation is not approval. See `publication/README.md` for the issue gate.
