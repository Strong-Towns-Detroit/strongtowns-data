---
artifact_id: GOV-010
artifact_type: register
title: Action-item register
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
depends_on: [GOV-002]
supersedes: null
confidentiality: internal
---

# Action-item register

`GOV-010` · governance · service code `ADM`

> **Reusable.** One copy project-wide, under `working/project-wide/`.

## Purpose

Tracks commitments made in meetings and correspondence so they do not evaporate between weekly cycles.

## When to use it

Populated from `GOV-024` (meeting minutes) and `GOV-013` (correspondence log).

## Required inputs

- Meeting minutes
- Correspondence
- Open items from the prior weekly report

## Instructions

- One owner, one due date, one verifiable done-condition per item.
- Items awaiting a Company decision are flagged separately — ICA §1.2 requires them in the weekly report.

## Completion criteria

This artifact is complete when **all** of the following hold:

- No item lacks an owner or a due date
- Items awaiting Company decision are distinguishable at a glance

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Unresolved questions

_None recorded. Add any question that would change a decision if answered differently._

## Approvals and professional review

- **Required reviewer: `internal_peer`.** No licensed professional is required for this artifact.
- The Company still decides; the Contractor recommends (ICA §1.3).

## Dependencies

**Upstream — this cannot be completed without:**

- `GOV-002` — Artifact lifecycle and publication rules


## Typst issue version expected?

**No.** This artifact stays in Markdown. If it ever becomes an external submission, a stage-gate package, or a controlled-distribution PDF, update `typst_issue_required` in `artifact-register.csv` first — the register is the source of truth, not the file.
