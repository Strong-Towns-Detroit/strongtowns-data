---
artifact_id: APR-003
artifact_type: tracker
title: Utility application tracker
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
source_ids: [SRC-020]
depends_on: [APR-001]
supersedes: null
confidentiality: internal
---

# Utility application tracker

`APR-003` · approvals · service code `PMT`

> **Parcel-specific.** Create one copy per candidate parcel under `working/candidate-parcels/<parcel-id>/`. Do not complete this template in place.

## Purpose

Tracker for utility applications: water, sewer, gas, electric, telecom.

## When to use it

As soon as the site plan is stable enough to locate services.

## Required inputs

- `DD-019` utility availability matrix
- `SRC-020` DWSD service page
- Utility application requirements

## Instructions

- Track application, review, approval and connection as separate states. Approval is not connection, and connection is what the schedule needs.
- `SRC-020` covers water ACCOUNT setup, which is a different question from new-service tap availability and capacity for a vacant lot. `DD-019` needs the latter and it is not yet sourced.
- Record lead times. Utility connection is a common critical-path item and a common surprise.
- An unchecked condition is `not_found` or `blocked` — never `verified`, never blank.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Every utility tracked through four distinct states
- Lead times recorded
- Connection dates reflected in `CON-003`

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Sources

Requirements in this artifact trace to the following rows in `source-register.csv`. Re-verify before relying on any of them — agency requirements change without notice.

| Source | Document | Status | Pinpoint |
| --- | --- | --- | --- |
| `SRC-020` | How do I turn on / transfer / turn off water service | `listed_not_retrieved` | — |

## Unresolved questions

- What is the process, cost and lead time for a NEW water and sewer tap on a vacant Detroit infill lot?

## Approvals and professional review

- **Required reviewer: `internal_peer`.** No licensed professional is required for this artifact.
- The Company still decides; the Contractor recommends (ICA §1.3).

## Dependencies

**Upstream — this cannot be completed without:**

- `APR-001` — Permit and approval matrix


## Typst issue version expected?

**No.** This artifact stays in Markdown. If it ever becomes an external submission, a stage-gate package, or a controlled-distribution PDF, update `typst_issue_required` in `artifact-register.csv` first — the register is the source of truth, not the file.
