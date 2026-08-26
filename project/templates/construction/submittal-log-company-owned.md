---
artifact_id: CON-012
artifact_type: received_record
title: Submittal log (Company-owned)
workstream: construction
service_code: INS
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
depends_on: [CON-003]
supersedes: null
confidentiality: internal
---

# Submittal log (Company-owned)

`CON-012` · construction · service code `INS`

> ### Company-owned record — received, not authored
>
> ICA §7.3: the Contractor does not supervise, direct, oversee, observe, monitor, or inspect construction, and is not the general contractor, superintendent, builder of record, or safety officer.
>
> This record is **the Company's**, produced by the Company's builder or subcontractors. It is registered here so that its **absence is visible at a stage gate**, and so it can be received, filed, and referenced.
>
> **Do not author it, populate it, or use it to evaluate the work.** Producing this record as Contractor work product is affirmative evidence of a duty the Agreement disclaims, and §7.4 relies on that duty not existing.

## Purpose

Contractor submittal log for materials and equipment.

## When to use it

On receipt from the Company or its builder.

## Required inputs

- The record as produced by the Company's builder or subcontractors

## Instructions

- Receive and file. Submittals are reviewed by the design professional the Company retains, not by the Contractor.
- Do not author, populate, or annotate with evaluative commentary. Filing a record is not reviewing it.
- If the record is not being produced, that is an issue for `GOV-009` and a gate blocker — raise it as a gap in the Company's records, not as work to be taken over.
- Reference it from `GOV-017` where its status affects schedule or budget reporting.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Record received and filed with a date and a source
- Absence escalated as a gap rather than filled
- No Contractor authorship or evaluation added

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

**No.** This artifact stays in Markdown. If it ever becomes an external submission, a stage-gate package, or a controlled-distribution PDF, update `typst_issue_required` in `artifact-register.csv` first — the register is the source of truth, not the file.
