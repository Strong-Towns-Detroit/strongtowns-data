---
artifact_id: DSN-009
artifact_type: analysis
title: Preliminary code analysis
workstream: design-feasibility
service_code: DSN
status: template
template_version: "1.0"
parcel_ids: []
owner_role: contractor_program_manager
decision_role: company_decision_authority
required_reviewer_role: licensed_architect_or_engineer
legal_review_required: false
typst_issue_required: true
typst_source: publication/typst/templates/report.typ
latest_issue_id: null
created_at: 2026-08-26
updated_at: 2026-08-26
source_as_of: 2026-08-26
source_ids: [SRC-015, SRC-017]
depends_on: [SCR-003]
supersedes: null
confidentiality: internal
---

# Preliminary code analysis

`DSN-009` · design-feasibility · service code `DSN`

> **Parcel-specific.** Create one copy per candidate parcel under `working/candidate-parcels/<parcel-id>/`. Do not complete this template in place.

## Purpose

Preliminary code analysis: occupancy, construction type, egress, fire separation, energy — the constraints that shape the design before it is drawn.

## When to use it

Before design development.

## Required inputs

- `SRC-015` codes enforced
- `SRC-017` submittal checklist
- Concept drawings

## Instructions

- Work from `SRC-015`: Detroit enforces the Detroit Zoning Ordinance, Michigan Building Code, Michigan Residential Code, Michigan Rehabilitation Code, and the Michigan Electrical, Mechanical and Plumbing Codes plus the International Fuel Gas Code.
- Pull the concrete requirements `SRC-017` already states — egress window sill height, window well dimensions, garage/house fire separation, attic and crawl access, stair and guard dimensions, attic ventilation, safety glazing.
- Note that `SRC-017` is dated 2013-06. Verify every requirement against the current code edition rather than treating the checklist as current.
- Conclusions reserved to a licensed discipline come from that professional, not from this artifact.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Occupancy and construction type established
- Egress, separation and ventilation requirements identified
- Every requirement verified against the current code edition, not just the checklist
- Architect or engineer review recorded in `GOV-015`

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Sources

Requirements in this artifact trace to the following rows in `source-register.csv`. Re-verify before relying on any of them — agency requirements change without notice.

| Source | Document | Status | Pinpoint |
| --- | --- | --- | --- |
| `SRC-015` | BSEED Plan Review | `verified` | Codes enforced; ePlans/eLAPS process steps; coordinating departments |
| `SRC-017` | Residential Building Permit/Plan Submittal Checklist | `verified` | Preamble (submittal quantities, sealed-drawing statement, fee deposit); Plot Plan; Foundation Plans; Floor Plans; Elevations; Framing Plans; Electrical; Mechanical; Details and General Notes |

## Unresolved questions

_None recorded. Add any question that would change a decision if answered differently._

## Approvals and professional review

- **Required reviewer: `licensed_architect_or_engineer`.** Record the review in `GOV-015` before this artifact is relied on at a gate.
- Conclusions reserved to that discipline must come from that professional, not from this document.

## Dependencies

**Upstream — this cannot be completed without:**

- `SCR-003` — Owner's project requirements brief


**Stage gates this is required evidence for:** `SG-06`

## Typst issue version expected?

**Yes.** A paired Typst issue document is expected before this leaves the project. Base template: `publication/typst/templates/report.typ`.

Transfer reviewed content to the `.typ` deliberately — there is no automatic Markdown→Typst conversion. The Markdown draft and the Typst issue share this `artifact_id`; the Typst metadata records the draft path and its SHA-256.

Compilation is not approval. See `publication/README.md` for the issue gate.
