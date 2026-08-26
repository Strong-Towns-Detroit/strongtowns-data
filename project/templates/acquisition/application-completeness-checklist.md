---
artifact_id: ACQ-007
artifact_type: checklist
title: Application completeness checklist
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
source_ids: [SRC-010, SRC-008, SRC-001]
depends_on: [ACQ-001]
supersedes: null
confidentiality: internal
---

# Application completeness checklist

`ACQ-007` · acquisition · service code `LND`

> **Parcel-specific.** Create one copy per candidate parcel under `working/candidate-parcels/<parcel-id>/`. Do not complete this template in place.

## Purpose

Confirms an application or offer package is complete against the receiving body's actual, current requirements before it is submitted.

## When to use it

Immediately before submission.

## Required inputs

- The receiving body's current requirement list
- All package components
- `SRC-010` portal field inventory

## Instructions

- Inventory the live form's actual fields before completing it. Do not reconstruct the form from a summary — the portal at `SRC-010` has not been field-inventoried and that is recorded as an open gap.
- For a development project, `SRC-008` requires at minimum a conceptual plan identifying proposed use, scope of work, estimated costs and financing sources, and prior experience with similar developments.
- For an Infill Housing Lot, `SRC-001` Ch.VI(C)(2)-(3) requires a thorough description of the proposed development and demonstrated capacity to finance and complete a 1-4 unit residential project within a reasonable time.
- Mark any requirement you could not verify as `blocked`, not `not_applicable`.
- Record the submission date, method, and a copy of exactly what was sent.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Every required field or attachment verified against the live form
- Conceptual plan components present where required
- Financial capacity evidence attached
- A copy of the submitted package retained

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Sources

Requirements in this artifact trace to the following rows in `source-register.csv`. Re-verify before relying on any of them — agency requirements change without notice.

| Source | Document | Status | Pinpoint |
| --- | --- | --- | --- |
| `SRC-010` | Public Property Purchase Application (portal) | `listed_not_retrieved` | — |
| `SRC-008` | Property Sales and Purchase FAQs | `verified` | Review-body list; conceptual plan requirement; market-value pricing; ~4-month timeline; 10% earnest money for commercial |
| `SRC-001` | Second Amended and Restated Vacant Land Policy | `verified` | Ch. VI (Infill Housing Lots), pp.16-18; Ch. VIII (Land-Based Projects) pp.21-23; Ch. IX (Land Review Areas) pp.24-25 |

## Unresolved questions

- What are the actual field requirements of the Public Property Purchase Application portal? Not yet inventoried.

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
