---
artifact_id: CLO-012
artifact_type: index
title: Compliance evidence index
workstream: closing-compliance
service_code: ADM
status: template
template_version: "1.0"
parcel_ids: []
owner_role: contractor_program_manager
decision_role: company_decision_authority
required_reviewer_role: michigan_licensed_attorney
legal_review_required: true
typst_issue_required: true
typst_source: publication/typst/templates/binder.typ
latest_issue_id: null
created_at: 2026-08-26
updated_at: 2026-08-26
source_as_of: 2026-08-26
source_ids: [SRC-007]
depends_on: [CON-019]
supersedes: null
confidentiality: internal
---

# Compliance evidence index

`CLO-012` · closing-compliance · service code `ADM`

> **Parcel-specific.** Create one copy per candidate parcel under `working/candidate-parcels/<parcel-id>/`. Do not complete this template in place.

## Purpose

Index of the evidence proving each continuing obligation has been met.

## When to use it

From closing until every obligation is discharged.

## Required inputs

- `CLO-011` obligation matrix
- Evidence artifacts

## Instructions

- Evidence is gathered as obligations are met, not reconstructed at the deadline.
- `SRC-007` shows the DLBA's evidence standard for structure sales is specific — dated photographs of all four sides, uploaded on a stated cadence, and it states the Compliance Team will not accept videos, receipts for small purchases, or written descriptions. Establish the standard that actually applies to this instrument rather than assuming.
- Index, do not archive twice. Point at where each evidence item lives.
- An unchecked condition is `not_found` or `blocked` — never `verified`, never blank.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Every obligation has indexed evidence
- Evidence meets the standard the instrument actually requires
- Gaps marked `blocked` with an owner

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Sources

Requirements in this artifact trace to the following rows in `source-register.csv`. Re-verify before relying on any of them — agency requirements change without notice.

| Source | Document | Status | Pinpoint |
| --- | --- | --- | --- |
| `SRC-007` | Compliance | `verified` | Post-sale timeline table (15/45/60 day milestones); evidence rules; Release of Interest |

## Unresolved questions

- What evidence standard applies to an Infill Housing Lot development agreement, as distinct from the structure-sale photo regime in `SRC-007`?

## Approvals and professional review

- **Required reviewer: `michigan_licensed_attorney`.** `legal_review_required: true` — every stage gate this artifact feeds is blocked until that review is recorded in `GOV-015` (professional-review tracker).
- This document is an *issue-spotting tool*. It does not contain legal advice and must not be treated as a substitute for counsel.
- Record the reviewer, the date, and the scope reviewed. A review with no recorded scope does not clear the gate.

## Dependencies

**Upstream — this cannot be completed without:**

- `CON-019` — Final-completion coordination checklist


**Stage gates this is required evidence for:** `SG-12`

## Typst issue version expected?

**Yes.** A paired Typst issue document is expected before this leaves the project. Base template: `publication/typst/templates/binder.typ`.

Transfer reviewed content to the `.typ` deliberately — there is no automatic Markdown→Typst conversion. The Markdown draft and the Typst issue share this `artifact_id`; the Typst metadata records the draft path and its SHA-256.

Compilation is not approval. See `publication/README.md` for the issue gate.
