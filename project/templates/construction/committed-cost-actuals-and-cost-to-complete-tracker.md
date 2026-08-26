---
artifact_id: CON-007
artifact_type: tracker
title: Committed cost, actuals and cost-to-complete tracker
workstream: construction
service_code: EST
status: template
template_version: "1.0"
parcel_ids: []
owner_role: contractor_program_manager
decision_role: company_decision_authority
required_reviewer_role: company_decision_authority
legal_review_required: false
typst_issue_required: true
typst_source: publication/typst/templates/report.typ
latest_issue_id: null
created_at: 2026-08-26
updated_at: 2026-08-26
source_as_of: null
source_ids: []
depends_on: [CON-003]
supersedes: null
confidentiality: internal
---

# Committed cost, actuals and cost-to-complete tracker

`CON-007` · construction · service code `EST`

> **Parcel-specific.** Create one copy per candidate parcel under `working/candidate-parcels/<parcel-id>/`. Do not complete this template in place.

## Purpose

Tracker for committed costs, actuals and cost-to-complete against the approved budget. ICA Exhibit A requires this and requires variances be flagged to the Company.

## When to use it

Continuously through construction.

## Required inputs

- `CON-002` baseline
- Commitments
- Invoices and actuals

## Instructions

- Track three distinct numbers: committed, spent, and forecast to complete. Reporting only spend hides the problem until it is unfixable.
- Cost-to-complete is a forecast, not arithmetic. State its basis and confidence.
- Exhibit A requires variances be flagged to the Company. Flag them when they appear, not when they are certain.
- Feeds the budget status and variance section of the weekly report (`GOV-017`).
- Every figure states its basis and confidence.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Committed, actual and cost-to-complete tracked separately
- Cost-to-complete has a stated basis
- Variances flagged when they appear
- Reconciles to `CON-002` baseline

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


**Stage gates this is required evidence for:** `SG-10`

## Typst issue version expected?

**Yes.** A paired Typst issue document is expected before this leaves the project. Base template: `publication/typst/templates/report.typ`.

Transfer reviewed content to the `.typ` deliberately — there is no automatic Markdown→Typst conversion. The Markdown draft and the Typst issue share this `artifact_id`; the Typst metadata records the draft path and its SHA-256.

Compilation is not approval. See `publication/README.md` for the issue gate.
