---
artifact_id: ACQ-006
artifact_type: register
title: Parcel schedule and legal-description register
workstream: acquisition
service_code: LND
status: template
template_version: "1.0"
parcel_ids: []
owner_role: contractor_program_manager
decision_role: company_decision_authority
required_reviewer_role: licensed_surveyor
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

# Parcel schedule and legal-description register

`ACQ-006` · acquisition · service code `LND`

> **Parcel-specific.** Create one copy per candidate parcel under `working/candidate-parcels/<parcel-id>/`. Do not complete this template in place.

## Purpose

The authoritative schedule of parcels in a transaction, with legal descriptions as they will appear on the conveyance instrument.

## When to use it

Once a parcel or assemblage is identified and before any offer.

## Required inputs

- Parcel identifiers from the City catalog
- Legal descriptions from the deed or title commitment
- Survey, where one exists

## Instructions

- Take the legal description from the recorded instrument or the title commitment, never from the assessor record or a listing.
- Reproduce the parcel identifier exactly as the authoritative source writes it, trailing punctuation included.
- Where a discrepancy exists between the assessor description and the recorded description, record both and mark the condition `professional_review_required` — this is a surveyor and counsel question, not a transcription question.
- For an assemblage, schedule each parcel separately even where they will be combined; combination is a later, separate act.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Every parcel has a legal description traced to a recorded instrument or commitment
- Identifiers match the authoritative catalog character for character
- Discrepancies flagged rather than reconciled

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

- **Required reviewer: `licensed_surveyor`.** `legal_review_required: true` — every stage gate this artifact feeds is blocked until that review is recorded in `GOV-015` (professional-review tracker).
- This document is an *issue-spotting tool*. It does not contain legal advice and must not be treated as a substitute for counsel.
- Record the reviewer, the date, and the scope reviewed. A review with no recorded scope does not clear the gate.

## Dependencies

**Upstream — this cannot be completed without:**

- `ACQ-001` — Acquisition pathway decision tree


## Typst issue version expected?

**No.** This artifact stays in Markdown. If it ever becomes an external submission, a stage-gate package, or a controlled-distribution PDF, update `typst_issue_required` in `artifact-register.csv` first — the register is the source of truth, not the file.
