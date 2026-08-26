---
artifact_id: DD-001
artifact_type: plan
title: Due-diligence plan and deadline calculator
workstream: due-diligence
service_code: LND
status: template
template_version: "1.0"
parcel_ids: []
owner_role: contractor_program_manager
decision_role: company_decision_authority
required_reviewer_role: michigan_licensed_attorney
legal_review_required: true
typst_issue_required: true
typst_source: publication/typst/templates/report.typ
latest_issue_id: null
created_at: 2026-08-26
updated_at: 2026-08-26
source_as_of: 2026-08-26
source_ids: [SRC-005, SRC-008]
depends_on: [SCR-002]
supersedes: null
confidentiality: internal
---

# Due-diligence plan and deadline calculator

`DD-001` · due-diligence · service code `LND`

> **Parcel-specific.** Create one copy per candidate parcel under `working/candidate-parcels/<parcel-id>/`. Do not complete this template in place.

## Purpose

Sets the diligence scope, sequence, and — critically — the deadline arithmetic. Most diligence failures are not analytical; they are calendar failures where a contractual window closed while a third party still held the answer.

## When to use it

Immediately on offer acceptance, before any diligence spend.

## Required inputs

- Executed agreement or term sheet
- Diligence period length and its trigger event
- Third-party turnaround estimates

## Instructions

- Compute every deadline from the trigger event stated in the agreement, and record which clause defines the trigger. Diligence periods that run from 'the Effective Date' and from 'delivery of the title commitment' produce different calendars.
- Work backwards from the deadline to the order date for every third-party product. A survey ordered too late is a survey you do not have.
- `SRC-005` indicates title issues at closing roughly 30 days after signing and `SRC-008` indicates roughly four months application-to-close for City property. Both are indicative, not contractual — do not build a calendar on them.
- Identify the single deadline whose miss is unrecoverable and mark it. Usually it is the diligence expiry, after which the deposit is at risk.
- A condition not yet checked is recorded `not_found` or `blocked` — never `verified`, never blank.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Every deadline traced to a clause and a trigger event
- Every third-party product has an order-by date derived from the deadline
- The unrecoverable deadline identified
- Owners assigned for each workstream

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Sources

Requirements in this artifact trace to the following rows in `source-register.csv`. Re-verify before relying on any of them — agency requirements change without notice.

| Source | Document | Status | Pinpoint |
| --- | --- | --- | --- |
| `SRC-005` | Frequently Asked Questions | `verified` | Buyer eligibility list; deed and closing section; closing-cost estimates |
| `SRC-008` | Property Sales and Purchase FAQs | `verified` | Review-body list; conceptual plan requirement; market-value pricing; ~4-month timeline; 10% earnest money for commercial |

## Unresolved questions

- Does the diligence period run from execution or from delivery of a specified document?

## Approvals and professional review

- **Required reviewer: `michigan_licensed_attorney`.** `legal_review_required: true` — every stage gate this artifact feeds is blocked until that review is recorded in `GOV-015` (professional-review tracker).
- This document is an *issue-spotting tool*. It does not contain legal advice and must not be treated as a substitute for counsel.
- Record the reviewer, the date, and the scope reviewed. A review with no recorded scope does not clear the gate.

## Dependencies

**Upstream — this cannot be completed without:**

- `SCR-002` — Parcel comparison and go/no-go memo

**Downstream — these depend on this:**

- `DD-002` — Integrated parcel diligence checklist
- `DD-003` — Title request and review checklist
- `DD-004` — Exception-document register
- `DD-005` — Tax, assessment, water and municipal-charge review
- `DD-006` — Lien and encumbrance register
- `DD-007` — Survey RFP and review checklist
- `DD-008` — Boundary, easement, encroachment and access matrix
- `DD-009` — Parcel-combination checklist
- `DD-010` — Zoning confirmation memo
- `DD-011` — Dimensional and permitted-use matrix
- _…and 16 more (see `dependency-register.csv`)_

**Stage gates this is required evidence for:** `SG-04`

## Typst issue version expected?

**Yes.** A paired Typst issue document is expected before this leaves the project. Base template: `publication/typst/templates/report.typ`.

Transfer reviewed content to the `.typ` deliberately — there is no automatic Markdown→Typst conversion. The Markdown draft and the Typst issue share this `artifact_id`; the Typst metadata records the draft path and its SHA-256.

Compilation is not approval. See `publication/README.md` for the issue gate.
