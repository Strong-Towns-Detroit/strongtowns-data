---
artifact_id: APR-011
artifact_type: letter
title: Agency correspondence
workstream: approvals
service_code: PMT
status: template
template_version: "1.0"
parcel_ids: []
owner_role: contractor_program_manager
decision_role: company_decision_authority
required_reviewer_role: company_decision_authority
legal_review_required: false
typst_issue_required: true
typst_source: publication/typst/templates/letter.typ
latest_issue_id: null
created_at: 2026-08-26
updated_at: 2026-08-26
source_as_of: null
source_ids: []
depends_on: [APR-001]
supersedes: null
confidentiality: internal
---

# Agency correspondence

`APR-011` · approvals · service code `PMT`

> **Parcel-specific.** Create one copy per candidate parcel under `working/candidate-parcels/<parcel-id>/`. Do not complete this template in place.

## Purpose

Correspondence to an agency or authority, issued as a controlled letter.

## When to use it

Whenever a written position must go to an authority.

## Required inputs

- `GOV-013` correspondence log
- The matter at hand

## Instructions

- Written correspondence to an authority creates a record that will be read back later. Say what is true and no more.
- Log every letter in `GOV-013` and retain a copy as sent.
- Issue via the Typst letter template so version and status are unambiguous.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Content reviewed before issue
- Logged in `GOV-013`
- Copy retained as sent
- Typst issue compiled and visually inspected

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

- `APR-001` — Permit and approval matrix


## Typst issue version expected?

**Yes.** A paired Typst issue document is expected before this leaves the project. Base template: `publication/typst/templates/letter.typ`.

Transfer reviewed content to the `.typ` deliberately — there is no automatic Markdown→Typst conversion. The Markdown draft and the Typst issue share this `artifact_id`; the Typst metadata records the draft path and its SHA-256.

Compilation is not approval. See `publication/README.md` for the issue gate.
