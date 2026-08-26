---
artifact_id: CON-009
artifact_type: report
title: Weekly progress report
workstream: construction
service_code: ADM
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

# Weekly progress report

`CON-009` · construction · service code `ADM`

> **Parcel-specific.** Create one copy per candidate parcel under `working/candidate-parcels/<parcel-id>/`. Do not complete this template in place.

## Purpose

The weekly written status report and updated schedule required by ICA §1.2 — the construction-phase instance of `GOV-017`.

## When to use it

Weekly throughout construction.

## Required inputs

- `CON-008` schedule status
- `CON-007` budget status
- `APR-007` permit status
- `APR-009`/`APR-010` inspection status
- `GOV-021` authorizations needed
- `GOV-009` open issues
- `GOV-010` items awaiting decision

## Instructions

- Cover all six §1.2 headings every week, even when a heading is empty. Write 'none this period' — an omitted heading is indistinguishable from an overlooked one.
- Attach the updated schedule itself, not a description of it.
- Put items awaiting Company decision where they will actually be read. They are the most consequential section and the reason the report exists.
- List expenditures needing authorization with amounts so the Company can authorise at the weekly meeting under §3.2.
- Issue as a Typst report where it is a controlled distribution.

## Completion criteria

This artifact is complete when **all** of the following hold:

- All six §1.2 headings present
- Updated schedule attached
- Every item awaiting decision states what is needed and by when
- Issued within the weekly cadence

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
