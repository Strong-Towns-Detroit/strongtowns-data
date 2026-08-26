---
artifact_id: GOV-015
artifact_type: tracker
title: Professional-review tracker
workstream: governance
service_code: ADM
status: template
template_version: "1.0"
parcel_ids: []
owner_role: contractor_program_manager
decision_role: company_decision_authority
required_reviewer_role: company_decision_authority
legal_review_required: true
typst_issue_required: false
typst_source: null
latest_issue_id: null
created_at: 2026-08-26
updated_at: 2026-08-26
source_as_of: null
source_ids: []
depends_on: [GOV-003]
supersedes: null
confidentiality: internal
---

# Professional-review tracker

`GOV-015` · governance · service code `ADM`

> **Reusable.** One copy project-wide, under `working/project-wide/`.

## Purpose

Enforces the reviewer named on every artifact where `legal_review_required` is true or a licensed discipline is named. This is the control that keeps professional-review requirements from being silently skipped.

## When to use it

Whenever an artifact requiring professional review approaches a gate.

## Required inputs

- `artifact-register.csv` reviewer columns
- Professional engagement records

## Instructions

- Record reviewer, discipline, licence identifier, date, and the *scope reviewed*. A review with no recorded scope does not clear a gate.
- A review is scoped to a version. If the artifact changes materially, the review is stale.
- Track the handoff package (`professional-handoff` class) that was actually sent, so the reviewer's answer can be read against the question asked.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Every artifact with `legal_review_required: true` feeding a passed gate has a recorded review
- No recorded review is missing its scope or its version reference

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Unresolved questions

- Which professionals has the Company already retained, and which must still be engaged?

## Approvals and professional review

- **Required reviewer: `company_decision_authority`.** `legal_review_required: true` — every stage gate this artifact feeds is blocked until that review is recorded in `GOV-015` (professional-review tracker).
- This document is an *issue-spotting tool*. It does not contain legal advice and must not be treated as a substitute for counsel.
- Record the reviewer, the date, and the scope reviewed. A review with no recorded scope does not clear the gate.

## Dependencies

**Upstream — this cannot be completed without:**

- `GOV-003` — Master artifact register


## Typst issue version expected?

**No.** This artifact stays in Markdown. If it ever becomes an external submission, a stage-gate package, or a controlled-distribution PDF, update `typst_issue_required` in `artifact-register.csv` first — the register is the source of truth, not the file.
