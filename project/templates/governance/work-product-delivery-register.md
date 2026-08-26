---
artifact_id: GOV-023
artifact_type: register
title: Work Product delivery register
workstream: governance
service_code: ADM
status: template
template_version: "1.0"
parcel_ids: []
owner_role: contractor_program_manager
decision_role: company_decision_authority
required_reviewer_role: company_decision_authority
legal_review_required: false
typst_issue_required: false
typst_source: null
latest_issue_id: null
created_at: 2026-08-26
updated_at: 2026-08-26
source_as_of: null
source_ids: []
depends_on: []
supersedes: null
confidentiality: internal
---

# Work Product delivery register

`GOV-023` · governance · service code `ADM`

> **Reusable.** One copy project-wide, under `working/project-wide/`.

## Purpose

Tracks Work Product delivery in native editable format, required by ICA §5.4 on request and at the end of the Term.

## When to use it

On every delivery, and as a complete sweep at termination (§9.3).

## Required inputs

- Design files, permit filings, estimates, schedules, analyses, reports

## Instructions

- Record what was delivered, in what format, on what date, and to whom.
- Native editable format means the working file, not an export. A PDF is not delivery under §5.4.
- At termination, §9.3 also requires returning any Company card or account access with outstanding receipts — track that here alongside Work Product.
- Note that §5.5 ends Contractor responsibility for anything modified after delivery; a clean delivery record is what makes that boundary provable.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Every deliverable named in §1.2 has a delivery record
- Native-format delivery is distinguished from PDF issue
- At termination, Company property returned and recorded

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Unresolved questions

_None recorded. Add any question that would change a decision if answered differently._

## Approvals and professional review

- **Required reviewer: `company_decision_authority`.** Record the review in `GOV-015` before this artifact is relied on at a gate.
- Conclusions reserved to that discipline must come from that professional, not from this document.

## Dependencies

**Upstream:** none. This is an entry point.


## Typst issue version expected?

**No.** This artifact stays in Markdown. If it ever becomes an external submission, a stage-gate package, or a controlled-distribution PDF, update `typst_issue_required` in `artifact-register.csv` first — the register is the source of truth, not the file.
