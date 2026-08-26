---
artifact_id: FIN-010
artifact_type: matrix
title: Insurance matrix
workstream: finance
service_code: ADM
status: template
template_version: "1.0"
parcel_ids: []
owner_role: contractor_program_manager
decision_role: company_decision_authority
required_reviewer_role: licensed_insurance_agent
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

# Insurance matrix

`FIN-010` · finance · service code `ADM`

> **Sensitive.** This blank template is tracked; every *completed* copy lives under `project/private/` and is never committed. Record no credentials, account numbers, signatures, government IDs, or personal financial information in it.

## Purpose

Matrix of required insurance: who carries what, at what limits, from when.

## When to use it

Before any work starts on site.

## Required inputs

- Lender requirements
- Contract requirements
- Insurance advisor input

## Instructions

- ICA §7.2 makes the Company solely responsible for construction including job site safety, and §7.4 disclaims Contractor liability for construction. The insurance matrix should reflect that allocation rather than contradict it.
- Builder's risk must be in place before materials arrive, not before work starts. Those are different dates.
- Record required certificates and their expiry. An expired certificate is an uninsured project.
- Conclusions reserved to a licensed discipline come from that professional, not from this artifact.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Every party's required coverage and limits recorded
- Effective dates precede the exposure they cover
- Certificate expiries calendared
- Insurance professional review recorded

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Sources

_No external requirements cited. If this artifact starts asserting one, add a row to `source-register.csv` first._

## Unresolved questions

_None recorded. Add any question that would change a decision if answered differently._

## Approvals and professional review

- **Required reviewer: `licensed_insurance_agent`.** Record the review in `GOV-015` before this artifact is relied on at a gate.
- Conclusions reserved to that discipline must come from that professional, not from this document.

## Dependencies

**Upstream — this cannot be completed without:**

- `FIN-001` — Cost plan


## Typst issue version expected?

**No.** This artifact stays in Markdown. If it ever becomes an external submission, a stage-gate package, or a controlled-distribution PDF, update `typst_issue_required` in `artifact-register.csv` first — the register is the source of truth, not the file.
