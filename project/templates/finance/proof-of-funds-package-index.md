---
artifact_id: FIN-008
artifact_type: index
title: Proof-of-funds package index
workstream: finance
service_code: EST
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
depends_on: [FIN-001]
supersedes: null
confidentiality: sensitive
---

# Proof-of-funds package index

`FIN-008` · finance · service code `EST`

> **Sensitive.** This blank template is tracked; every *completed* copy lives under `project/private/` and is never committed. Record no credentials, account numbers, signatures, government IDs, or personal financial information in it.

## Purpose

Index of the proof-of-funds package: what evidences capacity, and where each original is held.

## When to use it

With any application requiring evidence of financial capability.

## Required inputs

- Financial evidence
- Lender commitments

## Instructions

- Index only. This artifact records that a document exists and where it lives — it never contains the document.
- Never record balances, account numbers, or statements in this repository.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Every required evidence item indexed
- Nothing sensitive stored in-repo
- Custodian recorded for each original

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Sources

_No external requirements cited. If this artifact starts asserting one, add a row to `source-register.csv` first._

## Unresolved questions

_None recorded. Add any question that would change a decision if answered differently._

## Approvals and professional review

- **Required reviewer: `company_decision_authority`.** Record the review in `GOV-015` before this artifact is relied on at a gate.
- Conclusions reserved to that discipline must come from that professional, not from this document.

## Dependencies

**Upstream — this cannot be completed without:**

- `FIN-001` — Cost plan


## Typst issue version expected?

**No.** This artifact stays in Markdown. If it ever becomes an external submission, a stage-gate package, or a controlled-distribution PDF, update `typst_issue_required` in `artifact-register.csv` first — the register is the source of truth, not the file.
