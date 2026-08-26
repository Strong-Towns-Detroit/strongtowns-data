---
artifact_id: PRO-009
artifact_type: handoff
title: Professional agreement review handoff
workstream: procurement
service_code: ADM
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
source_as_of: null
source_ids: []
depends_on: [DSN-012]
supersedes: null
confidentiality: internal
---

# Professional agreement review handoff

`PRO-009` · procurement · service code `ADM`

> **Parcel-specific.** Create one copy per candidate parcel under `working/candidate-parcels/<parcel-id>/`. Do not complete this template in place.

## Purpose

Handoff package instructing counsel on a professional or construction agreement.

## When to use it

Before counsel reviews any agreement.

## Required inputs

- `PRO-008` issue checklist
- The draft agreement
- Relevant bid documents

## Instructions

- State the questions; do not argue the answers.
- Flag the ICA §7 allocation explicitly so counsel understands the Contractor's position: the Company controls construction, and the Contractor neither supervises nor bears construction liability.
- Attach the actual instrument.
- Record the returned review in `GOV-015`, scoped to the version reviewed.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Every question answerable as asked
- ICA §7 allocation flagged
- Instrument attached in original form
- Review recorded

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

- `DSN-012` — Design deliverables register


## Typst issue version expected?

**Yes.** A paired Typst issue document is expected before this leaves the project. Base template: `publication/typst/templates/professional-handoff.typ`.

Transfer reviewed content to the `.typ` deliberately — there is no automatic Markdown→Typst conversion. The Markdown draft and the Typst issue share this `artifact_id`; the Typst metadata records the draft path and its SHA-256.

Compilation is not approval. See `publication/README.md` for the issue gate.
