---
artifact_id: GOV-020
artifact_type: log
title: Expenditure substantiation and receipt log
workstream: governance
service_code: ADM
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
depends_on: [GOV-021]
supersedes: null
confidentiality: sensitive
---

# Expenditure substantiation and receipt log

`GOV-020` · governance · service code `ADM`

> **Sensitive.** This blank template is tracked; every *completed* copy lives under
`project/private/` and is never committed. Record no credentials, account numbers,
signatures, government IDs, or personal financial information in it.

## Purpose

Itemised receipt record for every Company-funded expenditure, coded to the property, per ICA §3.3.

## When to use it

At the moment of every expenditure. Receipts are collected, not reconstructed.

## Required inputs

- Receipts
- The authorization that permitted the spend (`GOV-021`)

## Instructions

- Code every receipt to a property.
- Link each expenditure to its authorization. An expenditure with no authorization record is the finding.
- Distinguish Company-card spend (§3.1) from Contractor-advanced funds (§3.4) — the latter requires prior authorization above the stated threshold and is reimbursed at cost without markup.
- Do not store card numbers or account identifiers. Reference the last four digits at most, and only if operationally necessary.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Every expenditure has an itemised receipt and a property code
- Every expenditure links to an authorization
- No card or account numbers stored

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Unresolved questions

_None recorded. Add any question that would change a decision if answered differently._

## Approvals and professional review

- **Required reviewer: `internal_peer`.** No licensed professional is required for this artifact.
- The Company still decides; the Contractor recommends (ICA §1.3).

## Dependencies

**Upstream — this cannot be completed without:**

- `GOV-021` — Spending authorization log


## Typst issue version expected?

**No.** This artifact stays in Markdown. If it ever becomes an external submission, a stage-gate package, or a controlled-distribution PDF, update `typst_issue_required` in `artifact-register.csv` first — the register is the source of truth, not the file.
