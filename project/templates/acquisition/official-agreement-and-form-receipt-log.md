---
artifact_id: ACQ-021
artifact_type: log
title: Official agreement and form receipt log
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
source_ids: [SRC-006]
depends_on: [ACQ-001]
supersedes: null
confidentiality: internal
---

# Official agreement and form receipt log

`ACQ-021` · acquisition · service code `LND`

> **Parcel-specific.** Create one copy per candidate parcel under `working/candidate-parcels/<parcel-id>/`. Do not complete this template in place.

## Purpose

Inventory of official agreements and forms received from a counterparty — what was received, in what version, when, and where the original is held.

## When to use it

On receipt of any agency or counterparty document.

## Required inputs

- Received documents

## Instructions

- Link and inventory. Never retype an official form into a project-authored document — a reconstructed official form is a forgery-shaped object regardless of intent.
- Record the version or revision marking on the document itself, not just the date received.
- Store the original as received.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Every received instrument inventoried with version and date
- Originals retained unaltered
- Nothing reconstructed

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Sources

Requirements in this artifact trace to the following rows in `source-register.csv`. Re-verify before relying on any of them — agency requirements change without notice.

| Source | Document | Status | Pinpoint |
| --- | --- | --- | --- |
| `SRC-006` | Policies and Procedures (index) | `verified` | Full list of 14 board-approved policy documents |

## Unresolved questions

_None recorded. Add any question that would change a decision if answered differently._

## Approvals and professional review

- **Required reviewer: `michigan_licensed_attorney`.** `legal_review_required: true` — every stage gate this artifact feeds is blocked until that review is recorded in `GOV-015` (professional-review tracker).
- This document is an *issue-spotting tool*. It does not contain legal advice and must not be treated as a substitute for counsel.
- Record the reviewer, the date, and the scope reviewed. A review with no recorded scope does not clear the gate.

## Dependencies

**Upstream — this cannot be completed without:**

- `ACQ-001` — Acquisition pathway decision tree


## Typst issue version expected?

**No.** This artifact stays in Markdown. If it ever becomes an external submission, a stage-gate package, or a controlled-distribution PDF, update `typst_issue_required` in `artifact-register.csv` first — the register is the source of truth, not the file.
