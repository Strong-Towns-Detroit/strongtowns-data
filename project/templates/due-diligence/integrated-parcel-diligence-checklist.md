---
artifact_id: DD-002
artifact_type: checklist
title: Integrated parcel diligence checklist
workstream: due-diligence
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
source_ids: [SRC-001]
depends_on: [DD-001]
supersedes: null
confidentiality: internal
---

# Integrated parcel diligence checklist

`DD-002` · due-diligence · service code `LND`

> **Parcel-specific.** Create one copy per candidate parcel under `working/candidate-parcels/<parcel-id>/`. Do not complete this template in place.

## Purpose

The single per-parcel checklist that every other diligence artifact rolls up into. It is the thing a gate reads.

## When to use it

Opened at diligence start, maintained throughout, closed at `SG-04`.

## Required inputs

- Every DD-series artifact for the parcel
- `DD-001` deadline calendar

## Instructions

- Roll up conditions; do not restate findings. Each row points at the artifact holding the evidence.
- Use the controlled vocabulary on every row. This checklist is what makes 'no condition is silently unknown' checkable at the gate.
- A row marked `not_applicable` states why. 'N/A' with no reason is an unexamined condition wearing a disguise.
- A condition not yet checked is recorded `not_found` or `blocked` — never `verified`, never blank.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Every diligence workstream represented
- Every row carries a state, an evidence pointer, and an owner
- No row blank
- Rolled into `DD-027` before the gate

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

- **Required reviewer: `michigan_licensed_attorney`.** `legal_review_required: true` — every stage gate this artifact feeds is blocked until that review is recorded in `GOV-015` (professional-review tracker).
- This document is an *issue-spotting tool*. It does not contain legal advice and must not be treated as a substitute for counsel.
- Record the reviewer, the date, and the scope reviewed. A review with no recorded scope does not clear the gate.

## Dependencies

**Upstream — this cannot be completed without:**

- `DD-001` — Due-diligence plan and deadline calculator


**Stage gates this is required evidence for:** `SG-04`

## Typst issue version expected?

**Yes.** A paired Typst issue document is expected before this leaves the project. Base template: `publication/typst/templates/form-checklist.typ`.

Transfer reviewed content to the `.typ` deliberately — there is no automatic Markdown→Typst conversion. The Markdown draft and the Typst issue share this `artifact_id`; the Typst metadata records the draft path and its SHA-256.

Compilation is not approval. See `publication/README.md` for the issue gate.
