---
artifact_id: APR-001
artifact_type: matrix
title: Permit and approval matrix
workstream: approvals
service_code: PMT
status: template
template_version: "1.0"
parcel_ids: []
owner_role: contractor_program_manager
decision_role: company_decision_authority
required_reviewer_role: licensed_architect_or_engineer
legal_review_required: false
typst_issue_required: false
typst_source: null
latest_issue_id: null
created_at: 2026-08-26
updated_at: 2026-08-26
source_as_of: 2026-08-26
source_ids: [SRC-015, SRC-016]
depends_on: [DD-010]
supersedes: null
confidentiality: internal
---

# Permit and approval matrix

`APR-001` · approvals · service code `PMT`

> **Parcel-specific.** Create one copy per candidate parcel under `working/candidate-parcels/<parcel-id>/`. Do not complete this template in place.

## Purpose

The master matrix of every permit and approval the project needs: authority, submission, dependency, status.

## When to use it

As soon as the pathway and design basis are known. It drives the schedule more than the design does.

## Required inputs

- `SRC-016` BSEED division list
- `SRC-015` coordinating reviewers
- `DD-010` zoning confirmation
- Utility requirements

## Instructions

- One row per approval, each naming the authority, the submission route, what it depends on, and what depends on it.
- Include the coordinating reviewers `SRC-015` names — Health, Water & Sewerage, Fire Marshal, Planning & Development. Each can issue comments and each is a schedule dependency, not a formality.
- Map each approval to the BSEED division that owns it (`SRC-016`): Development Resource Center for intake, Zoning/Special Land Use for site plan and conditional use, Permits & Plan Review, Construction Inspection.
- Where an approval is a precondition to another, say so. The critical path through approvals is usually not the longest single review.
- An unchecked condition is `not_found` or `blocked` — never `verified`, never blank.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Every approval has an authority, a route, and a dependency
- Coordinating reviewers included as distinct rows
- Preconditions mapped
- Critical path through approvals identified

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Sources

Requirements in this artifact trace to the following rows in `source-register.csv`. Re-verify before relying on any of them — agency requirements change without notice.

| Source | Document | Status | Pinpoint |
| --- | --- | --- | --- |
| `SRC-015` | BSEED Plan Review | `verified` | Codes enforced; ePlans/eLAPS process steps; coordinating departments |
| `SRC-016` | Buildings, Safety Engineering and Environmental Department (divisions index) | `verified` | Division list and responsibilities |

## Unresolved questions

_None recorded. Add any question that would change a decision if answered differently._

## Approvals and professional review

- **Required reviewer: `licensed_architect_or_engineer`.** Record the review in `GOV-015` before this artifact is relied on at a gate.
- Conclusions reserved to that discipline must come from that professional, not from this document.

## Dependencies

**Upstream — this cannot be completed without:**

- `DD-010` — Zoning confirmation memo

**Downstream — these depend on this:**

- `APR-002` — BSEED submission checklist
- `APR-003` — Utility application tracker
- `APR-004` — Variance submission checklist
- `APR-005` — Approval-condition tracker
- `APR-006` — Permit comment and response log
- `APR-007` — Permit log
- `APR-008` — Permit expiration and renewal calendar
- `APR-009` — Municipal inspection scheduling log
- `APR-010` — Correction notice and re-inspection tracker
- `APR-011` — Agency correspondence

**Stage gates this is required evidence for:** `SG-07`

## Typst issue version expected?

**No.** This artifact stays in Markdown. If it ever becomes an external submission, a stage-gate package, or a controlled-distribution PDF, update `typst_issue_required` in `artifact-register.csv` first — the register is the source of truth, not the file.
