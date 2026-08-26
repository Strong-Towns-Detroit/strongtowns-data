---
artifact_id: PRO-002
artifact_type: rfp
title: Builder and general-contractor RFP
workstream: procurement
service_code: EST
status: template
template_version: "1.0"
parcel_ids: []
owner_role: contractor_program_manager
decision_role: company_decision_authority
required_reviewer_role: company_decision_authority
legal_review_required: false
typst_issue_required: true
typst_source: publication/typst/templates/rfp.typ
latest_issue_id: null
created_at: 2026-08-26
updated_at: 2026-08-26
source_as_of: null
source_ids: []
depends_on: [DSN-012]
supersedes: null
confidentiality: internal
---

# Builder and general-contractor RFP

`PRO-002` · procurement · service code `EST`

> **Parcel-specific.** Create one copy per candidate parcel under `working/candidate-parcels/<parcel-id>/`. Do not complete this template in place.

## Purpose

RFP for a builder or general contractor.

## When to use it

Once construction documents are permit-ready or near it.

## Required inputs

- Construction documents
- `FIN-001` cost plan
- `CON-003` baseline schedule

## Instructions

- ICA §7.2 makes the Company solely responsible for selecting, engaging, directing and paying builders. The Contractor solicits and levels bids (Exhibit A); the Company contracts.
- State the scope boundary precisely — what is in the base bid, what is an allowance, what is by others. Scope gaps become change orders.
- Require a schedule with the bid, not just a price. A price without a schedule is half a proposal.
- State the required licensure and insurance up front, per `FIN-010`.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Base bid, allowances and by-others clearly separated
- Schedule required with the bid
- Licensure and insurance stated
- The solicit-versus-contract boundary respected
- Typst RFP compiled and visually inspected

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

- `DSN-012` — Design deliverables register

**Downstream — these depend on this:**

- `CON-001` — Preconstruction checklist
- `CON-002` — Baseline budget
- `CON-003` — Baseline schedule

## Typst issue version expected?

**Yes.** A paired Typst issue document is expected before this leaves the project. Base template: `publication/typst/templates/rfp.typ`.

Transfer reviewed content to the `.typ` deliberately — there is no automatic Markdown→Typst conversion. The Markdown draft and the Typst issue share this `artifact_id`; the Typst metadata records the draft path and its SHA-256.

Compilation is not approval. See `publication/README.md` for the issue gate.
