---
artifact_id: PRO-001
artifact_type: rfp
title: Architect and consultant RFP
workstream: procurement
service_code: DSN
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

# Architect and consultant RFP

`PRO-001` · procurement · service code `DSN`

> **Parcel-specific.** Create one copy per candidate parcel under `working/candidate-parcels/<parcel-id>/`. Do not complete this template in place.

## Purpose

RFP for architectural or consultant services.

## When to use it

Once `DSN-006` establishes what scope must be procured.

## Required inputs

- `DSN-006` consultant scope matrix
- `DSN-014` sealed-drawing triggers
- `DSN-001` program

## Instructions

- Scope from `DSN-006`. An RFP that does not state the scope boundary produces proposals that cannot be compared.
- Where a sealed drawing is required (`DSN-014`), say so explicitly and require evidence of Michigan licensure.
- Name a single point of contact and state the contact restriction. Side conversations during a solicitation are how procurement gets challenged.
- State the evaluation criteria and weights. Proposers allocate effort to what is scored.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Scope boundary unambiguous
- Licensure requirements stated where seals are needed
- Single point of contact named
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


## Typst issue version expected?

**Yes.** A paired Typst issue document is expected before this leaves the project. Base template: `publication/typst/templates/rfp.typ`.

Transfer reviewed content to the `.typ` deliberately — there is no automatic Markdown→Typst conversion. The Markdown draft and the Typst issue share this `artifact_id`; the Typst metadata records the draft path and its SHA-256.

Compilation is not approval. See `publication/README.md` for the issue gate.
