---
artifact_id: GOV-024
artifact_type: template
title: Weekly coordination meeting agenda and minutes
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
depends_on: [GOV-012]
supersedes: null
confidentiality: internal
---

# Weekly coordination meeting agenda and minutes

`GOV-024` · governance · service code `ADM`

> **Reusable.** One copy project-wide, under `working/project-wide/`.

## Purpose

Agenda and minutes for the weekly coordination meeting required by ICA §1.3 — the forum where scope, budget, schedule, and program requirements are conferred on, and where §3.2 spending authorizations are commonly given.

## When to use it

Weekly, alongside the status report.

## Required inputs

- `GOV-017` weekly status report
- `GOV-010` open actions
- Items awaiting Company decision

## Instructions

- Run the agenda from the status report's headings so nothing contractual is skipped.
- Put items awaiting Company decision first — they are the reason the meeting exists.
- Record any spending authorization given, and copy it to `GOV-021` the same day.
- Record any Company direction that the Contractor objected to, in the Contractor's own words, and copy to `GOV-007`.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Decisions, authorizations, and actions recorded and routed
- Every item awaiting decision either decided or re-dated with a reason

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Unresolved questions

_None recorded. Add any question that would change a decision if answered differently._

## Approvals and professional review

- **Required reviewer: `internal_peer`.** No licensed professional is required for this artifact.
- The Company still decides; the Contractor recommends (ICA §1.3).

## Dependencies

**Upstream — this cannot be completed without:**

- `GOV-012` — Meeting-note template


## Typst issue version expected?

**No.** This artifact stays in Markdown. If it ever becomes an external submission, a stage-gate package, or a controlled-distribution PDF, update `typst_issue_required` in `artifact-register.csv` first — the register is the source of truth, not the file.
