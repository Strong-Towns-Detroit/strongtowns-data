---
artifact_id: DD-007
artifact_type: checklist
title: Survey RFP and review checklist
workstream: due-diligence
service_code: LND
status: template
template_version: "1.0"
parcel_ids: []
owner_role: contractor_program_manager
decision_role: company_decision_authority
required_reviewer_role: licensed_surveyor
legal_review_required: false
typst_issue_required: true
typst_source: publication/typst/templates/rfp.typ
latest_issue_id: null
created_at: 2026-08-26
updated_at: 2026-08-26
source_as_of: null
source_ids: []
depends_on: [DD-001]
supersedes: null
confidentiality: internal
---

# Survey RFP and review checklist

`DD-007` · due-diligence · service code `LND`

> **Parcel-specific.** Create one copy per candidate parcel under `working/candidate-parcels/<parcel-id>/`. Do not complete this template in place.

## Purpose

Scopes and reviews the boundary survey. The survey is what converts an assumed buildable envelope into a real one.

## When to use it

Once title exceptions are known, so the survey can be scoped to plot them.

## Required inputs

- `DD-004` exception register
- `ACQ-006` legal descriptions
- `SCR-006` provisional envelope

## Instructions

- Scope the survey to plot the recorded easements from `DD-004`. A survey that does not show them cannot answer the question you are asking.
- Require the surveyor to address encroachments in both directions, and access.
- Until a survey exists, every buildable-envelope conclusion is provisional and must say so.
- Any conclusion reserved to a licensed discipline comes from that professional, not from this artifact.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Scope covers boundary, easements, encroachments and access
- Survey obtained and read against `DD-004`
- `SCR-006` envelope updated from survey rather than assumption
- Surveyor review recorded in `GOV-015`

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Sources

_No external requirements cited. If this artifact starts asserting one, add a row to `source-register.csv` first._

## Unresolved questions

_None recorded. Add any question that would change a decision if answered differently._

## Approvals and professional review

- **Required reviewer: `licensed_surveyor`.** Record the review in `GOV-015` before this artifact is relied on at a gate.
- Conclusions reserved to that discipline must come from that professional, not from this document.

## Dependencies

**Upstream — this cannot be completed without:**

- `DD-001` — Due-diligence plan and deadline calculator


## Typst issue version expected?

**Yes.** A paired Typst issue document is expected before this leaves the project. Base template: `publication/typst/templates/rfp.typ`.

Transfer reviewed content to the `.typ` deliberately — there is no automatic Markdown→Typst conversion. The Markdown draft and the Typst issue share this `artifact_id`; the Typst metadata records the draft path and its SHA-256.

Compilation is not approval. See `publication/README.md` for the issue gate.
