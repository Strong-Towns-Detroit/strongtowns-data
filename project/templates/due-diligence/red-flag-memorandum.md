---
artifact_id: DD-026
artifact_type: memo
title: Red-flag memorandum
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
typst_source: publication/typst/templates/report.typ
latest_issue_id: null
created_at: 2026-08-26
updated_at: 2026-08-26
source_as_of: null
source_ids: []
depends_on: [DD-001]
supersedes: null
confidentiality: internal
---

# Red-flag memorandum

`DD-026` · due-diligence · service code `LND`

> **Parcel-specific.** Create one copy per candidate parcel under `working/candidate-parcels/<parcel-id>/`. Do not complete this template in place.

## Purpose

The red-flag memorandum: what was found that could kill the deal, change the price, or change the design. Written to be read by a decision-maker in five minutes.

## When to use it

Once diligence is substantially complete, before the go/no-go.

## Required inputs

- Every DD-series finding
- `DD-002` integrated checklist
- `GOV-009` risk register

## Instructions

- Lead with the flags, not the method. A reader who stops after the first page should still know the worst of it.
- Every flag states its consequence in cost, schedule, or feasibility terms, with a confidence.
- Unresolved conditions are flags. A condition that could not be established is reported as such, not omitted.
- Issue as a Typst report; counsel review recorded in `GOV-015` before it drives a decision.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Every material finding represented
- Consequences quantified with a basis and confidence
- Unresolved conditions reported as unresolved
- Counsel review recorded
- Typst issue compiled and visually inspected

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Sources

_No external requirements cited. If this artifact starts asserting one, add a row to `source-register.csv` first._

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

**Yes.** A paired Typst issue document is expected before this leaves the project. Base template: `publication/typst/templates/report.typ`.

Transfer reviewed content to the `.typ` deliberately — there is no automatic Markdown→Typst conversion. The Markdown draft and the Typst issue share this `artifact_id`; the Typst metadata records the draft path and its SHA-256.

Compilation is not approval. See `publication/README.md` for the issue gate.
