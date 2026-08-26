---
artifact_id: DSN-013
artifact_type: log
title: Plan version control and revision issue log
workstream: design-feasibility
service_code: DSN
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
source_as_of: null
source_ids: []
depends_on: [SCR-003]
supersedes: null
confidentiality: internal
---

# Plan version control and revision issue log

`DSN-013` · design-feasibility · service code `DSN`

> **Parcel-specific.** Create one copy per candidate parcel under `working/candidate-parcels/<parcel-id>/`. Do not complete this template in place.

## Purpose

Plan version control and revision issue log. ICA Exhibit A assigns the Contractor plan version control and revision issue.

## When to use it

From first issue onward.

## Required inputs

- Issued drawing sets

## Instructions

- Every issued set gets a version, a date, and a reason for issue. A drawing on site with no version is a defect waiting to be argued about.
- Record who received each issue. ICA §5.5 ends Contractor responsibility for post-delivery modification — that boundary is provable only from a clean issue record.
- Revisions required to obtain permit approval are corrected at no additional charge under ICA §6; revisions from Company-directed scope change are billable. Code the reason for every revision accordingly.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Every issue versioned, dated and reason-coded
- Recipients recorded
- Revision reasons coded to the ICA §6 distinction

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Sources

_No external requirements cited. If this artifact starts asserting one, add a row to `source-register.csv` first._

## Unresolved questions

_None recorded. Add any question that would change a decision if answered differently._

## Approvals and professional review

- **Required reviewer: `internal_peer`.** No licensed professional is required for this artifact.
- The Company still decides; the Contractor recommends (ICA §1.3).

## Dependencies

**Upstream — this cannot be completed without:**

- `SCR-003` — Owner's project requirements brief


## Typst issue version expected?

**No.** This artifact stays in Markdown. If it ever becomes an external submission, a stage-gate package, or a controlled-distribution PDF, update `typst_issue_required` in `artifact-register.csv` first — the register is the source of truth, not the file.
