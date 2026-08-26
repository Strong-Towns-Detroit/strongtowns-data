---
artifact_id: CON-002
artifact_type: budget
title: Baseline budget
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
depends_on: [PRO-002]
supersedes: null
confidentiality: internal
---

# Baseline budget

`CON-002` · construction · service code `EST`

> **Parcel-specific.** Create one copy per candidate parcel under `working/candidate-parcels/<parcel-id>/`. Do not complete this template in place.

## Purpose

The baseline budget: the approved cost position against which all variance is measured.

## When to use it

At notice to proceed. Frozen thereafter; changes are tracked, not edited in.

## Required inputs

- `FIN-001` cost plan
- `PRO-005` levelled bids
- `PRO-006` scope gaps

## Instructions

- Freeze it. A baseline that gets quietly updated cannot produce a variance, and variance is the entire point.
- Carry allowances and contingency as separate visible lines (`CON-006`), not folded into trade totals.
- Reconcile to `PRO-005` levelled bids and record any difference.
- Every figure states its basis and confidence.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Baseline frozen and dated
- Allowances and contingency separately visible
- Reconciles to levelled bids
- Company approval recorded

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

- `PRO-002` — Builder and general-contractor RFP


**Stage gates this is required evidence for:** `SG-09`

## Typst issue version expected?

**Yes.** A paired Typst issue document is expected before this leaves the project. Base template: `publication/typst/templates/report.typ`.

Transfer reviewed content to the `.typ` deliberately — there is no automatic Markdown→Typst conversion. The Markdown draft and the Typst issue share this `artifact_id`; the Typst metadata records the draft path and its SHA-256.

Compilation is not approval. See `publication/README.md` for the issue gate.
