---
artifact_id: ACQ-025
artifact_type: abstract
title: Post-closing covenant and reverter abstract
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
typst_source: publication/typst/templates/report.typ
latest_issue_id: null
created_at: 2026-08-26
updated_at: 2026-08-26
source_as_of: 2026-08-26
source_ids: [SRC-001, SRC-005, SRC-007]
depends_on: [ACQ-001]
supersedes: null
confidentiality: internal
---

# Post-closing covenant and reverter abstract

`ACQ-025` · acquisition · service code `LND`

> **Parcel-specific.** Create one copy per candidate parcel under `working/candidate-parcels/<parcel-id>/`. Do not complete this template in place.

## Purpose

Abstracts every obligation that survives closing — covenants, restrictions, reverter and repurchase rights, compliance deadlines — into one place with owners and dates.

## When to use it

Immediately after closing, and maintained until every obligation is discharged.

## Required inputs

- Recorded deed
- Development agreement
- Reconveyance deed
- `SRC-007` compliance requirements

## Instructions

- Abstract from the executed instruments, not from the marketing description of the programme.
- For an Infill Housing Lot, the development agreement under `SRC-001` Ch.VI(F) governs type, density, schedules, timelines and affordability monitoring, and DLBA reserves the right to take back title on violation. Every one of those is a dated obligation with an owner.
- Where a discount was taken for affordability, the monitored period is at least ten years (Ch.VI(D)(1)). Calendar it to expiry, not to the next milestone.
- Do not import the `SRC-007` compliance timeline (15/45/60 day photo milestones) into a vacant-land infill purchase — that page describes structure-sale compliance. Establish the actual applicable regime from the executed agreement.
- Extension and waiver procedure is not published (`SRC-007` is silent). Record that as unresolved rather than assuming none exists.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Every surviving obligation abstracted with a deadline, an owner and an evidence requirement
- Reverter and take-back triggers stated explicitly
- Affordability monitoring period calendared to expiry
- The applicable compliance regime established from the executed instrument, not from a web page

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Sources

Requirements in this artifact trace to the following rows in `source-register.csv`. Re-verify before relying on any of them — agency requirements change without notice.

| Source | Document | Status | Pinpoint |
| --- | --- | --- | --- |
| `SRC-001` | Second Amended and Restated Vacant Land Policy | `verified` | Ch. VI (Infill Housing Lots), pp.16-18; Ch. VIII (Land-Based Projects) pp.21-23; Ch. IX (Land Review Areas) pp.24-25 |
| `SRC-005` | Frequently Asked Questions | `verified` | Buyer eligibility list; deed and closing section; closing-cost estimates |
| `SRC-007` | Compliance | `verified` | Post-sale timeline table (15/45/60 day milestones); evidence rules; Release of Interest |

## Unresolved questions

- What is the DLBA's procedure for requesting an extension or waiver of a compliance deadline? Not published on `SRC-007`.
- What compliance regime applies to a vacant Infill Housing Lot purchase, as distinct from a structure sale?

## Approvals and professional review

- **Required reviewer: `michigan_licensed_attorney`.** `legal_review_required: true` — every stage gate this artifact feeds is blocked until that review is recorded in `GOV-015` (professional-review tracker).
- This document is an *issue-spotting tool*. It does not contain legal advice and must not be treated as a substitute for counsel.
- Record the reviewer, the date, and the scope reviewed. A review with no recorded scope does not clear the gate.

## Dependencies

**Upstream — this cannot be completed without:**

- `ACQ-001` — Acquisition pathway decision tree


## Typst issue version expected?

**Yes.** A paired Typst issue document is expected before this leaves the project. Base template: `publication/typst/templates/report.typ`.

Transfer reviewed content to the `.typ` deliberately — there is no automatic Markdown→Typst conversion. The Markdown draft and the Typst issue share this `artifact_id`; the Typst metadata records the draft path and its SHA-256.

Compilation is not approval. See `publication/README.md` for the issue gate.
