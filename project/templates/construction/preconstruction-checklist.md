---
artifact_id: CON-001
artifact_type: checklist
title: Preconstruction checklist
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
typst_source: publication/typst/templates/form-checklist.typ
latest_issue_id: null
created_at: 2026-08-26
updated_at: 2026-08-26
source_as_of: null
source_ids: []
depends_on: [PRO-002]
supersedes: null
confidentiality: internal
---

# Preconstruction checklist

`CON-001` · construction · service code `EST`

> **Parcel-specific.** Create one copy per candidate parcel under `working/candidate-parcels/<parcel-id>/`. Do not complete this template in place.

## Purpose

Preconstruction checklist: everything that must be true before work starts on site.

## When to use it

Before notice to proceed.

## Required inputs

- `APR-007` permit log
- `FIN-010` insurance matrix
- `CON-002` baseline budget
- `CON-003` baseline schedule

## Instructions

- Permits issued, not applied for. `APR-007` status must read issued for every permit needed to start.
- Insurance effective dates must precede the exposure, per `FIN-010`. Builder's risk before materials arrive.
- Baseline budget and schedule fixed and approved — after work starts, a baseline is a negotiation rather than a measurement.
- Utility connections confirmed or their absence explicitly accepted as a risk (`APR-003`).
- ICA §7.2 makes the Company solely responsible for construction means, methods, sequencing, workmanship, field code compliance, and job site safety. Nothing here changes that.
- An unchecked condition is `not_found` or `blocked` — never `verified`, never blank.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Every required permit issued
- Insurance in force with dates preceding exposure
- Baseline budget and schedule approved and frozen
- Nothing marked ready without evidence

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

- `PRO-002` — Builder and general-contractor RFP


**Stage gates this is required evidence for:** `SG-09`

## Typst issue version expected?

**Yes.** A paired Typst issue document is expected before this leaves the project. Base template: `publication/typst/templates/form-checklist.typ`.

Transfer reviewed content to the `.typ` deliberately — there is no automatic Markdown→Typst conversion. The Markdown draft and the Typst issue share this `artifact_id`; the Typst metadata records the draft path and its SHA-256.

Compilation is not approval. See `publication/README.md` for the issue gate.
