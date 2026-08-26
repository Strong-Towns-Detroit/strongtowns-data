---
artifact_id: CLO-001
artifact_type: memo
title: Pre-closing authorization memo
workstream: closing-compliance
service_code: LND
status: template
template_version: "1.0"
parcel_ids: []
owner_role: contractor_program_manager
decision_role: company_decision_authority
required_reviewer_role: michigan_licensed_attorney
legal_review_required: true
typst_issue_required: true
typst_source: publication/typst/templates/memo.typ
latest_issue_id: null
created_at: 2026-08-26
updated_at: 2026-08-26
source_as_of: null
source_ids: []
depends_on: [ACQ-023]
supersedes: null
confidentiality: internal
---

# Pre-closing authorization memo

`CLO-001` · closing-compliance · service code `LND`

> **Parcel-specific.** Create one copy per candidate parcel under `working/candidate-parcels/<parcel-id>/`. Do not complete this template in place.

## Purpose

Memo recommending that the Company authorise closing, with the conditions satisfied and the ones knowingly accepted.

## When to use it

At `SG-05`, before funds move.

## Required inputs

- `ACQ-023` closing conditions
- `DD-027` go/no-go
- `ACQ-019` issue checklist
- `GOV-015` review records

## Instructions

- State plainly which conditions are satisfied, which are waived, and who waived them. A closing memo that reads as uniformly positive is not a memo.
- Confirm counsel has reviewed the conveyance terms and that the review is recorded in `GOV-015`, scoped to the version being signed.
- Recommend; the Company authorises. ICA §1.3 and §3.2 both place the authorization with the Company.
- Issue as a Typst memo once approved.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Every closing condition stated as satisfied, waived, or blocked
- Counsel review recorded and version-scoped
- Waivers name their authority
- Typst issue compiled and visually inspected

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Sources

_No external requirements cited. If this artifact starts asserting one, add a row to `source-register.csv` first._

## Unresolved questions

_None recorded. Add any question that would change a decision if answered differently._

## Approvals and professional review

- **Required reviewer: `michigan_licensed_attorney`.** `legal_review_required: true` — every stage gate this artifact feeds is blocked until that review is recorded in `GOV-015` (professional-review tracker).
- This document is an *issue-spotting tool*. It does not contain legal advice and must not be treated as a substitute for counsel.
- Record the reviewer, the date, and the scope reviewed. A review with no recorded scope does not clear the gate.

## Dependencies

**Upstream — this cannot be completed without:**

- `ACQ-023` — Closing-conditions checklist


**Stage gates this is required evidence for:** `SG-05`

## Typst issue version expected?

**Yes.** A paired Typst issue document is expected before this leaves the project. Base template: `publication/typst/templates/memo.typ`.

Transfer reviewed content to the `.typ` deliberately — there is no automatic Markdown→Typst conversion. The Markdown draft and the Typst issue share this `artifact_id`; the Typst metadata records the draft path and its SHA-256.

Compilation is not approval. See `publication/README.md` for the issue gate.
