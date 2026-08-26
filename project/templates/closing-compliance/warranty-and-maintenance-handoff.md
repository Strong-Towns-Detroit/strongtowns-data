---
artifact_id: CLO-017
artifact_type: handoff
title: Warranty and maintenance handoff
workstream: closing-compliance
service_code: INS
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
depends_on: [CON-019]
supersedes: null
confidentiality: internal
---

# Warranty and maintenance handoff

`CLO-017` · closing-compliance · service code `INS`

> **Parcel-specific.** Create one copy per candidate parcel under `working/candidate-parcels/<parcel-id>/`. Do not complete this template in place.

## Purpose

Handoff of warranties and maintenance obligations to the Company or occupant.

## When to use it

At completion.

## Required inputs

- `CON-020` warranty register
- O&M manuals

## Instructions

- Hand off with start dates and claim routes, not just documents. A warranty nobody knows how to claim is not a warranty.
- ICA §7.4 disclaims Contractor liability for warranty claims from any purchaser, occupant or lender. The handoff transfers the documents and the knowledge, not a duty.
- An unchecked condition is `not_found` or `blocked` — never `verified`, never blank.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Every warranty handed off with start date and claim route
- Handoff acknowledged and dated
- No Contractor warranty obligation implied

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


## Typst issue version expected?

**Yes.** A paired Typst issue document is expected before this leaves the project. Base template: `publication/typst/templates/report.typ`.

Transfer reviewed content to the `.typ` deliberately — there is no automatic Markdown→Typst conversion. The Markdown draft and the Typst issue share this `artifact_id`; the Typst metadata records the draft path and its SHA-256.

Compilation is not approval. See `publication/README.md` for the issue gate.
