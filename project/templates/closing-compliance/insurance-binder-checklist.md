---
artifact_id: CLO-008
artifact_type: checklist
title: Insurance binder checklist
workstream: closing-compliance
service_code: ADM
status: template
template_version: "1.0"
parcel_ids: []
owner_role: contractor_program_manager
decision_role: company_decision_authority
required_reviewer_role: licensed_insurance_agent
legal_review_required: false
typst_issue_required: true
typst_source: publication/typst/templates/form-checklist.typ
latest_issue_id: null
created_at: 2026-08-26
updated_at: 2026-08-26
source_as_of: null
source_ids: []
depends_on: [ACQ-023]
supersedes: null
confidentiality: internal
---

# Insurance binder checklist

`CLO-008` · closing-compliance · service code `ADM`

> **Parcel-specific.** Create one copy per candidate parcel under `working/candidate-parcels/<parcel-id>/`. Do not complete this template in place.

## Purpose

Checklist for the insurance binder at and after closing.

## When to use it

Before closing and at each coverage transition.

## Required inputs

- `FIN-010` insurance matrix
- Binders and certificates

## Instructions

- Coverage must be in force at closing, not applied for. Vacant land, course-of-construction and completed-value coverage are different products with different trigger dates.
- Calendar every certificate expiry. An expired certificate mid-construction is an uninsured project.
- An unchecked condition is `not_found` or `blocked` — never `verified`, never blank.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Coverage in force at closing with evidence
- Transitions between coverage types planned
- Expiries calendared

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Sources

_No external requirements cited. If this artifact starts asserting one, add a row to `source-register.csv` first._

## Unresolved questions

_None recorded. Add any question that would change a decision if answered differently._

## Approvals and professional review

- **Required reviewer: `licensed_insurance_agent`.** Record the review in `GOV-015` before this artifact is relied on at a gate.
- Conclusions reserved to that discipline must come from that professional, not from this document.

## Dependencies

**Upstream — this cannot be completed without:**

- `ACQ-023` — Closing-conditions checklist


## Typst issue version expected?

**Yes.** A paired Typst issue document is expected before this leaves the project. Base template: `publication/typst/templates/form-checklist.typ`.

Transfer reviewed content to the `.typ` deliberately — there is no automatic Markdown→Typst conversion. The Markdown draft and the Typst issue share this `artifact_id`; the Typst metadata records the draft path and its SHA-256.

Compilation is not approval. See `publication/README.md` for the issue gate.
