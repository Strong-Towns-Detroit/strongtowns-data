---
artifact_id: FIN-003
artifact_type: register
title: Soft-cost and contingency register
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
source_as_of: 2026-08-26
source_ids: [SRC-018]
depends_on: [FIN-001]
supersedes: null
confidentiality: sensitive
---

# Soft-cost and contingency register

`FIN-003` · finance · service code `EST`

> **Sensitive.** This blank template is tracked; every *completed* copy lives under `project/private/` and is never committed. Record no credentials, account numbers, signatures, government IDs, or personal financial information in it.

## Purpose

Register of soft costs and contingencies — the lines most often omitted and most often blamed later.

## When to use it

With the cost plan.

## Required inputs

- `DSN-014` sealed-drawing triggers
- `SRC-018` fee schedule
- Consultant scopes
- Diligence costs

## Instructions

- Enumerate: design and engineering, sealed drawings, permit and plan review fees, survey, title, environmental, geotechnical, utility connection, insurance, legal, financing costs, and the tax capture buy-out.
- Sealed-drawing costs follow directly from `DSN-014`. Do not carry them as a lump.
- State each contingency's purpose. An undifferentiated contingency gets spent on the first surprise regardless of what it was for.
- Every figure states its basis (quote, estimate, published figure, placeholder) and a confidence. A placeholder that looks like an estimate is how a cost plan misleads.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Every soft cost category present or explicitly zero
- Sealed-drawing costs itemised from `DSN-014`
- Each contingency has a stated purpose

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Sources

Requirements in this artifact trace to the following rows in `source-register.csv`. Re-verify before relying on any of them — agency requirements change without notice.

| Source | Document | Status | Pinpoint |
| --- | --- | --- | --- |
| `SRC-018` | Fee Schedule (BSEED) | `verified` | Filename carries effective and modification dates; line items not yet abstracted |

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
