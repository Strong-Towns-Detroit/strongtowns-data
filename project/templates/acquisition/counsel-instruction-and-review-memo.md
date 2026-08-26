---
artifact_id: ACQ-020
artifact_type: handoff
title: Counsel instruction and review memo
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
typst_source: publication/typst/templates/professional-handoff.typ
latest_issue_id: null
created_at: 2026-08-26
updated_at: 2026-08-26
source_as_of: 2026-08-26
source_ids: [SRC-001, SRC-005]
depends_on: [ACQ-001]
supersedes: null
confidentiality: internal
---

# Counsel instruction and review memo

`ACQ-020` · acquisition · service code `LND`

> **Parcel-specific.** Create one copy per candidate parcel under `working/candidate-parcels/<parcel-id>/`. Do not complete this template in place.

## Purpose

Instructs counsel: states the facts, the assumptions, and the precise questions to be answered. Asking a well-formed question is the whole job of this artifact.

## When to use it

Before counsel begins work on any agreement or conveyance.

## Required inputs

- `ACQ-019` issue checklist
- Diligence findings
- `ACQ-017` term sheet
- The counterparty's draft instrument

## Instructions

- State questions, not conclusions. A handoff that argues its own answer wastes the review.
- Attach the actual instrument, not a summary of it.
- Declare every assumption the questions rest on, with its resolving test.
- Flag the two structural features most likely to matter: the Quit Claim / Reconveyance Deed structure (`SRC-005`) and the development agreement with take-back rights under `SRC-001` Ch.VI(F).
- Record the review in `GOV-015` when it returns, scoped to the version reviewed.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Every question is answerable as asked
- All materials attached in original form
- Assumptions declared
- Review recorded in `GOV-015`

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

**Yes.** A paired Typst issue document is expected before this leaves the project. Base template: `publication/typst/templates/professional-handoff.typ`.

Transfer reviewed content to the `.typ` deliberately — there is no automatic Markdown→Typst conversion. The Markdown draft and the Typst issue share this `artifact_id`; the Typst metadata records the draft path and its SHA-256.

Compilation is not approval. See `publication/README.md` for the issue gate.
