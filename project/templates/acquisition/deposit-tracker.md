---
artifact_id: ACQ-018
artifact_type: tracker
title: Deposit tracker
workstream: acquisition
service_code: LND
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
source_as_of: 2026-08-26
source_ids: [SRC-008]
depends_on: [ACQ-001]
supersedes: null
confidentiality: internal
---

# Deposit tracker

`ACQ-018` · acquisition · service code `LND`

> **Parcel-specific.** Create one copy per candidate parcel under `working/candidate-parcels/<parcel-id>/`. Do not complete this template in place.

## Purpose

Tracks deposits and earnest money: amount, form, holder, and the conditions under which it is refundable.

## When to use it

From the first deposit until closing or return.

## Required inputs

- Executed offer or agreement
- Deposit receipts

## Instructions

- Record who holds the deposit and under what instrument. `SRC-008` states a 10% earnest money deposit in certified funds is due to the Detroit Building Authority at purchase agreement execution for commercial City-owned property; confirm what applies to the actual pathway.
- Record refundability conditions precisely — this is the money at risk if diligence fails.
- Do not record account or routing numbers.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Amount, form, holder and instrument recorded
- Refundability conditions stated with their source
- No payment credentials stored

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Sources

Requirements in this artifact trace to the following rows in `source-register.csv`. Re-verify before relying on any of them — agency requirements change without notice.

| Source | Document | Status | Pinpoint |
| --- | --- | --- | --- |
| `SRC-008` | Property Sales and Purchase FAQs | `verified` | Review-body list; conceptual plan requirement; market-value pricing; ~4-month timeline; 10% earnest money for commercial |

## Unresolved questions

_None recorded. Add any question that would change a decision if answered differently._

## Approvals and professional review

- **Required reviewer: `michigan_licensed_attorney`.** `legal_review_required: true` — every stage gate this artifact feeds is blocked until that review is recorded in `GOV-015` (professional-review tracker).
- This document is an *issue-spotting tool*. It does not contain legal advice and must not be treated as a substitute for counsel.
- Record the reviewer, the date, and the scope reviewed. A review with no recorded scope does not clear the gate.

## Dependencies

**Upstream — this cannot be completed without:**

- `ACQ-001` — Acquisition pathway decision tree


## Typst issue version expected?

**No.** This artifact stays in Markdown. If it ever becomes an external submission, a stage-gate package, or a controlled-distribution PDF, update `typst_issue_required` in `artifact-register.csv` first — the register is the source of truth, not the file.
