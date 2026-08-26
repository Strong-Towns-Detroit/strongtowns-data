---
artifact_id: APR-007
artifact_type: log
title: Permit log
workstream: approvals
service_code: PMT
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
source_as_of: 2026-08-26
source_ids: [SRC-019, SRC-018]
depends_on: [APR-001]
supersedes: null
confidentiality: internal
---

# Permit log

`APR-007` · approvals · service code `PMT`

> **Parcel-specific.** Create one copy per candidate parcel under `working/candidate-parcels/<parcel-id>/`. Do not complete this template in place.

## Purpose

The permit log ICA Exhibit A requires: status, fees paid, expiration dates, conditions of approval.

## When to use it

From first application; maintained through closeout.

## Required inputs

- Permit applications and issued permits
- `SRC-018` fee schedule
- `SRC-019` eLAPS

## Instructions

- Record all four Exhibit A fields for every permit: status, fees paid, expiration date, conditions of approval.
- Expiration is the field that bites. A permit that lapses mid-construction is a stop-work event.
- `SRC-019` is the production Accela instance; note that Accela deployments commonly also expose a test twin — confirm you are reading production before recording a status.
- An unchecked condition is `not_found` or `blocked` — never `verified`, never blank.

## Completion criteria

This artifact is complete when **all** of the following hold:

- All four Exhibit A fields present for every permit
- Expiration dates calendared in `APR-008`
- Conditions cross-referenced to `APR-005`
- Statuses read from the production portal

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Sources

Requirements in this artifact trace to the following rows in `source-register.csv`. Re-verify before relying on any of them — agency requirements change without notice.

| Source | Document | Status | Pinpoint |
| --- | --- | --- | --- |
| `SRC-019` | Accela Citizen Access / eLAPS permit portal | `listed_not_retrieved` | — |
| `SRC-018` | Fee Schedule (BSEED) | `verified` | Filename carries effective and modification dates; line items not yet abstracted |

## Unresolved questions

_None recorded. Add any question that would change a decision if answered differently._

## Approvals and professional review

- **Required reviewer: `internal_peer`.** No licensed professional is required for this artifact.
- The Company still decides; the Contractor recommends (ICA §1.3).

## Dependencies

**Upstream — this cannot be completed without:**

- `APR-001` — Permit and approval matrix


**Stage gates this is required evidence for:** `SG-09`

## Typst issue version expected?

**No.** This artifact stays in Markdown. If it ever becomes an external submission, a stage-gate package, or a controlled-distribution PDF, update `typst_issue_required` in `artifact-register.csv` first — the register is the source of truth, not the file.
