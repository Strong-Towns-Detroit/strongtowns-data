---
artifact_id: CLO-020
artifact_type: package
title: Certificate of occupancy closeout package
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
typst_source: publication/typst/templates/binder.typ
latest_issue_id: null
created_at: 2026-08-26
updated_at: 2026-08-26
source_as_of: null
source_ids: []
depends_on: [CON-019]
supersedes: null
confidentiality: internal
---

# Certificate of occupancy closeout package

`CLO-020` · closing-compliance · service code `INS`

> **Parcel-specific.** Create one copy per candidate parcel under `working/candidate-parcels/<parcel-id>/`. Do not complete this template in place.

## Purpose

The certificate-of-occupancy closeout package ICA §1.2 requires: final sign-offs, the CO, and a package of permits, approvals and approval conditions.

## When to use it

At final completion.

## Required inputs

- `CON-019` final completion
- `APR-007` permit log
- `APR-005` condition tracker
- `CLO-009` permit closeout

## Instructions

- §1.2 specifies the contents: final sign-offs, certificate of occupancy, and a closeout package of permits, approvals, and approval conditions. Assemble exactly that.
- Include conditions that continue past occupancy — they belong to `CLO-011`, and the package should say so rather than implying everything is closed.
- Issue as a Typst binder; record the manifest.
- An unchecked condition is `not_found` or `blocked` — never `verified`, never blank.

## Completion criteria

This artifact is complete when **all** of the following hold:

- All §1.2 contents present
- Continuing conditions identified and routed to `CLO-011`
- Typst binder compiled, inspected, and manifest validated
- Delivery recorded in `GOV-023`

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


**Stage gates this is required evidence for:** `SG-11`

## Typst issue version expected?

**Yes.** A paired Typst issue document is expected before this leaves the project. Base template: `publication/typst/templates/binder.typ`.

Transfer reviewed content to the `.typ` deliberately — there is no automatic Markdown→Typst conversion. The Markdown draft and the Typst issue share this `artifact_id`; the Typst metadata records the draft path and its SHA-256.

Compilation is not approval. See `publication/README.md` for the issue gate.
