---
artifact_id: GOV-007
artifact_type: log
title: Decision log
workstream: governance
service_code: ADM
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
depends_on: [GOV-002]
supersedes: null
confidentiality: internal
---

# Decision log

`GOV-007` · governance · service code `ADM`

> **Reusable.** One copy project-wide, under `working/project-wide/`.

## Purpose

Records decisions that would otherwise be reconstructed from memory: what was decided, by whom, on what basis, and what was rejected.

## When to use it

Whenever a choice forecloses an option — parcel selection, design direction, pathway, procurement, or scope.

## Required inputs

- The options considered
- The evidence available at the time
- The decider

## Instructions

- Record the decision *and* the alternatives rejected. The rejected options are the valuable part.
- Record what was known at the time, not what is known now. A decision log is not corrected retroactively; it is superseded by a new entry.
- Under ICA §1.3 the Contractor recommends and the Company decides — record both roles separately.
- Where the Company directs a decision over the Contractor's written objection, record the objection. ICA §8.2 turns on it.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Every entry names a decider, a date, and a basis
- Rejected alternatives are recorded
- Any Company direction over written objection is captured verbatim

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Unresolved questions

_None recorded. Add any question that would change a decision if answered differently._

## Approvals and professional review

- **Required reviewer: `company_decision_authority`.** Record the review in `GOV-015` before this artifact is relied on at a gate.
- Conclusions reserved to that discipline must come from that professional, not from this document.

## Dependencies

**Upstream — this cannot be completed without:**

- `GOV-002` — Artifact lifecycle and publication rules


## Typst issue version expected?

**No.** This artifact stays in Markdown. If it ever becomes an external submission, a stage-gate package, or a controlled-distribution PDF, update `typst_issue_required` in `artifact-register.csv` first — the register is the source of truth, not the file.
