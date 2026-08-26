---
artifact_id: GOV-017
artifact_type: report
title: Weekly status report
workstream: governance
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
depends_on: [GOV-009, CON-008]
supersedes: null
confidentiality: internal
---

# Weekly status report

`GOV-017` · governance · service code `ADM`

> **Reusable.** One copy project-wide, under `working/project-wide/`.

## Purpose

The weekly written status report and updated schedule required by ICA §1.2. This is a contractual deliverable with a fixed content list, not a discretionary summary.

## When to use it

Weekly, throughout the Term.

## Required inputs

- `CON-008` schedule status against baseline
- `CON-007` budget status and variance
- `APR-007` permit status and `APR-009`/`APR-010` inspection status
- `GOV-021` expenditures needing authorization
- `GOV-009` open issues
- `GOV-010` items awaiting Company decision

## Instructions

- Cover all six contractual headings every week, even when a heading is empty — write 'none this period' rather than omitting it. An omitted heading is indistinguishable from an overlooked one.
- Attach the updated schedule, not a description of it.
- List expenditures needing authorization with amounts, so the Company can authorise at the weekly meeting under §3.2.
- Items awaiting Company decision are the most consequential section; put them where they will be read.

## Completion criteria

This artifact is complete when **all** of the following hold:

- All six §1.2 headings present
- Updated schedule attached
- Every item awaiting Company decision states what decision is needed and by when
- Report issued within the agreed weekly cadence

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Unresolved questions

_None recorded. Add any question that would change a decision if answered differently._

## Approvals and professional review

- **Required reviewer: `company_decision_authority`.** Record the review in `GOV-015` before this artifact is relied on at a gate.
- Conclusions reserved to that discipline must come from that professional, not from this document.

## Dependencies

**Upstream — this cannot be completed without:**

- `GOV-009` — Risk and issue register
- `CON-008` — Schedule update and variance report


## Typst issue version expected?

**Yes.** A paired Typst issue document is expected before this leaves the project. Base template: `publication/typst/templates/report.typ`.

Transfer reviewed content to the `.typ` deliberately — there is no automatic Markdown→Typst conversion. The Markdown draft and the Typst issue share this `artifact_id`; the Typst metadata records the draft path and its SHA-256.

Compilation is not approval. See `publication/README.md` for the issue gate.
