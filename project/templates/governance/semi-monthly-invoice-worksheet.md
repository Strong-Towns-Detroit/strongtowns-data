---
artifact_id: GOV-019
artifact_type: worksheet
title: Semi-monthly invoice worksheet
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
depends_on: [GOV-018]
supersedes: null
confidentiality: sensitive
---

# Semi-monthly invoice worksheet

`GOV-019` · governance · service code `ADM`

> **Sensitive.** This blank template is tracked; every *completed* copy lives under
`project/private/` and is never committed. Record no credentials, account numbers,
signatures, government IDs, or personal financial information in it.

## Purpose

Preparation worksheet for the semi-monthly invoice. The invoice form itself is Exhibit B to the Agreement — Company-supplied, and reproduced from the executed Agreement rather than authored here.

## When to use it

At each period close: the 15th and the last day of the month. Due by end of the first business day after close (§2.2).

## Required inputs

- `GOV-018` time record for the period
- `GOV-020` receipts for reimbursables

## Instructions

- Total hours by service code before filling the Company's form.
- Attach receipts for every reimbursable (§3.3).
- Submit by the deadline — a late invoice is paid in the following cycle (§2.3).
- Do not record bank details, account numbers, or any payment credentials in this workspace. Remittance details go on the Company's form only.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Hours reconcile to `GOV-018`
- Hours-by-code subtotals sum to the total
- Every reimbursable line has an attached receipt
- No payment credentials stored in-repo

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Unresolved questions

_None recorded. Add any question that would change a decision if answered differently._

## Approvals and professional review

- **Required reviewer: `internal_peer`.** No licensed professional is required for this artifact.
- The Company still decides; the Contractor recommends (ICA §1.3).

## Dependencies

**Upstream — this cannot be completed without:**

- `GOV-018` — Time record and service-code log


## Typst issue version expected?

**No.** This artifact stays in Markdown. If it ever becomes an external submission, a stage-gate package, or a controlled-distribution PDF, update `typst_issue_required` in `artifact-register.csv` first — the register is the source of truth, not the file.
