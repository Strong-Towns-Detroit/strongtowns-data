---
artifact_id: DD-010
artifact_type: memo
title: Zoning confirmation memo
workstream: due-diligence
service_code: PMT
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
source_as_of: 2026-08-26
source_ids: [SRC-001, SRC-002]
depends_on: [DD-001]
supersedes: null
confidentiality: internal
---

# Zoning confirmation memo

`DD-010` · due-diligence · service code `PMT`

> **Parcel-specific.** Create one copy per candidate parcel under `working/candidate-parcels/<parcel-id>/`. Do not complete this template in place.

## Purpose

Confirms the zoning district and what it permits, in writing from the authority — not from a map viewer.

## When to use it

Early. Zoning is an eligibility criterion as well as a design constraint.

## Required inputs

- Parcel ID
- City zoning map and ordinance

## Instructions

- Obtain written confirmation. A map viewer is a starting point, not a determination.
- `SRC-001` Ch. VI(B)(4) restricts Infill Housing Lots to R1, R1-H, R2, R3, R3H, R4, R5, R5-H, R6, R6-H, PD, PD-H, SD1, SD1-H, SD2, SD2-H, SD4. Note this list differs from the narrower list in `SRC-002` — cite the correct policy for the pathway.
- Record the ordinance section, not just the district label.
- Any conclusion reserved to a licensed discipline comes from that professional, not from this artifact.
- A condition not yet checked is recorded `not_found` or `blocked` — never `verified`, never blank.

## Completion criteria

This artifact is complete when **all** of the following hold:

- District confirmed in writing with a date
- Ordinance sections cited
- Programme eligibility under Ch. VI(B)(4) confirmed

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Sources

Requirements in this artifact trace to the following rows in `source-register.csv`. Re-verify before relying on any of them — agency requirements change without notice.

| Source | Document | Status | Pinpoint |
| --- | --- | --- | --- |
| `SRC-001` | Second Amended and Restated Vacant Land Policy | `verified` | Ch. VI (Infill Housing Lots), pp.16-18; Ch. VIII (Land-Based Projects) pp.21-23; Ch. IX (Land Review Areas) pp.24-25 |
| `SRC-002` | Neighborhood Create-a-Project Pilot Policy | `conflicting` | Sec. I (Objective) p.1; Sec. II (Purchaser Eligibility) p.1; Sec. III (Property Eligibility) pp.1-2; Sec. IV (Terms) p.2; Sec. V (Compliance) p.2 |

## Unresolved questions

- Does the City issue written zoning verifications, and at what cost and turnaround?

## Approvals and professional review

- **Required reviewer: `michigan_licensed_attorney`.** `legal_review_required: true` — every stage gate this artifact feeds is blocked until that review is recorded in `GOV-015` (professional-review tracker).
- This document is an *issue-spotting tool*. It does not contain legal advice and must not be treated as a substitute for counsel.
- Record the reviewer, the date, and the scope reviewed. A review with no recorded scope does not clear the gate.

## Dependencies

**Upstream — this cannot be completed without:**

- `DD-001` — Due-diligence plan and deadline calculator

**Downstream — these depend on this:**

- `APR-001` — Permit and approval matrix

## Typst issue version expected?

**Yes.** A paired Typst issue document is expected before this leaves the project. Base template: `publication/typst/templates/memo.typ`.

Transfer reviewed content to the `.typ` deliberately — there is no automatic Markdown→Typst conversion. The Markdown draft and the Typst issue share this `artifact_id`; the Typst metadata records the draft path and its SHA-256.

Compilation is not approval. See `publication/README.md` for the issue gate.
