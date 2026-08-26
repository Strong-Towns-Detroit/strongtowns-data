---
artifact_id: SCR-005
artifact_type: register
title: Candidate pipeline record
workstream: parcel-screening
service_code: LND
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
depends_on: [SCR-001]
supersedes: null
confidentiality: internal
---

# Candidate pipeline record

`SCR-005` · parcel-screening · service code `LND`

> **Reusable.** One copy project-wide, under `working/project-wide/`.

## Purpose

The pipeline record of candidates, status, and disposition required by ICA Exhibit A. It is the answer to 'what have you looked at, and what happened to it'.

## When to use it

Continuously, from first identification through acquisition or rejection.

## Required inputs

- `SCR-001` dossiers
- `SCR-002` recommendations
- Company decisions

## Instructions

- Every parcel that was seriously considered gets a row, including rejected ones. A pipeline that only shows live candidates cannot answer the question it exists to answer.
- Record disposition and the reason. 'Passed' is not a disposition; 'passed — buildable width below program minimum' is.
- Record the date a parcel was *presented to the Company*. ICA §4.3 runs a twelve-month restriction from presentation, and `GOV-022` needs that date.
- Keep this current enough to drop into the weekly status report without rework.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Every considered parcel has a row with a status and a disposition reason
- Presentation dates recorded for §4.3 tracking
- Live candidates are distinguishable from closed ones at a glance

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Unresolved questions

_None recorded. Add any question that would change a decision if answered differently._

## Approvals and professional review

- **Required reviewer: `internal_peer`.** No licensed professional is required for this artifact.
- The Company still decides; the Contractor recommends (ICA §1.3).

## Dependencies

**Upstream — this cannot be completed without:**

- `SCR-001` — Candidate-parcel dossier


## Typst issue version expected?

**No.** This artifact stays in Markdown. If it ever becomes an external submission, a stage-gate package, or a controlled-distribution PDF, update `typst_issue_required` in `artifact-register.csv` first — the register is the source of truth, not the file.
