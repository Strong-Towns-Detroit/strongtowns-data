---
artifact_id: ACQ-019
artifact_type: checklist
title: Purchase-agreement issue checklist
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
source_ids: [SRC-001, SRC-005]
depends_on: [ACQ-001]
supersedes: null
confidentiality: internal
---

# Purchase-agreement issue checklist

`ACQ-019` · acquisition · service code `LND`

> **Parcel-specific.** Create one copy per candidate parcel under `working/candidate-parcels/<parcel-id>/`. Do not complete this template in place.

## Purpose

Issue checklist for a purchase agreement supplied by the DLBA or the City. It is a tool for spotting what to ask counsel about — it is not a draft agreement and contains no legal advice.

## When to use it

On receipt of a draft agreement, before counsel review, so counsel's time is spent on judgement rather than reading.

## Required inputs

- The counterparty's draft agreement
- `ACQ-017` term sheet
- Diligence findings

## Instructions

- Work the full issue list: parties and authority; parcel and legal description; price, deposit and payment; Board or governmental approval; title and conveyance; taxes, assessments and liens; as-is condition; access and inspection; due-diligence period; environmental allocation; development and occupancy obligations; deed restrictions; compliance deadlines; reverter or repurchase rights; assignment; casualty and condemnation; default and remedies; indemnity and insurance; closing deliverables; survival; required attorney review.
- Pay particular attention to the development agreement contemplated by `SRC-001` Ch.VI(F): it sets type, density, required schedules and timelines, and affordability monitoring, and DLBA reserves the right to take back title on violation. Those terms are the real consideration.
- DLBA conveys by Quit Claim Deed with a Reconveyance Deed securing performance (`SRC-005`). Understand what that means for title insurability before closing.
- Do not redraft the counterparty's agreement here. Record the issue and the question for counsel.
- Every issue gets one of: acceptable, negotiate, or refer to counsel. Nothing is left unmarked.

## Completion criteria

This artifact is complete when **all** of the following hold:

- All twenty-one issue headings addressed
- Reverter, reconveyance and development-agreement terms specifically analysed
- Every issue marked acceptable / negotiate / refer
- Counsel instructed via `ACQ-020` before signature

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Sources

Requirements in this artifact trace to the following rows in `source-register.csv`. Re-verify before relying on any of them — agency requirements change without notice.

| Source | Document | Status | Pinpoint |
| --- | --- | --- | --- |
| `SRC-001` | Second Amended and Restated Vacant Land Policy | `verified` | Ch. VI (Infill Housing Lots), pp.16-18; Ch. VIII (Land-Based Projects) pp.21-23; Ch. IX (Land Review Areas) pp.24-25 |
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


**Stage gates this is required evidence for:** `SG-05`

## Typst issue version expected?

**Yes.** A paired Typst issue document is expected before this leaves the project. Base template: `publication/typst/templates/form-checklist.typ`.

Transfer reviewed content to the `.typ` deliberately — there is no automatic Markdown→Typst conversion. The Markdown draft and the Typst issue share this `artifact_id`; the Typst metadata records the draft path and its SHA-256.

Compilation is not approval. See `publication/README.md` for the issue gate.
