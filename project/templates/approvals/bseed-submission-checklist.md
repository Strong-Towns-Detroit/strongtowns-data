---
artifact_id: APR-002
artifact_type: checklist
title: BSEED submission checklist
workstream: approvals
service_code: PMT
status: template
template_version: "1.0"
parcel_ids: []
owner_role: contractor_program_manager
decision_role: company_decision_authority
required_reviewer_role: licensed_architect_or_engineer
legal_review_required: false
typst_issue_required: true
typst_source: publication/typst/templates/form-checklist.typ
latest_issue_id: null
created_at: 2026-08-26
updated_at: 2026-08-26
source_as_of: 2026-08-26
source_ids: [SRC-017, SRC-018, SRC-015]
depends_on: [APR-001]
supersedes: null
confidentiality: internal
---

# BSEED submission checklist

`APR-002` · approvals · service code `PMT`

> **Parcel-specific.** Create one copy per candidate parcel under `working/candidate-parcels/<parcel-id>/`. Do not complete this template in place.

## Purpose

Checklist for a complete BSEED residential plan submission.

## When to use it

Immediately before submitting to plan review.

## Required inputs

- `SRC-017` residential plan submittal checklist
- `SRC-018` fee schedule
- Complete drawing set
- `DSN-014` sealed drawings

## Instructions

- Work `SRC-017` section by section: Plot Plan, Foundation, Floor Plans, Elevations, Framing, Electrical, Mechanical, Details and General Notes.
- Confirm the submittal quantities: three complete plan sets drawn to scale, one set of calculations, one set of specifications, plus a completed Building Permit Application.
- Confirm sealed items are actually sealed — truss calculations, and engineered design for masonry and concrete basement walls.
- Include the State of Michigan Energy Code Compliance worksheet for new construction.
- **`SRC-017` is dated 2013-06.** Verify the current requirement set with the Development Resource Center (313-224-2372) before submitting. Do not treat a thirteen-year-old checklist as current.
- Fees: a deposit is due at log-in with the balance at permit issuance (`SRC-017`); amounts per `SRC-018`.
- Submission is via an eLAPS account then ePlans upload (`SRC-015`).
- An unchecked condition is `not_found` or `blocked` — never `verified`, never blank.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Every `SRC-017` section addressed
- Submittal quantities confirmed
- Sealed items sealed by a Michigan-licensed professional
- Energy Code Compliance worksheet included
- Current requirement set confirmed with BSEED, not assumed from the 2013 checklist

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Sources

Requirements in this artifact trace to the following rows in `source-register.csv`. Re-verify before relying on any of them — agency requirements change without notice.

| Source | Document | Status | Pinpoint |
| --- | --- | --- | --- |
| `SRC-017` | Residential Building Permit/Plan Submittal Checklist | `verified` | Preamble (submittal quantities, sealed-drawing statement, fee deposit); Plot Plan; Foundation Plans; Floor Plans; Elevations; Framing Plans; Electrical; Mechanical; Details and General Notes |
| `SRC-018` | Fee Schedule (BSEED) | `verified` | Filename carries effective and modification dates; line items not yet abstracted |
| `SRC-015` | BSEED Plan Review | `verified` | Codes enforced; ePlans/eLAPS process steps; coordinating departments |

## Unresolved questions

- What is the current residential submittal requirement set, and has the 2013-06 checklist been superseded?

## Approvals and professional review

- **Required reviewer: `licensed_architect_or_engineer`.** Record the review in `GOV-015` before this artifact is relied on at a gate.
- Conclusions reserved to that discipline must come from that professional, not from this document.

## Dependencies

**Upstream — this cannot be completed without:**

- `APR-001` — Permit and approval matrix


**Stage gates this is required evidence for:** `SG-07`

## Typst issue version expected?

**Yes.** A paired Typst issue document is expected before this leaves the project. Base template: `publication/typst/templates/form-checklist.typ`.

Transfer reviewed content to the `.typ` deliberately — there is no automatic Markdown→Typst conversion. The Markdown draft and the Typst issue share this `artifact_id`; the Typst metadata records the draft path and its SHA-256.

Compilation is not approval. See `publication/README.md` for the issue gate.
