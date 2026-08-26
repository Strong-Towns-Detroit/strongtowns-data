---
artifact_id: APR-006
artifact_type: log
title: Permit comment and response log
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
source_ids: [SRC-015]
depends_on: [APR-001]
supersedes: null
confidentiality: internal
---

# Permit comment and response log

`APR-006` · approvals · service code `PMT`

> **Parcel-specific.** Create one copy per candidate parcel under `working/candidate-parcels/<parcel-id>/`. Do not complete this template in place.

## Purpose

Log of plan review comments and the responses submitted.

## When to use it

From first comment through approval.

## Required inputs

- Plan review comments via ePlans
- Response submissions

## Instructions

- ICA Exhibit A assigns the Contractor responsibility to track applications through plan review, respond to reviewer comments, and resubmit.
- Log every comment individually with the responding drawing revision. A response that does not name the revision cannot be audited at re-review.
- Note the ICA §6 distinction: revisions required to obtain permit approval are corrected at no additional charge; revisions from Company-directed change are billable. Code each response accordingly.
- Comments may come from any coordinating reviewer `SRC-015` names, not only BSEED plan review.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Every comment logged with a response and a drawing revision
- Responses coded to the ICA §6 distinction
- Comments from coordinating departments captured
- Turnaround times recorded for schedule learning

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Sources

Requirements in this artifact trace to the following rows in `source-register.csv`. Re-verify before relying on any of them — agency requirements change without notice.

| Source | Document | Status | Pinpoint |
| --- | --- | --- | --- |
| `SRC-015` | BSEED Plan Review | `verified` | Codes enforced; ePlans/eLAPS process steps; coordinating departments |

## Unresolved questions

_None recorded. Add any question that would change a decision if answered differently._

## Approvals and professional review

- **Required reviewer: `licensed_architect_or_engineer`.** Record the review in `GOV-015` before this artifact is relied on at a gate.
- Conclusions reserved to that discipline must come from that professional, not from this document.

## Dependencies

**Upstream — this cannot be completed without:**

- `APR-001` — Permit and approval matrix


## Typst issue version expected?

**No.** This artifact stays in Markdown. If it ever becomes an external submission, a stage-gate package, or a controlled-distribution PDF, update `typst_issue_required` in `artifact-register.csv` first — the register is the source of truth, not the file.
