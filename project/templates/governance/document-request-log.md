---
artifact_id: GOV-014
artifact_type: log
title: Document-request log
workstream: governance
service_code: ADM
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
depends_on: []
supersedes: null
confidentiality: internal
---

# Document-request log

`GOV-014` · governance · service code `ADM`

> **Reusable.** One copy project-wide, under `working/project-wide/`.

## Purpose

Tracks documents requested from third parties — title, survey, environmental, geotechnical, utility, agency — with request date, expected date, and receipt.

## When to use it

Whenever the project depends on someone else producing a document.

## Required inputs

- Due-diligence plan
- Consultant scopes

## Instructions

- Record the request date and the promised date separately. The gap is the schedule risk.
- An overdue request is an issue in `GOV-009`, not a note in this log.
- Mark the dependent condition `blocked` — never `not_found` — while a request is outstanding.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Every outstanding request has a promised date and a chase date
- Every received document is filed and linked

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Unresolved questions

_None recorded. Add any question that would change a decision if answered differently._

## Approvals and professional review

- **Required reviewer: `internal_peer`.** No licensed professional is required for this artifact.
- The Company still decides; the Contractor recommends (ICA §1.3).

## Dependencies

**Upstream:** none. This is an entry point.


## Typst issue version expected?

**No.** This artifact stays in Markdown. If it ever becomes an external submission, a stage-gate package, or a controlled-distribution PDF, update `typst_issue_required` in `artifact-register.csv` first — the register is the source of truth, not the file.
