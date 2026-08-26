---
artifact_id: ACQ-003
artifact_type: checklist
title: Ownership and disposition-path checklist
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
source_ids: [SRC-011, SRC-001, SRC-008]
depends_on: [ACQ-001]
supersedes: null
confidentiality: internal
---

# Ownership and disposition-path checklist

`ACQ-003` · acquisition · service code `LND`

> **Parcel-specific.** Create one copy per candidate parcel under `working/candidate-parcels/<parcel-id>/`. Do not complete this template in place.

## Purpose

Determines which entity owns a parcel and therefore which disposition rules apply. This is the first branch of the entire acquisition process — DLBA-owned and City-owned property follow different rules, different review bodies, and different approval authorities.

## When to use it

On every candidate parcel, before any other acquisition work.

## Required inputs

- Parcel ID and address
- Detroit Development Opportunities map (`SRC-011`)
- Assessor record of current owner

## Instructions

- Determine ownership from the City's Development Opportunities map, not from a listing or an assumption.
- DLBA-owned → the Second Amended and Restated Vacant Land Policy (`SRC-001`) governs. City-owned → the Public Property Purchase Application path governs, and City Council is the final decision maker (`SRC-008`).
- Privately owned → neither applies; this becomes a direct-approach or broker transaction.
- Record the date ownership was checked. Land bank inventory turns over constantly.
- Where ownership is ambiguous or the map disagrees with the assessor record, mark the condition `blocked` and resolve with the owning body before proceeding.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Owning entity identified from a primary source with a retrieval date
- The governing disposition pathway named
- Any ownership ambiguity recorded as `blocked`, not resolved by assumption

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Sources

Requirements in this artifact trace to the following rows in `source-register.csv`. Re-verify before relying on any of them — agency requirements change without notice.

| Source | Document | Status | Pinpoint |
| --- | --- | --- | --- |
| `SRC-011` | Detroit Development Opportunities map | `listed_not_retrieved` | — |
| `SRC-001` | Second Amended and Restated Vacant Land Policy | `verified` | Ch. VI (Infill Housing Lots), pp.16-18; Ch. VIII (Land-Based Projects) pp.21-23; Ch. IX (Land Review Areas) pp.24-25 |
| `SRC-008` | Property Sales and Purchase FAQs | `verified` | Review-body list; conceptual plan requirement; market-value pricing; ~4-month timeline; 10% earnest money for commercial |

## Unresolved questions

- Does the Development Opportunities map expose an underlying service the pipeline can query directly?

## Approvals and professional review

- **Required reviewer: `michigan_licensed_attorney`.** `legal_review_required: true` — every stage gate this artifact feeds is blocked until that review is recorded in `GOV-015` (professional-review tracker).
- This document is an *issue-spotting tool*. It does not contain legal advice and must not be treated as a substitute for counsel.
- Record the reviewer, the date, and the scope reviewed. A review with no recorded scope does not clear the gate.

## Dependencies

**Upstream — this cannot be completed without:**

- `ACQ-001` — Acquisition pathway decision tree


**Stage gates this is required evidence for:** `SG-03`

## Typst issue version expected?

**Yes.** A paired Typst issue document is expected before this leaves the project. Base template: `publication/typst/templates/form-checklist.typ`.

Transfer reviewed content to the `.typ` deliberately — there is no automatic Markdown→Typst conversion. The Markdown draft and the Typst issue share this `artifact_id`; the Typst metadata records the draft path and its SHA-256.

Compilation is not approval. See `publication/README.md` for the issue gate.
