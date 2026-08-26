---
artifact_id: GOV-016
artifact_type: record
title: Stage-gate record
workstream: governance
service_code: ADM
status: template
template_version: "1.0"
parcel_ids: []
owner_role: contractor_program_manager
decision_role: company_decision_authority
required_reviewer_role: company_decision_authority
legal_review_required: false
typst_issue_required: true
typst_source: publication/typst/templates/stage-gate-package.typ
latest_issue_id: null
created_at: 2026-08-26
updated_at: 2026-08-26
source_as_of: null
source_ids: []
depends_on: [GOV-005]
supersedes: null
confidentiality: internal
---

# Stage-gate record

`GOV-016` · governance · service code `ADM`

> **Parcel-specific.** Create one copy per candidate parcel under `working/candidate-parcels/<parcel-id>/`. Do not complete this template in place.

## Purpose

The per-gate evidence record: what was required, what was present, what was blocked, what was decided, and who decided it.

## When to use it

At every stage gate.

## Required inputs

- `stage-gates.csv` row for the gate
- Each required evidence artifact
- `GOV-009` open blockers
- `GOV-015` review records

## Instructions

- Assemble the evidence before proposing a decision, not after.
- State each required artifact's condition using the controlled vocabulary. Absent is `blocked`, not blank.
- A conditional pass names the waived condition, the waiver authority, and the gate at which it must be closed.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Every required artifact is present or explicitly waived
- No condition is silently unknown
- Required professional reviews are recorded
- The Typst package compiled and was visually inspected

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Unresolved questions

_None recorded. Add any question that would change a decision if answered differently._

## Approvals and professional review

- **Required reviewer: `company_decision_authority`.** Record the review in `GOV-015` before this artifact is relied on at a gate.
- Conclusions reserved to that discipline must come from that professional, not from this document.

## Dependencies

**Upstream — this cannot be completed without:**

- `GOV-005` — Stage-gate register


## Typst issue version expected?

**Yes.** A paired Typst issue document is expected before this leaves the project. Base template: `publication/typst/templates/stage-gate-package.typ`.

Transfer reviewed content to the `.typ` deliberately — there is no automatic Markdown→Typst conversion. The Markdown draft and the Typst issue share this `artifact_id`; the Typst metadata records the draft path and its SHA-256.

Compilation is not approval. See `publication/README.md` for the issue gate.
