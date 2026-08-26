---
artifact_id: DD-005
artifact_type: review
title: Tax, assessment, water and municipal-charge review
workstream: due-diligence
service_code: LND
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
source_ids: [SRC-001, SRC-005, SRC-013]
depends_on: [DD-001]
supersedes: null
confidentiality: internal
---

# Tax, assessment, water and municipal-charge review

`DD-005` · due-diligence · service code `LND`

> **Parcel-specific.** Create one copy per candidate parcel under `working/candidate-parcels/<parcel-id>/`. Do not complete this template in place.

## Purpose

Establishes the tax, assessment, water and municipal charge position — which on a DLBA purchase is also an eligibility question, not only a cost question.

## When to use it

Early. A tax finding can disqualify the purchase entirely.

## Required inputs

- Wayne County Treasurer records
- City of Detroit assessment and water records
- Purchasing entity's own Detroit property tax status

## Instructions

- Check two different things and do not conflate them: charges against the PARCEL, and the purchasing entity's standing across ALL Detroit property.
- `SRC-001` Ch. VI(B)(3) requires no delinquent or currently due taxes on the lot; Ch. VI(C)(4) requires the purchaser to be current on all Detroit property owned directly or indirectly. `SRC-005` adds the general bars: Wayne County delinquency, tax foreclosure within three years, outstanding blight or code violations.
- Carry the DLBA five-year, fifty-percent tax capture as a cost until `SRC-013` is retrieved and read. It has not been. This is material to project economics.
- Water arrears can attach to the property. Establish the position in writing from DWSD, not by inference.
- A condition not yet checked is recorded `not_found` or `blocked` — never `verified`, never blank.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Parcel-level charges established from primary records
- Entity-level eligibility established across all Detroit holdings
- Tax capture position established or explicitly carried as unknown
- Water position confirmed in writing

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Sources

Requirements in this artifact trace to the following rows in `source-register.csv`. Re-verify before relying on any of them — agency requirements change without notice.

| Source | Document | Status | Pinpoint |
| --- | --- | --- | --- |
| `SRC-001` | Second Amended and Restated Vacant Land Policy | `verified` | Ch. VI (Infill Housing Lots), pp.16-18; Ch. VIII (Land-Based Projects) pp.21-23; Ch. IX (Land Review Areas) pp.24-25 |
| `SRC-005` | Frequently Asked Questions | `verified` | Buyer eligibility list; deed and closing section; closing-cost estimates |
| `SRC-013` | Tax Capture Waiver Policy (First Amended, Nov 2020) | `listed_not_retrieved` | — |

## Unresolved questions

- Is the 5yr/50% tax capture waived for Infill Housing Lots? `SRC-013` not retrieved.

## Approvals and professional review

- **Required reviewer: `cpa_or_tax_advisor`.** Record the review in `GOV-015` before this artifact is relied on at a gate.
- Conclusions reserved to that discipline must come from that professional, not from this document.

## Dependencies

**Upstream — this cannot be completed without:**

- `DD-001` — Due-diligence plan and deadline calculator


## Typst issue version expected?

**No.** This artifact stays in Markdown. If it ever becomes an external submission, a stage-gate package, or a controlled-distribution PDF, update `typst_issue_required` in `artifact-register.csv` first — the register is the source of truth, not the file.
