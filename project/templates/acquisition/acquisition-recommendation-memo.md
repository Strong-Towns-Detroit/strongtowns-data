---
artifact_id: ACQ-026
artifact_type: memo
title: Acquisition recommendation memo
workstream: acquisition
service_code: LND
status: template
template_version: "1.0"
parcel_ids: []
owner_role: contractor_program_manager
decision_role: company_decision_authority
required_reviewer_role: company_decision_authority
legal_review_required: false
typst_issue_required: true
typst_source: publication/typst/templates/memo.typ
latest_issue_id: null
created_at: 2026-08-26
updated_at: 2026-08-26
source_as_of: 2026-08-26
source_ids: [SRC-001]
depends_on: [ACQ-001]
supersedes: null
confidentiality: internal
---

# Acquisition recommendation memo

`ACQ-026` · acquisition · service code `LND`

> **Parcel-specific.** Create one copy per candidate parcel under `working/candidate-parcels/<parcel-id>/`. Do not complete this template in place.

## Purpose

The written analysis and recommendation on a candidate property required by ICA §1.2. Recommends; does not decide.

## When to use it

Once diligence is complete enough to support a recommendation.

## Required inputs

- `SCR-002` comparison memo
- `DD-026` red-flag memorandum
- `DD-027` go/no-go
- `ACQ-017` term sheet

## Instructions

- Lead with the recommendation in one sentence, then the basis.
- State the pathway and why it was selected over the alternatives — `ACQ-002` holds the comparison.
- Carry unresolved items forward visibly. A recommendation that hides an open question is worse than no recommendation.
- ICA §1.3 reserves the decision to the Company. Record the recommendation and the decision separately in `GOV-007`.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Recommendation stated in one sentence
- Pathway selection justified against alternatives
- Open items and their owners visible
- Issued as a Typst memo once approved

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Sources

Requirements in this artifact trace to the following rows in `source-register.csv`. Re-verify before relying on any of them — agency requirements change without notice.

| Source | Document | Status | Pinpoint |
| --- | --- | --- | --- |
| `SRC-001` | Second Amended and Restated Vacant Land Policy | `verified` | Ch. VI (Infill Housing Lots), pp.16-18; Ch. VIII (Land-Based Projects) pp.21-23; Ch. IX (Land Review Areas) pp.24-25 |

## Unresolved questions

_None recorded. Add any question that would change a decision if answered differently._

## Approvals and professional review

- **Required reviewer: `company_decision_authority`.** Record the review in `GOV-015` before this artifact is relied on at a gate.
- Conclusions reserved to that discipline must come from that professional, not from this document.

## Dependencies

**Upstream — this cannot be completed without:**

- `ACQ-001` — Acquisition pathway decision tree


## Typst issue version expected?

**Yes.** A paired Typst issue document is expected before this leaves the project. Base template: `publication/typst/templates/memo.typ`.

Transfer reviewed content to the `.typ` deliberately — there is no automatic Markdown→Typst conversion. The Markdown draft and the Typst issue share this `artifact_id`; the Typst metadata records the draft path and its SHA-256.

Compilation is not approval. See `publication/README.md` for the issue gate.
