---
artifact_id: GOV-009
artifact_type: register
title: Risk and issue register
workstream: governance
service_code: ADM
status: template
template_version: "1.0"
parcel_ids: []
owner_role: contractor_program_manager
decision_role: company_decision_authority
required_reviewer_role: company_decision_authority
legal_review_required: false
typst_issue_required: false
typst_source: null
latest_issue_id: null
created_at: 2026-08-26
updated_at: 2026-08-26
source_as_of: null
source_ids: []
depends_on: [GOV-002]
supersedes: null
confidentiality: internal
---

# Risk and issue register

`GOV-009` · governance · service code `ADM`

> **Reusable.** One copy project-wide, under `working/project-wide/`.

## Purpose

Single place where risks (may happen) and issues (have happened) are tracked with owner, response, and status.

## When to use it

Continuously. Reviewed at the weekly coordination meeting and reported in the weekly status report.

## Required inputs

- Findings from diligence, design, permitting, and cost artifacts

## Instructions

- Distinguish risk from issue. A risk with no trigger condition is an anxiety, not a risk.
- Every entry names one owner. Shared ownership means no ownership.
- Escalate anything that changes budget, schedule, or the decision to acquire into the weekly status report (`GOV-017`).

## Completion criteria

This artifact is complete when **all** of the following hold:

- Every open entry has an owner and a next action with a date
- Entries affecting a gate are reflected in that gate's package

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Unresolved questions

_None recorded. Add any question that would change a decision if answered differently._

## Approvals and professional review

- **Required reviewer: `company_decision_authority`.** Record the review in `GOV-015` before this artifact is relied on at a gate.
- Conclusions reserved to that discipline must come from that professional, not from this document.

## Dependencies

**Upstream — this cannot be completed without:**

- `GOV-002` — Artifact lifecycle and publication rules

**Downstream — these depend on this:**

- `GOV-017` — Weekly status report

## Typst issue version expected?

**No.** This artifact stays in Markdown. If it ever becomes an external submission, a stage-gate package, or a controlled-distribution PDF, update `typst_issue_required` in `artifact-register.csv` first — the register is the source of truth, not the file.
