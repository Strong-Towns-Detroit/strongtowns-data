---
artifact_id: GOV-012
artifact_type: template
title: Meeting-note template
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

# Meeting-note template

`GOV-012` · governance · service code `ADM`

> **Reusable.** One copy project-wide, under `working/project-wide/`.

## Purpose

A consistent shape for meeting notes so that decisions, actions, and open questions can be extracted mechanically rather than re-read.

## When to use it

Any meeting whose outcome affects budget, schedule, scope, or a decision.

## Required inputs

- Attendee list
- Agenda
- Prior open items

## Instructions

- Separate three things explicitly: decisions made, actions assigned, questions left open.
- Route decisions to `GOV-007`, actions to `GOV-010`, questions to the relevant artifact.
- Record any spending authorization given verbally or by email — ICA §3.2 permits authorization at the weekly meeting, and that authorization needs a record.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Decisions, actions, and open questions are separated
- Any authorization granted in the meeting is recorded in `GOV-021`

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Unresolved questions

_None recorded. Add any question that would change a decision if answered differently._

## Approvals and professional review

- **Required reviewer: `internal_peer`.** No licensed professional is required for this artifact.
- The Company still decides; the Contractor recommends (ICA §1.3).

## Dependencies

**Upstream:** none. This is an entry point.

**Downstream — these depend on this:**

- `GOV-024` — Weekly coordination meeting agenda and minutes

## Typst issue version expected?

**No.** This artifact stays in Markdown. If it ever becomes an external submission, a stage-gate package, or a controlled-distribution PDF, update `typst_issue_required` in `artifact-register.csv` first — the register is the source of truth, not the file.
