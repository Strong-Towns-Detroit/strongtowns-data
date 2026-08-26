---
artifact_id: GOV-021
artifact_type: log
title: Spending authorization log
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
depends_on: []
supersedes: null
confidentiality: sensitive
---

# Spending authorization log

`GOV-021` · governance · service code `ADM`

> **Sensitive.** This blank template is tracked; every *completed* copy lives under
`project/private/` and is never committed. Record no credentials, account numbers,
signatures, government IDs, or personal financial information in it.

## Purpose

Records authorizations to commit Company funds, and flags spend approaching the per-transaction and per-month limits before it exceeds them.

## When to use it

Before committing Company funds; and continuously as the monthly total accumulates.

## Required inputs

- Approved budget
- Per-transaction and per-month limits from the executed Agreement
- `GOV-020` expenditure log

## Instructions

- Take the thresholds from the **executed** Agreement. The draft carries bracketed figures (§3.2 per-transaction and per-month; §3.4 advance-authorization floor) that are open negotiation points — do not hardcode a bracketed number as if it were agreed.
- Track the running monthly total. The monthly cap binds even when each transaction is individually under the per-transaction cap.
- Authorization may be given at the weekly meeting or by email (§3.2). Either way it gets a row here, with the authoriser and the date.
- Anything outside the approved budget requires authorization regardless of amount.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Every commitment above threshold has a recorded prior authorization
- The running monthly total is current
- Thresholds cited match the executed Agreement, not the draft

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Unresolved questions

- Confirm the final per-transaction, per-month, and advance-authorization figures once the Agreement is executed.

## Approvals and professional review

- **Required reviewer: `company_decision_authority`.** Record the review in `GOV-015` before this artifact is relied on at a gate.
- Conclusions reserved to that discipline must come from that professional, not from this document.

## Dependencies

**Upstream:** none. This is an entry point.

**Downstream — these depend on this:**

- `GOV-020` — Expenditure substantiation and receipt log

## Typst issue version expected?

**No.** This artifact stays in Markdown. If it ever becomes an external submission, a stage-gate package, or a controlled-distribution PDF, update `typst_issue_required` in `artifact-register.csv` first — the register is the source of truth, not the file.
