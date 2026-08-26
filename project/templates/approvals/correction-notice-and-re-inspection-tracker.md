---
artifact_id: APR-010
artifact_type: tracker
title: Correction notice and re-inspection tracker
workstream: approvals
service_code: INS
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
depends_on: [APR-001]
supersedes: null
confidentiality: internal
---

# Correction notice and re-inspection tracker

`APR-010` · approvals · service code `INS`

> **Parcel-specific.** Create one copy per candidate parcel under `working/candidate-parcels/<parcel-id>/`. Do not complete this template in place.

## Purpose

Tracker for correction notices and re-inspections. ICA Exhibit A assigns the Contractor tracking inspection results and correction notices, reporting failures and stop-work orders promptly, and following corrections through to closure.

## When to use it

On any inspection result.

## Required inputs

- Inspection results
- Correction notices

## Instructions

- Report failures and stop-work orders to the Company **promptly** — Exhibit A makes this an explicit obligation, and a stop-work order is a same-day escalation, not a weekly-report item.
- Track each correction to re-inspection and closure with the municipality. Closure with the municipality is the deliverable, not the correction itself.
- The correction work is the Company's builder's responsibility. The Contractor tracks and closes out the municipal record.
- An unchecked condition is `not_found` or `blocked` — never `verified`, never blank.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Every correction notice tracked to municipal closure
- Failures and stop-work orders escalated same-day and logged in `GOV-009`
- The tracking-versus-performing boundary respected

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

- `APR-001` — Permit and approval matrix


## Typst issue version expected?

**No.** This artifact stays in Markdown. If it ever becomes an external submission, a stage-gate package, or a controlled-distribution PDF, update `typst_issue_required` in `artifact-register.csv` first — the register is the source of truth, not the file.
