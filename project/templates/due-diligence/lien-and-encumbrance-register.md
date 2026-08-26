---
artifact_id: DD-006
artifact_type: register
title: Lien and encumbrance register
workstream: due-diligence
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
source_as_of: null
source_ids: []
depends_on: [DD-001]
supersedes: null
confidentiality: internal
---

# Lien and encumbrance register

`DD-006` · due-diligence · service code `LND`

> **Parcel-specific.** Create one copy per candidate parcel under `working/candidate-parcels/<parcel-id>/`. Do not complete this template in place.

## Purpose

Registers liens and encumbrances beyond title exceptions — judgments, municipal charges, demolition liens, and anything else attaching to the parcel.

## When to use it

Alongside the title review.

## Required inputs

- Title commitment
- Municipal records
- Court records

## Instructions

- Demolition and nuisance-abatement liens are common on Detroit vacant land and may not appear where expected. Search specifically.
- Record the amount, the holder, and whether it survives the conveyance. A lien that survives is a purchase-price adjustment; one that does not is a closing mechanic.
- Any conclusion reserved to a licensed discipline comes from that professional, not from this artifact.
- A condition not yet checked is recorded `not_found` or `blocked` — never `verified`, never blank.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Every lien recorded with amount, holder and survival position
- Survival conclusions reviewed by counsel

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Sources

_No external requirements cited. If this artifact starts asserting one, add a row to `source-register.csv` first._

## Unresolved questions

_None recorded. Add any question that would change a decision if answered differently._

## Approvals and professional review

- **Required reviewer: `michigan_licensed_attorney`.** `legal_review_required: true` — every stage gate this artifact feeds is blocked until that review is recorded in `GOV-015` (professional-review tracker).
- This document is an *issue-spotting tool*. It does not contain legal advice and must not be treated as a substitute for counsel.
- Record the reviewer, the date, and the scope reviewed. A review with no recorded scope does not clear the gate.

## Dependencies

**Upstream — this cannot be completed without:**

- `DD-001` — Due-diligence plan and deadline calculator


## Typst issue version expected?

**No.** This artifact stays in Markdown. If it ever becomes an external submission, a stage-gate package, or a controlled-distribution PDF, update `typst_issue_required` in `artifact-register.csv` first — the register is the source of truth, not the file.
