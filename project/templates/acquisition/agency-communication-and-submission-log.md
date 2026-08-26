---
artifact_id: ACQ-015
artifact_type: log
title: Agency communication and submission log
workstream: acquisition
service_code: LND
status: template
template_version: "1.0"
parcel_ids: []
owner_role: contractor_program_manager
decision_role: company_decision_authority
required_reviewer_role: internal_peer
legal_review_required: false
typst_issue_required: false
typst_source: null
latest_issue_id: null
created_at: 2026-08-26
updated_at: 2026-08-26
source_as_of: 2026-08-26
source_ids: [SRC-004]
depends_on: [ACQ-001]
supersedes: null
confidentiality: internal
---

# Agency communication and submission log

`ACQ-015` · acquisition · service code `LND`

> **Parcel-specific.** Create one copy per candidate parcel under `working/candidate-parcels/<parcel-id>/`. Do not complete this template in place.

## Purpose

Chronological record of every communication with the DLBA or City regarding a parcel or application, and of everything submitted.

## When to use it

Continuously from first contact.

## Required inputs

- Emails, portal confirmations, call notes

## Instructions

- `SRC-004` states an applicant can expect a call from a DLBA representative within 2-4 weeks if the DLBA owns the property. Log the application date so that window is measurable and chaseable.
- Verbal guidance from staff is not a citable source. Log it, then seek written confirmation before it informs a decision.
- Retain a copy of every submitted package as sent.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Every contact logged with date, participant, and substance
- Verbal guidance flagged as unconfirmed
- Submitted packages retained

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Sources

Requirements in this artifact trace to the following rows in `source-register.csv`. Re-verify before relying on any of them — agency requirements change without notice.

| Source | Document | Status | Pinpoint |
| --- | --- | --- | --- |
| `SRC-004` | Development Projects / Create-a-Project | `conflicting` | Three-step process; 2-4 week callback statement; Board approval statement |

## Unresolved questions

_None recorded. Add any question that would change a decision if answered differently._

## Approvals and professional review

- **Required reviewer: `internal_peer`.** No licensed professional is required for this artifact.
- The Company still decides; the Contractor recommends (ICA §1.3).

## Dependencies

**Upstream — this cannot be completed without:**

- `ACQ-001` — Acquisition pathway decision tree


## Typst issue version expected?

**No.** This artifact stays in Markdown. If it ever becomes an external submission, a stage-gate package, or a controlled-distribution PDF, update `typst_issue_required` in `artifact-register.csv` first — the register is the source of truth, not the file.
