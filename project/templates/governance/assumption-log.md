---
artifact_id: GOV-008
artifact_type: log
title: Assumption log
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

# Assumption log

`GOV-008` · governance · service code `ADM`

> **Reusable.** One copy project-wide, under `working/project-wide/`.

## Purpose

Tracks every assumption load-bearing enough that being wrong about it would change a decision — with the test that would confirm or refute it.

## When to use it

Whenever an estimate, schedule, or recommendation rests on something not yet verified.

## Required inputs

- The artifact making the assumption
- The condition that would resolve it

## Instructions

- Every assumption names an owner and a resolving test. An assumption with no test is a guess.
- Assumptions that survive to a gate must be visible in that gate's package.
- When an assumption is resolved, record the outcome and update dependent artifacts — do not delete the row.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Every open assumption has an owner and a resolving test
- No assumption feeding a passed gate is still open without a recorded waiver

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Unresolved questions

- Which assumptions must be resolved before diligence spend is authorised?

## Approvals and professional review

- **Required reviewer: `internal_peer`.** No licensed professional is required for this artifact.
- The Company still decides; the Contractor recommends (ICA §1.3).

## Dependencies

**Upstream — this cannot be completed without:**

- `GOV-002` — Artifact lifecycle and publication rules


## Typst issue version expected?

**No.** This artifact stays in Markdown. If it ever becomes an external submission, a stage-gate package, or a controlled-distribution PDF, update `typst_issue_required` in `artifact-register.csv` first — the register is the source of truth, not the file.
