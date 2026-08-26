---
artifact_id: ACQ-009
artifact_type: narrative
title: Proposed-use and community-benefit statement
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

# Proposed-use and community-benefit statement

`ACQ-009` · acquisition · service code `LND`

> **Parcel-specific.** Create one copy per candidate parcel under `working/candidate-parcels/<parcel-id>/`. Do not complete this template in place.

## Purpose

States the proposed use and the benefit to the surrounding neighborhood — a scored criterion on both the marketed-property and Infill Housing Lot pathways.

## When to use it

Alongside the development proposal narrative.

## Required inputs

- Proposed use
- Community engagement record
- Any letters of support

## Instructions

- Both pathways weigh neighborhood benefit and neighbor support (`SRC-001` Ch.VI(E)(2); `SRC-009`). `SRC-009` states community engagement is required and that Office of Civil Rights certification earns additional points.
- Evidence engagement; do not assert it. Record who was engaged, when, and what they said — including objections.
- Do not draft statements of support on a supporter's behalf.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Engagement evidenced with dates and participants
- Objections recorded, not omitted
- Any certification claimed is held, not pending

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Sources

Requirements in this artifact trace to the following rows in `source-register.csv`. Re-verify before relying on any of them — agency requirements change without notice.

| Source | Document | Status | Pinpoint |
| --- | --- | --- | --- |
| `SRC-001` | Second Amended and Restated Vacant Land Policy | `verified` | Ch. VI (Infill Housing Lots), pp.16-18; Ch. VIII (Land-Based Projects) pp.21-23; Ch. IX (Land Review Areas) pp.24-25 |
| `SRC-009` | Marketing Programs (marketed properties) | `verified` | 60-day listing; ~90 days to close; scoring categories; six proposal-guideline categories including New Build Opportunities |

## Unresolved questions

- What is the Office of Civil Rights certification referenced by `SRC-009`, and what does it require? Link not published on the page.

## Approvals and professional review

- **Required reviewer: `company_decision_authority`.** Record the review in `GOV-015` before this artifact is relied on at a gate.
- Conclusions reserved to that discipline must come from that professional, not from this document.

## Dependencies

**Upstream — this cannot be completed without:**

- `ACQ-001` — Acquisition pathway decision tree


## Typst issue version expected?

**Yes.** A paired Typst issue document is expected before this leaves the project. Base template: `publication/typst/templates/application-package.typ`.

Transfer reviewed content to the `.typ` deliberately — there is no automatic Markdown→Typst conversion. The Markdown draft and the Typst issue share this `artifact_id`; the Typst metadata records the draft path and its SHA-256.

Compilation is not approval. See `publication/README.md` for the issue gate.
