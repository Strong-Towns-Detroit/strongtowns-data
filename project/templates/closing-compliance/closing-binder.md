---
artifact_id: CLO-006
artifact_type: binder
title: Closing binder
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
typst_source: publication/typst/templates/binder.typ
latest_issue_id: null
created_at: 2026-08-26
updated_at: 2026-08-26
source_as_of: null
source_ids: []
depends_on: [ACQ-023]
supersedes: null
confidentiality: internal
---

# Closing binder

`CLO-006` · closing-compliance · service code `LND`

> **Parcel-specific.** Create one copy per candidate parcel under `working/candidate-parcels/<parcel-id>/`. Do not complete this template in place.

## Purpose

The assembled closing binder — a record, not a summary.

## When to use it

Assembled through closing, issued after.

## Required inputs

- All closing documents
- `ACQ-024` binder index

## Instructions

- Every tab listed in the index must be present. A tab listed but not attached is recorded `blocked`, never omitted.
- Include the development agreement and any reconveyance instrument — they govern obligations that outlive the closing and are the documents most often needed later.
- Issue as a Typst binder; record the manifest.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Every tab present or explicitly blocked
- Post-closing obligation documents included
- Typst binder compiled, inspected, and manifest validated

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


## Typst issue version expected?

**Yes.** A paired Typst issue document is expected before this leaves the project. Base template: `publication/typst/templates/binder.typ`.

Transfer reviewed content to the `.typ` deliberately — there is no automatic Markdown→Typst conversion. The Markdown draft and the Typst issue share this `artifact_id`; the Typst metadata records the draft path and its SHA-256.

Compilation is not approval. See `publication/README.md` for the issue gate.
