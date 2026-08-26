---
artifact_id: DSN-011
artifact_type: log
title: Design decision log
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

# Design decision log

`DSN-011` · design-feasibility · service code `DSN`

> **Parcel-specific.** Create one copy per candidate parcel under `working/candidate-parcels/<parcel-id>/`. Do not complete this template in place.

## Purpose

Design decision log: what was decided, what was rejected, and on whose direction.

## When to use it

Continuously through design.

## Required inputs

- Design reviews
- Company direction

## Instructions

- Record Company-directed decisions separately from Contractor recommendations — ICA §1.3 and §8.2 both turn on the distinction.
- Where the Company directs a design decision over the Contractor's written objection, record the objection verbatim. ICA §8.2 indemnity depends on it existing.
- Copy material decisions to `GOV-007`.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Every decision names a decider and a date
- Rejected alternatives recorded
- Written objections captured verbatim

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
