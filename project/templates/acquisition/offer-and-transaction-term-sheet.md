---
artifact_id: ACQ-017
artifact_type: term_sheet
title: Offer and transaction term sheet
workstream: acquisition
service_code: LND
status: template
template_version: "1.0"
parcel_ids: []
owner_role: contractor_program_manager
decision_role: company_decision_authority
required_reviewer_role: michigan_licensed_attorney
legal_review_required: true
typst_issue_required: true
typst_source: publication/typst/templates/memo.typ
latest_issue_id: null
created_at: 2026-08-26
updated_at: 2026-08-26
source_as_of: 2026-08-26
source_ids: [SRC-001, SRC-013]
depends_on: [ACQ-001]
supersedes: null
confidentiality: internal
---

# Offer and transaction term sheet

`ACQ-017` · acquisition · service code `LND`

> **Parcel-specific.** Create one copy per candidate parcel under `working/candidate-parcels/<parcel-id>/`. Do not complete this template in place.

## Purpose

States the commercial terms of an offer before any agreement is drafted. This is a term sheet and an issue list — it is not an operative purchase agreement and must never be presented as one.

## When to use it

Once diligence supports an offer and before counsel is instructed.

## Required inputs

- `SCR-008` cost screen
- Pricing basis from the governing policy
- `DD-027` go/no-go recommendation

## Instructions

- Establish the pricing mechanism from the policy, not from negotiation instinct. Infill Housing Lots are listed at fair market value as determined by an independent real estate broker (`SRC-001` Ch.VI(D)).
- Model the discounts deliberately. Ch.VI(D)(1) offers 50% off where at least 25% of units are affordable at no more than 80% AMI, or 80% off where at least 25% are at no more than 50% AMI — but both require RENTAL units and a ten-year affordability agreement with City monitoring. Ch.VI(D)(2) caps cumulative discount at 90%.
- A discount taken is an obligation accepted. A ten-year monitored affordability covenant is a material, long-lived constraint and belongs in the decision log with its rejected alternative.
- Carry the DLBA five-year, fifty-percent tax capture as a cost until the Tax Capture Waiver Policy (`SRC-013`) is retrieved and read. It has not been.
- This artifact does not create an obligation. Counsel drafts or reviews the operative instrument.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Pricing basis traced to the governing policy
- Any discount modelled together with the obligation it carries
- Tax capture position established or explicitly carried as unknown
- Marked for counsel review before any agreement is signed

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Sources

Requirements in this artifact trace to the following rows in `source-register.csv`. Re-verify before relying on any of them — agency requirements change without notice.

| Source | Document | Status | Pinpoint |
| --- | --- | --- | --- |
| `SRC-001` | Second Amended and Restated Vacant Land Policy | `verified` | Ch. VI (Infill Housing Lots), pp.16-18; Ch. VIII (Land-Based Projects) pp.21-23; Ch. IX (Land Review Areas) pp.24-25 |
| `SRC-013` | Tax Capture Waiver Policy (First Amended, Nov 2020) | `listed_not_retrieved` | — |

## Unresolved questions

- Is the DLBA's 5-year/50% tax capture waived for Infill Housing Lots? `SRC-013` not yet retrieved and this is material to project economics.

## Approvals and professional review

- **Required reviewer: `michigan_licensed_attorney`.** `legal_review_required: true` — every stage gate this artifact feeds is blocked until that review is recorded in `GOV-015` (professional-review tracker).
- This document is an *issue-spotting tool*. It does not contain legal advice and must not be treated as a substitute for counsel.
- Record the reviewer, the date, and the scope reviewed. A review with no recorded scope does not clear the gate.

## Dependencies

**Upstream — this cannot be completed without:**

- `ACQ-001` — Acquisition pathway decision tree


**Stage gates this is required evidence for:** `SG-03`

## Typst issue version expected?

**Yes.** A paired Typst issue document is expected before this leaves the project. Base template: `publication/typst/templates/memo.typ`.

Transfer reviewed content to the `.typ` deliberately — there is no automatic Markdown→Typst conversion. The Markdown draft and the Typst issue share this `artifact_id`; the Typst metadata records the draft path and its SHA-256.

Compilation is not approval. See `publication/README.md` for the issue gate.
