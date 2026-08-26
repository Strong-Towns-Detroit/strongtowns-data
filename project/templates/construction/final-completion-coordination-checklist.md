---
artifact_id: CON-019
artifact_type: checklist
title: Final-completion coordination checklist
workstream: construction
service_code: INS
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
depends_on: [CON-003]
supersedes: null
confidentiality: internal
---

# Final-completion coordination checklist

`CON-019` · construction · service code `INS`

> **Parcel-specific.** Create one copy per candidate parcel under `working/candidate-parcels/<parcel-id>/`. Do not complete this template in place.

## Purpose

Coordination checklist for final completion and certificate of occupancy. ICA §1.2 makes obtaining final sign-offs and the CO a Contractor deliverable.

## When to use it

At project completion.

## Required inputs

- `CON-018`
- `APR-007` permit log
- Final inspection results

## Instructions

- Obtaining final sign-offs and the certificate of occupancy is an explicit §1.2 deliverable. Drive it to closure.
- Confirm every trade's final inspection has passed and been recorded in the municipal system.
- Assemble the closeout package §1.2 requires: permits, approvals, and approval conditions.
- An unchecked condition is `not_found` or `blocked` — never `verified`, never blank.

## Completion criteria

This artifact is complete when **all** of the following hold:

- All final inspections passed and recorded
- Certificate of occupancy obtained
- Closeout package assembled per §1.2

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

**Downstream — these depend on this:**

- `CLO-009` — Permit closeout and occupancy checklist
- `CLO-010` — Utility transfer checklist
- `CLO-011` — Seller and agency obligation matrix
- `CLO-012` — Compliance evidence index
- `CLO-013` — Milestone calendar
- `CLO-014` — Inspection and photo evidence log
- `CLO-015` — Extension and waiver request
- `CLO-016` — Restriction and reverter calendar
- `CLO-017` — Warranty and maintenance handoff
- `CLO-018` — Final archive index
- _…and 2 more (see `dependency-register.csv`)_

**Stage gates this is required evidence for:** `SG-11`

## Typst issue version expected?

**Yes.** A paired Typst issue document is expected before this leaves the project. Base template: `publication/typst/templates/form-checklist.typ`.

Transfer reviewed content to the `.typ` deliberately — there is no automatic Markdown→Typst conversion. The Markdown draft and the Typst issue share this `artifact_id`; the Typst metadata records the draft path and its SHA-256.

Compilation is not approval. See `publication/README.md` for the issue gate.
