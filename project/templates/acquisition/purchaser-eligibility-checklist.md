---
artifact_id: ACQ-004
artifact_type: checklist
title: Purchaser eligibility checklist
workstream: acquisition
service_code: LND
status: template
template_version: "1.0"
parcel_ids: []
owner_role: contractor_program_manager
decision_role: company_decision_authority
required_reviewer_role: michigan_licensed_attorney
legal_review_required: true
typst_issue_required: true
typst_source: publication/typst/templates/form-checklist.typ
latest_issue_id: null
created_at: 2026-08-26
updated_at: 2026-08-26
source_as_of: 2026-08-26
source_ids: [SRC-001, SRC-005]
depends_on: [ACQ-001]
supersedes: null
confidentiality: internal
---

# Purchaser eligibility checklist

`ACQ-004` · acquisition · service code `LND`

> **Reusable.** One copy project-wide, under `working/project-wide/`.

## Purpose

Confirms the purchasing entity is eligible to buy from the DLBA at all. Failing any one of these is disqualifying regardless of the merits of the project.

## When to use it

Before any offer or application, and re-checked before closing.

## Required inputs

- Purchasing entity's legal name and Michigan registration
- Wayne County property tax status for all entity-owned Detroit property
- City of Detroit blight and code violation status
- Any existing DLBA agreements

## Instructions

- Check every criterion against a primary record, not a recollection. The general DLBA eligibility bars are: delinquent Wayne County property taxes; property lost to tax foreclosure in Wayne County within three years (other than a primary residence); outstanding Detroit blight or code violations; active bankruptcy; non-compliance with Nuisance Abatement proceedings (`SRC-005`).
- For an Infill Housing Lot specifically, the purchaser must additionally be current on taxes for ALL property owned directly or indirectly in Detroit, be in good standing on any DLBA agreement, and must not have purchased three or more Infill Housing Lots in the preceding twelve months (`SRC-001` Ch.VI(C)(4)-(6)).
- Entities must be licensed to do business in Michigan (`SRC-005`).
- The three-lot ceiling is a programme-level constraint on Krabby's pipeline, not just this parcel. Track cumulative purchases centrally.
- Re-check immediately before closing. Eligibility is a state, not an event, and a violation acquired mid-transaction still disqualifies.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Every general eligibility bar checked against a primary record
- Infill-specific criteria checked where that pathway applies
- Cumulative Infill Housing Lot count for the preceding twelve months recorded
- Re-check performed within a stated window of closing

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Sources

Requirements in this artifact trace to the following rows in `source-register.csv`. Re-verify before relying on any of them — agency requirements change without notice.

| Source | Document | Status | Pinpoint |
| --- | --- | --- | --- |
| `SRC-001` | Second Amended and Restated Vacant Land Policy | `verified` | Ch. VI (Infill Housing Lots), pp.16-18; Ch. VIII (Land-Based Projects) pp.21-23; Ch. IX (Land Review Areas) pp.24-25 |
| `SRC-005` | Frequently Asked Questions | `verified` | Buyer eligibility list; deed and closing section; closing-cost estimates |

## Unresolved questions

- Does the three-lot ceiling count lots purchased by affiliated entities? The policy says 'directly or indirectly' but does not define affiliation.

## Approvals and professional review

- **Required reviewer: `michigan_licensed_attorney`.** `legal_review_required: true` — every stage gate this artifact feeds is blocked until that review is recorded in `GOV-015` (professional-review tracker).
- This document is an *issue-spotting tool*. It does not contain legal advice and must not be treated as a substitute for counsel.
- Record the reviewer, the date, and the scope reviewed. A review with no recorded scope does not clear the gate.

## Dependencies

**Upstream — this cannot be completed without:**

- `ACQ-001` — Acquisition pathway decision tree


## Typst issue version expected?

**Yes.** A paired Typst issue document is expected before this leaves the project. Base template: `publication/typst/templates/form-checklist.typ`.

Transfer reviewed content to the `.typ` deliberately — there is no automatic Markdown→Typst conversion. The Markdown draft and the Typst issue share this `artifact_id`; the Typst metadata records the draft path and its SHA-256.

Compilation is not approval. See `publication/README.md` for the issue gate.
