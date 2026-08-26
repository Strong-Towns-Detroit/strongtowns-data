---
artifact_id: CON-006
artifact_type: log
title: Allowance and contingency log
workstream: construction
service_code: EST
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

# Allowance and contingency log

`CON-006` · construction · service code `EST`

> **Parcel-specific.** Create one copy per candidate parcel under `working/candidate-parcels/<parcel-id>/`. Do not complete this template in place.

## Purpose

Log of allowances and contingency: what remains, what it was drawn for, and who authorised.

## When to use it

From the baseline onward.

## Required inputs

- `CON-002` baseline budget
- Authorised drawdowns

## Instructions

- Track each allowance separately against its stated purpose. A pooled contingency is spent by whoever asks first.
- Record the authorising decision for every drawdown. Reconcile to `GOV-021` where Company funds are committed.
- Report remaining balance in the weekly report — it is the single best early indicator of budget trouble.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Every allowance tracked against its purpose
- Every drawdown has a recorded authorization
- Remaining balances reported weekly

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
