---
artifact_id: ACQ-014
artifact_type: checklist
title: Organizational-authority checklist
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
source_ids: [SRC-001, SRC-008]
depends_on: [ACQ-001]
supersedes: null
confidentiality: internal
---

# Organizational-authority checklist

`ACQ-014` · acquisition · service code `LND`

> **Reusable.** One copy project-wide, under `working/project-wide/`.

## Purpose

Evidences that the signing individual can bind the purchasing entity.

## When to use it

Before any offer is signed.

## Required inputs

- The receiving body's current requirement list
- Corresponding upstream artifact

## Instructions

- Verify the requirement against the live form or the adopted policy before completing this.
- `SRC-001` Ch.VI(C)(3) requires demonstrated capacity to finance AND complete a 1-4 unit residential project within a reasonable time — capacity to buy is not the test.
- Anything offered here that describes future performance may become a term of the development agreement under Ch.VI(F). Offer what can be delivered.
- Mark unverified requirements `blocked`.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Every element traced to a stated requirement
- Nothing asserted that the cost plan or schedule cannot support
- Unverified requirements marked `blocked`

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Sources

Requirements in this artifact trace to the following rows in `source-register.csv`. Re-verify before relying on any of them — agency requirements change without notice.

| Source | Document | Status | Pinpoint |
| --- | --- | --- | --- |
| `SRC-001` | Second Amended and Restated Vacant Land Policy | `verified` | Ch. VI (Infill Housing Lots), pp.16-18; Ch. VIII (Land-Based Projects) pp.21-23; Ch. IX (Land Review Areas) pp.24-25 |
| `SRC-008` | Property Sales and Purchase FAQs | `verified` | Review-body list; conceptual plan requirement; market-value pricing; ~4-month timeline; 10% earnest money for commercial |

## Unresolved questions

_None recorded. Add any question that would change a decision if answered differently._

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
