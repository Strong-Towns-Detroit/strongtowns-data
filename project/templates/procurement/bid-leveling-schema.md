---
artifact_id: PRO-005
artifact_type: schema
title: Bid-leveling schema
workstream: procurement
service_code: EST
status: template
template_version: "1.0"
parcel_ids: []
owner_role: contractor_program_manager
decision_role: company_decision_authority
required_reviewer_role: internal_peer
legal_review_required: false
typst_issue_required: false
typst_source: null
latest_issue_id: null
created_at: 2026-08-26
updated_at: 2026-08-26
source_as_of: null
source_ids: []
depends_on: [DSN-012]
supersedes: null
confidentiality: internal
---

# Bid-leveling schema

`PRO-005` · procurement · service code `EST`

> **Parcel-specific.** Create one copy per candidate parcel under `working/candidate-parcels/<parcel-id>/`. Do not complete this template in place.

## Purpose

The bid levelling schema: the structure that makes bids comparable.

## When to use it

Before bids are received, not after.

## Required inputs

- The bid form
- `FIN-001` cost plan structure

## Instructions

- Define the levelling structure before opening bids. A structure invented after seeing the numbers is a structure that flatters a preferred bidder.
- Level to a common scope: add back exclusions, normalise allowances, and price scope gaps from `PRO-006`.
- Show the adjustments, not just the adjusted total. The adjustments are the analysis.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Structure defined before bid opening
- Every adjustment itemised and explained
- Levelled totals reconcile to `FIN-001`

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Sources

_No external requirements cited. If this artifact starts asserting one, add a row to `source-register.csv` first._

## Unresolved questions

_None recorded. Add any question that would change a decision if answered differently._

## Approvals and professional review

- **Required reviewer: `internal_peer`.** No licensed professional is required for this artifact.
- The Company still decides; the Contractor recommends (ICA §1.3).

## Dependencies

**Upstream — this cannot be completed without:**

- `DSN-012` — Design deliverables register


**Stage gates this is required evidence for:** `SG-08`

## Typst issue version expected?

**No.** This artifact stays in Markdown. If it ever becomes an external submission, a stage-gate package, or a controlled-distribution PDF, update `typst_issue_required` in `artifact-register.csv` first — the register is the source of truth, not the file.
