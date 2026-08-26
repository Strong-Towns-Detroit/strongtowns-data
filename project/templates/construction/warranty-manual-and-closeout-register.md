---
artifact_id: CON-020
artifact_type: register
title: Warranty, manual and closeout register
workstream: construction
service_code: INS
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
depends_on: [CON-003]
supersedes: null
confidentiality: internal
---

# Warranty, manual and closeout register

`CON-020` · construction · service code `INS`

> **Parcel-specific.** Create one copy per candidate parcel under `working/candidate-parcels/<parcel-id>/`. Do not complete this template in place.

## Purpose

Register of warranties, manuals and closeout documentation.

## When to use it

Assembled through construction, closed at completion.

## Required inputs

- Warranty documents
- O&M manuals
- As-built information

## Instructions

- Warranties are produced by the Company's builder and suppliers. The Contractor registers and indexes them; ICA §7.4 disclaims Contractor liability for warranty claims.
- Record each warranty's start date, duration and claim route. A warranty whose start date is unknown is unenforceable in practice.
- Calendar warranty expiries into `CLO-013`.
- An unchecked condition is `not_found` or `blocked` — never `verified`, never blank.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Every warranty registered with start, duration and claim route
- Expiries calendared
- Manuals and as-builts indexed

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

- `CON-003` — Baseline schedule


## Typst issue version expected?

**No.** This artifact stays in Markdown. If it ever becomes an external submission, a stage-gate package, or a controlled-distribution PDF, update `typst_issue_required` in `artifact-register.csv` first — the register is the source of truth, not the file.
