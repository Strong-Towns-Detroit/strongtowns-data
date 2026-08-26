---
artifact_id: PRO-010
artifact_type: record
title: Bid comparison record
workstream: procurement
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
depends_on: [DSN-012]
supersedes: null
confidentiality: internal
---

# Bid comparison record

`PRO-010` · procurement · service code `EST`

> **Parcel-specific.** Create one copy per candidate parcel under `working/candidate-parcels/<parcel-id>/`. Do not complete this template in place.

## Purpose

The bid comparison record ICA Exhibit A requires the Contractor to maintain.

## When to use it

On completion of levelling.

## Required inputs

- `PRO-005` levelled bids
- `PRO-006` scope gaps
- `PRO-007` qualification results

## Instructions

- Record price, schedule, qualification status and scope-gap exposure together. Price alone has never been the decision.
- Recommend; do not award. ICA §7.2 reserves selection and engagement of builders to the Company.
- Retain the record. Exhibit A requires a bid comparison record be maintained, and it is the evidence that the recommendation was reasoned.

## Completion criteria

This artifact is complete when **all** of the following hold:

- All bidders compared on price, schedule, qualification and scope exposure
- Recommendation separated from decision
- Record retained
- Company decision recorded separately in `GOV-007`

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

- `DSN-012` — Design deliverables register


**Stage gates this is required evidence for:** `SG-08`

## Typst issue version expected?

**No.** This artifact stays in Markdown. If it ever becomes an external submission, a stage-gate package, or a controlled-distribution PDF, update `typst_issue_required` in `artifact-register.csv` first — the register is the source of truth, not the file.
