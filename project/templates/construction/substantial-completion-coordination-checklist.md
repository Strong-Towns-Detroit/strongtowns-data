---
artifact_id: CON-018
artifact_type: checklist
title: Substantial-completion coordination checklist
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

# Substantial-completion coordination checklist

`CON-018` · construction · service code `INS`

> **Parcel-specific.** Create one copy per candidate parcel under `working/candidate-parcels/<parcel-id>/`. Do not complete this template in place.

## Purpose

Coordination checklist for substantial completion — limited to the permit and certificate-of-occupancy scope ICA Exhibit A assigns the Contractor.

## When to use it

As the project approaches substantial completion.

## Required inputs

- `APR-007` permit log
- `APR-005` approval conditions
- `APR-010` open corrections

## Instructions

- Scope this to permits, inspections and municipal sign-offs. Substantial completion of the **work** is a Company and design-professional determination; ICA §7.3 excludes the Contractor from evaluating the work.
- Confirm every permit is in a state that can proceed to final, and every correction notice is closed with the municipality (`APR-010`).
- Confirm every approval condition from `APR-005` is satisfied and evidenced.
- An unchecked condition is `not_found` or `blocked` — never `verified`, never blank.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Every permit ready to proceed to final
- Every correction notice closed with the municipality
- Every approval condition evidenced
- The permit-scope boundary respected

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

**Yes.** A paired Typst issue document is expected before this leaves the project. Base template: `publication/typst/templates/form-checklist.typ`.

Transfer reviewed content to the `.typ` deliberately — there is no automatic Markdown→Typst conversion. The Markdown draft and the Typst issue share this `artifact_id`; the Typst metadata records the draft path and its SHA-256.

Compilation is not approval. See `publication/README.md` for the issue gate.
