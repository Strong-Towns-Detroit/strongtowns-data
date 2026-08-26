---
artifact_id: CON-005
artifact_type: log
title: Change-event and change-order log
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

# Change-event and change-order log

`CON-005` · construction · service code `EST`

> **Parcel-specific.** Create one copy per candidate parcel under `working/candidate-parcels/<parcel-id>/`. Do not complete this template in place.

## Purpose

Log of change events and change orders, tracked for cost and schedule impact.

## When to use it

From the first change event.

## Required inputs

- Change requests
- `CON-002` baseline budget
- `CON-003` baseline schedule

## Instructions

- Log the event when it arises, not when it is priced. Unpriced change events are the ones that surprise the budget.
- Record both cost and schedule impact. A change order with no time impact stated has an unstated time impact.
- The Contractor tracks and reports the impact; the Company decides and contracts. ICA §7.2 keeps construction contracting with the Company.
- Anything requiring Company authorization goes into the weekly report (`GOV-017`) under expenditures needing authorization.
- Every figure states its basis and confidence.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Every change event logged at onset
- Cost and schedule impact both stated
- Authorization needs escalated weekly
- The track-versus-contract boundary respected

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

**Yes.** A paired Typst issue document is expected before this leaves the project. Base template: `publication/typst/templates/report.typ`.

Transfer reviewed content to the `.typ` deliberately — there is no automatic Markdown→Typst conversion. The Markdown draft and the Typst issue share this `artifact_id`; the Typst metadata records the draft path and its SHA-256.

Compilation is not approval. See `publication/README.md` for the issue gate.
