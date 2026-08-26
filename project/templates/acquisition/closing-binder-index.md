---
artifact_id: ACQ-024
artifact_type: index
title: Closing binder index
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
typst_source: publication/typst/templates/binder.typ
latest_issue_id: null
created_at: 2026-08-26
updated_at: 2026-08-26
source_as_of: 2026-08-26
source_ids: [SRC-005]
depends_on: [ACQ-001]
supersedes: null
confidentiality: internal
---

# Closing binder index

`ACQ-024` · acquisition · service code `LND`

> **Parcel-specific.** Create one copy per candidate parcel under `working/candidate-parcels/<parcel-id>/`. Do not complete this template in place.

## Purpose

Index of the assembled closing binder. The binder is a record; this is its table of contents and its completeness check.

## When to use it

Assembled through closing, finalised immediately after.

## Required inputs

- All closing documents
- `ACQ-023` conditions checklist

## Instructions

- A tab listed but not attached is a defect in the record. Record it as `blocked`, never omit it.
- Include the development agreement and any reconveyance instrument — they govern obligations that outlive the closing.
- Issue as a Typst binder once complete.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Every tab present or explicitly marked blocked
- Post-closing obligation documents included
- Binder issued and manifest validated

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Sources

Requirements in this artifact trace to the following rows in `source-register.csv`. Re-verify before relying on any of them — agency requirements change without notice.

| Source | Document | Status | Pinpoint |
| --- | --- | --- | --- |
| `SRC-005` | Frequently Asked Questions | `verified` | Buyer eligibility list; deed and closing section; closing-cost estimates |

## Unresolved questions

_None recorded. Add any question that would change a decision if answered differently._

## Approvals and professional review

- **Required reviewer: `michigan_licensed_attorney`.** `legal_review_required: true` — every stage gate this artifact feeds is blocked until that review is recorded in `GOV-015` (professional-review tracker).
- This document is an *issue-spotting tool*. It does not contain legal advice and must not be treated as a substitute for counsel.
- Record the reviewer, the date, and the scope reviewed. A review with no recorded scope does not clear the gate.

## Dependencies

**Upstream — this cannot be completed without:**

- `ACQ-001` — Acquisition pathway decision tree


## Typst issue version expected?

**Yes.** A paired Typst issue document is expected before this leaves the project. Base template: `publication/typst/templates/binder.typ`.

Transfer reviewed content to the `.typ` deliberately — there is no automatic Markdown→Typst conversion. The Markdown draft and the Typst issue share this `artifact_id`; the Typst metadata records the draft path and its SHA-256.

Compilation is not approval. See `publication/README.md` for the issue gate.
