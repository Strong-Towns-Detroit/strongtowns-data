---
artifact_id: ACQ-016
artifact_type: tracker
title: Board-approval tracker
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
source_ids: [SRC-001, SRC-003, SRC-004]
depends_on: [ACQ-001]
supersedes: null
confidentiality: internal
---

# Board-approval tracker

`ACQ-016` · acquisition · service code `LND`

> **Parcel-specific.** Create one copy per candidate parcel under `working/candidate-parcels/<parcel-id>/`. Do not complete this template in place.

## Purpose

Tracks whether a given disposition actually requires Board approval, and if so its status through the Board calendar.

## When to use it

Once a pathway is selected.

## Required inputs

- The pathway's governing policy
- DLBA Board meeting calendar

## Instructions

- Establish first whether Board approval is required at all. This is contested in the sources: `SRC-003` and `SRC-004` state Board approval at a monthly public meeting; `SRC-001` Introduction p.iii states that sales of Oversize, Neighborhood, Infill Housing and Homestead Lots in accordance with the policy no longer require Board approval.
- The adopted policy is the later and more authoritative instrument, but the conflict is recorded rather than resolved. Confirm with the DLBA which applies to the specific pathway before relying on either.
- Where Board approval IS required, track the meeting date, the agenda posting, and the resolution number.
- A Board calendar slip is a schedule risk. Log it in `GOV-009`.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Whether Board approval is required is established from the governing policy and confirmed with the DLBA
- The conflict between the web pages and the adopted policy is recorded, not silently resolved
- Where required, meeting date and resolution recorded

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Sources

Requirements in this artifact trace to the following rows in `source-register.csv`. Re-verify before relying on any of them — agency requirements change without notice.

| Source | Document | Status | Pinpoint |
| --- | --- | --- | --- |
| `SRC-001` | Second Amended and Restated Vacant Land Policy | `verified` | Ch. VI (Infill Housing Lots), pp.16-18; Ch. VIII (Land-Based Projects) pp.21-23; Ch. IX (Land Review Areas) pp.24-25 |
| `SRC-003` | Purchase Property (program overview) | `conflicting` | Program tiles: Auction, Own It Now, Rehabbed & Ready, Marketed Properties, Side Lots, Neighborhood Lots, Purchase Property by Application |
| `SRC-004` | Development Projects / Create-a-Project | `conflicting` | Three-step process; 2-4 week callback statement; Board approval statement |

## Unresolved questions

- Does Board approval apply to Infill Housing Lot sales? `SRC-001` and `SRC-003`/`SRC-004` disagree. Unresolved.

## Approvals and professional review

- **Required reviewer: `michigan_licensed_attorney`.** `legal_review_required: true` — every stage gate this artifact feeds is blocked until that review is recorded in `GOV-015` (professional-review tracker).
- This document is an *issue-spotting tool*. It does not contain legal advice and must not be treated as a substitute for counsel.
- Record the reviewer, the date, and the scope reviewed. A review with no recorded scope does not clear the gate.

## Dependencies

**Upstream — this cannot be completed without:**

- `ACQ-001` — Acquisition pathway decision tree


## Typst issue version expected?

**No.** This artifact stays in Markdown. If it ever becomes an external submission, a stage-gate package, or a controlled-distribution PDF, update `typst_issue_required` in `artifact-register.csv` first — the register is the source of truth, not the file.
