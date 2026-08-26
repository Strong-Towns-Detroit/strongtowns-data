---
artifact_id: CON-010
artifact_type: review
title: Constructability and value-engineering review
workstream: construction
service_code: EST
status: template
template_version: "1.0"
parcel_ids: []
owner_role: contractor_program_manager
decision_role: company_decision_authority
required_reviewer_role: company_decision_authority
legal_review_required: false
typst_issue_required: true
typst_source: publication/typst/templates/report.typ
latest_issue_id: null
created_at: 2026-08-26
updated_at: 2026-08-26
source_as_of: null
source_ids: []
depends_on: [CON-003]
supersedes: null
confidentiality: internal
---

# Constructability and value-engineering review

`CON-010` · construction · service code `EST`

> **Parcel-specific.** Create one copy per candidate parcel under `working/candidate-parcels/<parcel-id>/`. Do not complete this template in place.

## Purpose

Constructability and value-engineering review. ICA Exhibit A requires this be performed before permit submission.

## When to use it

Before permit submission — after it, the findings cost money to act on.

## Required inputs

- Construction documents
- `DD-023` site logistics review
- `FIN-001` cost plan

## Instructions

- Exhibit A places this before permit submission specifically. A constructability finding after permit issue means a resubmittal.
- Separate constructability problems (it cannot be built as drawn) from value engineering (it can be built cheaper). They have different urgency and different decision-makers.
- Price every VE option with its consequence, including consequences for quality and for the finished-value estimate. VE that reduces value is not a saving.
- Recommend; the Company decides. Record both in `GOV-007`.
- Every figure states its basis and confidence.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Review completed before permit submission
- Constructability and VE findings separated
- Every VE option priced with its consequence
- Recommendation and Company decision recorded separately

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Sources

_No external requirements cited. If this artifact starts asserting one, add a row to `source-register.csv` first._

## Unresolved questions

_None recorded. Add any question that would change a decision if answered differently._

## Approvals and professional review

- **Required reviewer: `company_decision_authority`.** Record the review in `GOV-015` before this artifact is relied on at a gate.
- Conclusions reserved to that discipline must come from that professional, not from this document.

## Dependencies

**Upstream — this cannot be completed without:**

- `CON-003` — Baseline schedule


## Typst issue version expected?

**Yes.** A paired Typst issue document is expected before this leaves the project. Base template: `publication/typst/templates/report.typ`.

Transfer reviewed content to the `.typ` deliberately — there is no automatic Markdown→Typst conversion. The Markdown draft and the Typst issue share this `artifact_id`; the Typst metadata records the draft path and its SHA-256.

Compilation is not approval. See `publication/README.md` for the issue gate.
