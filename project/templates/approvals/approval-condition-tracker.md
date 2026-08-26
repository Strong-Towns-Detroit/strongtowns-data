---
artifact_id: APR-005
artifact_type: tracker
title: Approval-condition tracker
workstream: approvals
service_code: PMT
status: template
template_version: "1.0"
parcel_ids: []
owner_role: contractor_program_manager
decision_role: company_decision_authority
required_reviewer_role: michigan_licensed_attorney
legal_review_required: true
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

# Approval-condition tracker

`APR-005` · approvals · service code `PMT`

> **Parcel-specific.** Create one copy per candidate parcel under `working/candidate-parcels/<parcel-id>/`. Do not complete this template in place.

## Purpose

Tracker for conditions attached to any approval — the obligations that arrive with a yes.

## When to use it

On receipt of any conditional approval.

## Required inputs

- Approval documents

## Instructions

- Read the conditions before celebrating the approval. A conditional approval is a set of dated obligations.
- Every condition gets an owner, a deadline, and an evidence requirement. Conditions are what get missed at closeout.
- Feed continuing conditions into `CLO-012` compliance evidence index.
- An unchecked condition is `not_found` or `blocked` — never `verified`, never blank.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Every condition extracted with owner, deadline and evidence
- Continuing conditions routed to closeout
- Nothing marked satisfied without evidence

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Sources

_No external requirements cited. If this artifact starts asserting one, add a row to `source-register.csv` first._

## Unresolved questions

_None recorded. Add any question that would change a decision if answered differently._

## Approvals and professional review

- **Required reviewer: `michigan_licensed_attorney`.** `legal_review_required: true` — every stage gate this artifact feeds is blocked until that review is recorded in `GOV-015` (professional-review tracker).
- This document is an *issue-spotting tool*. It does not contain legal advice and must not be treated as a substitute for counsel.
- Record the reviewer, the date, and the scope reviewed. A review with no recorded scope does not clear the gate.

## Dependencies

**Upstream — this cannot be completed without:**

- `APR-001` — Permit and approval matrix


## Typst issue version expected?

**No.** This artifact stays in Markdown. If it ever becomes an external submission, a stage-gate package, or a controlled-distribution PDF, update `typst_issue_required` in `artifact-register.csv` first — the register is the source of truth, not the file.
