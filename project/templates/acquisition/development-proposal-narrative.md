---
artifact_id: ACQ-008
artifact_type: proposal
title: Development proposal narrative
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
typst_source: publication/typst/templates/application-package.typ
latest_issue_id: null
created_at: 2026-08-26
updated_at: 2026-08-26
source_as_of: 2026-08-26
source_ids: [SRC-001, SRC-009]
depends_on: [ACQ-001]
supersedes: null
confidentiality: internal
---

# Development proposal narrative

`ACQ-008` · acquisition · service code `LND`

> **Parcel-specific.** Create one copy per candidate parcel under `working/candidate-parcels/<parcel-id>/`. Do not complete this template in place.

## Purpose

The development proposal narrative submitted to the disposing body. For an Infill Housing Lot this is the 'thorough description of the proposed development' the policy requires; for marketed property it is the substance the DLBA scores.

## When to use it

Once the design basis and cost plan are firm enough to describe honestly.

## Required inputs

- `SCR-003` owner's project requirements
- Concept site plan
- `SCR-008` cost screen
- Development schedule
- Financing evidence

## Instructions

- Write to the criteria the body actually scores. For marketed property `SRC-009` names price, experience and financing, project feasibility, and neighborhood benefit. For Infill Housing Lots `SRC-001` Ch.VI(E)(2) names offer price, community benefit, purchaser experience and financial capability, connection to the neighborhood, proposed use, and support of neighbors and local organizations.
- Published scoring weights were not available for either pathway. Do not infer them; treat all named criteria as material.
- State the housing type, density, and schedule concretely — these become terms of the development agreement under Ch.VI(F) and will bind.
- Do not promise what the cost plan cannot support. A schedule offered to win a parcel becomes a deadline enforceable by reverter.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Every named scoring criterion addressed explicitly
- Type, density and schedule stated in terms that can survive becoming contractual
- Financial capacity evidenced, not asserted
- Community engagement evidenced where the pathway weighs it

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Sources

Requirements in this artifact trace to the following rows in `source-register.csv`. Re-verify before relying on any of them — agency requirements change without notice.

| Source | Document | Status | Pinpoint |
| --- | --- | --- | --- |
| `SRC-001` | Second Amended and Restated Vacant Land Policy | `verified` | Ch. VI (Infill Housing Lots), pp.16-18; Ch. VIII (Land-Based Projects) pp.21-23; Ch. IX (Land Review Areas) pp.24-25 |
| `SRC-009` | Marketing Programs (marketed properties) | `verified` | 60-day listing; ~90 days to close; scoring categories; six proposal-guideline categories including New Build Opportunities |

## Unresolved questions

- Are the scoring weights for either pathway published anywhere? Not found on the public pages.

## Approvals and professional review

- **Required reviewer: `company_decision_authority`.** Record the review in `GOV-015` before this artifact is relied on at a gate.
- Conclusions reserved to that discipline must come from that professional, not from this document.

## Dependencies

**Upstream — this cannot be completed without:**

- `ACQ-001` — Acquisition pathway decision tree


**Stage gates this is required evidence for:** `SG-03`

## Typst issue version expected?

**Yes.** A paired Typst issue document is expected before this leaves the project. Base template: `publication/typst/templates/application-package.typ`.

Transfer reviewed content to the `.typ` deliberately — there is no automatic Markdown→Typst conversion. The Markdown draft and the Typst issue share this `artifact_id`; the Typst metadata records the draft path and its SHA-256.

Compilation is not approval. See `publication/README.md` for the issue gate.
