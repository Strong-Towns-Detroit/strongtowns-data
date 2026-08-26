---
artifact_id: CLO-018
artifact_type: index
title: Final archive index
workstream: closing-compliance
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
depends_on: [CON-019]
supersedes: null
confidentiality: internal
---

# Final archive index

`CLO-018` · closing-compliance · service code `ADM`

> **Parcel-specific.** Create one copy per candidate parcel under `working/candidate-parcels/<parcel-id>/`. Do not complete this template in place.

## Purpose

Index of the final project archive.

## When to use it

At project close, and at termination under ICA §9.3.

## Required inputs

- Every project artifact
- `GOV-023` Work Product delivery register

## Instructions

- ICA §5.4 requires Work Product delivery in native editable format on request and at end of Term; §9.3 requires it on termination together with return of any Company card or account access.
- Index what exists and where. Deliver natives, not exports — a PDF is not delivery under §5.4.
- Confirm nothing sensitive has leaked into tracked files before archiving.
- An unchecked condition is `not_found` or `blocked` — never `verified`, never blank.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Every artifact indexed with its location
- Native-format delivery recorded in `GOV-023`
- Company property returned and evidenced
- No sensitive data in tracked files

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

- `CON-019` — Final-completion coordination checklist


**Stage gates this is required evidence for:** `SG-12`

## Typst issue version expected?

**No.** This artifact stays in Markdown. If it ever becomes an external submission, a stage-gate package, or a controlled-distribution PDF, update `typst_issue_required` in `artifact-register.csv` first — the register is the source of truth, not the file.
