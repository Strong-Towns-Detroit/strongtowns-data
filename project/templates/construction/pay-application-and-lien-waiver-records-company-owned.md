---
artifact_id: CON-014
artifact_type: received_record
title: Pay-application and lien-waiver records (Company-owned)
workstream: construction
service_code: INS
status: template
template_version: "1.0"
parcel_ids: []
owner_role: contractor_program_manager
decision_role: company_decision_authority
required_reviewer_role: michigan_licensed_attorney
legal_review_required: true
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

# Pay-application and lien-waiver records (Company-owned)

`CON-014` · construction · service code `INS`

> ### Company-owned record — received, not authored
>
> ICA §7.3: the Contractor does not supervise, direct, oversee, observe, monitor, or inspect construction, and is not the general contractor, superintendent, builder of record, or safety officer.
>
> This record is **the Company's**, produced by the Company's builder or subcontractors. It is registered here so that its **absence is visible at a stage gate**, and so it can be received, filed, and referenced.
>
> **Do not author it, populate it, or use it to evaluate the work.** Producing this record as Contractor work product is affirmative evidence of a duty the Agreement disclaims, and §7.4 relies on that duty not existing.

## Purpose

Payment applications and lien waivers.

## When to use it

On receipt from the Company or its builder.

## Required inputs

- The record as produced by the Company's builder or subcontractors

## Instructions

- Receive and file. Payment certification and lien-waiver adequacy are Company and counsel determinations. ICA §7.4 expressly disclaims Contractor liability for mechanics' liens and construction payment disputes.
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

- **Required reviewer: `michigan_licensed_attorney`.** `legal_review_required: true` — every stage gate this artifact feeds is blocked until that review is recorded in `GOV-015` (professional-review tracker).
- This document is an *issue-spotting tool*. It does not contain legal advice and must not be treated as a substitute for counsel.
- Record the reviewer, the date, and the scope reviewed. A review with no recorded scope does not clear the gate.

## Dependencies

**Upstream — this cannot be completed without:**

- `CON-003` — Baseline schedule


**Stage gates this is required evidence for:** `SG-10`

## Typst issue version expected?

**No.** This artifact stays in Markdown. If it ever becomes an external submission, a stage-gate package, or a controlled-distribution PDF, update `typst_issue_required` in `artifact-register.csv` first — the register is the source of truth, not the file.
