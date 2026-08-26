---
artifact_id: FIN-007
artifact_type: register
title: Incentive, abatement, grant and rebate register
workstream: finance
service_code: EST
status: template
template_version: "1.0"
parcel_ids: []
owner_role: contractor_program_manager
decision_role: company_decision_authority
required_reviewer_role: cpa_or_tax_advisor
legal_review_required: false
typst_issue_required: false
typst_source: null
latest_issue_id: null
created_at: 2026-08-26
updated_at: 2026-08-26
source_as_of: 2026-08-26
source_ids: [SRC-013, SRC-009]
depends_on: [FIN-001]
supersedes: null
confidentiality: sensitive
---

# Incentive, abatement, grant and rebate register

`FIN-007` · finance · service code `EST`

> **Sensitive.** This blank template is tracked; every *completed* copy lives under `project/private/` and is never committed. Record no credentials, account numbers, signatures, government IDs, or personal financial information in it.

## Purpose

Register of incentives, abatements, grants and rebates — what exists, what the project qualifies for, and what each requires in return.

## When to use it

Early. Several incentives must be applied for before work starts.

## Required inputs

- Programme documentation
- `SRC-013` tax capture policy

## Instructions

- Record the application deadline relative to construction start. An incentive applied for after mobilisation is usually forfeited.
- Note the interaction recorded in `SRC-009`: tax abatement can conflict with the DLBA five-year, fifty-percent tax capture and may require additional DLBA payments.
- `SRC-013` Sec. IV(B) waives the capture free for Auction and Own-It-Now purchases specifically so owners can take a Neighborhood Enterprise Zone or other abatement — that carve-out does not extend to Infill Housing Lots.
- Every incentive carries an obligation. Record it alongside the benefit.
- An unchecked condition is `not_found` or `blocked` — never `verified`, never blank.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Every incentive has a deadline relative to construction start
- Tax capture interaction assessed
- Obligations recorded alongside benefits
- CPA review recorded

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Sources

Requirements in this artifact trace to the following rows in `source-register.csv`. Re-verify before relying on any of them — agency requirements change without notice.

| Source | Document | Status | Pinpoint |
| --- | --- | --- | --- |
| `SRC-013` | First Amended Tax Capture Waiver Policy | `verified` | Sec. I (statutory basis MCL 211.7gg; waiver authority MCL 211.1025a(1)); Sec. II (governs over conflicting DLBA policy); Sec. III (application); Sec. IV(C) (Projects and Infill Housing Lots); Sec. IV(D) (de minimis); Sec. VI(A) (calculation) |
| `SRC-009` | Marketing Programs (marketed properties) | `verified` | 60-day listing; ~90 days to close; scoring categories; six proposal-guideline categories including New Build Opportunities |

## Unresolved questions

- Does a Neighborhood Enterprise Zone abatement interact with the Infill Housing Lot tax capture buy-out, and if so how?

## Approvals and professional review

- **Required reviewer: `cpa_or_tax_advisor`.** Record the review in `GOV-015` before this artifact is relied on at a gate.
- Conclusions reserved to that discipline must come from that professional, not from this document.

## Dependencies

**Upstream — this cannot be completed without:**

- `FIN-001` — Cost plan


## Typst issue version expected?

**No.** This artifact stays in Markdown. If it ever becomes an external submission, a stage-gate package, or a controlled-distribution PDF, update `typst_issue_required` in `artifact-register.csv` first — the register is the source of truth, not the file.
