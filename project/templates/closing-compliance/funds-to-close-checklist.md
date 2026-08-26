---
artifact_id: CLO-002
artifact_type: checklist
title: Funds-to-close checklist
workstream: closing-compliance
service_code: LND
status: template
template_version: "1.0"
parcel_ids: []
owner_role: contractor_program_manager
decision_role: company_decision_authority
required_reviewer_role: michigan_licensed_attorney
legal_review_required: true
typst_issue_required: true
typst_source: publication/typst/templates/form-checklist.typ
latest_issue_id: null
created_at: 2026-08-26
updated_at: 2026-08-26
source_as_of: 2026-08-26
source_ids: [SRC-013]
depends_on: [ACQ-023]
supersedes: null
confidentiality: internal
---

# Funds-to-close checklist

`CLO-002` · closing-compliance · service code `LND`

> **Parcel-specific.** Create one copy per candidate parcel under `working/candidate-parcels/<parcel-id>/`. Do not complete this template in place.

## Purpose

Checklist of funds required to close and their sources.

## When to use it

Before closing.

## Required inputs

- Closing statement
- `FIN-002` sources and uses
- Deposit position `ACQ-018`

## Instructions

- Reconcile to the closing statement line by line. A funds checklist that does not tie to the statement will find its gap on closing day.
- Account for the deposit already held (`ACQ-018`) and any tax capture buy-out owed under `SRC-013` Sec. IV(C).
- Never record account or routing numbers. Record that funds are arranged and where confirmation is held.
- An unchecked condition is `not_found` or `blocked` — never `verified`, never blank.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Ties to the closing statement
- Deposit and any capture buy-out accounted for
- No payment credentials stored

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Sources

Requirements in this artifact trace to the following rows in `source-register.csv`. Re-verify before relying on any of them — agency requirements change without notice.

| Source | Document | Status | Pinpoint |
| --- | --- | --- | --- |
| `SRC-013` | First Amended Tax Capture Waiver Policy | `verified` | Sec. I (statutory basis MCL 211.7gg; waiver authority MCL 211.1025a(1)); Sec. II (governs over conflicting DLBA policy); Sec. III (application); Sec. IV(C) (Projects and Infill Housing Lots); Sec. IV(D) (de minimis); Sec. VI(A) (calculation) |

## Unresolved questions

_None recorded. Add any question that would change a decision if answered differently._

## Approvals and professional review

- **Required reviewer: `michigan_licensed_attorney`.** `legal_review_required: true` — every stage gate this artifact feeds is blocked until that review is recorded in `GOV-015` (professional-review tracker).
- This document is an *issue-spotting tool*. It does not contain legal advice and must not be treated as a substitute for counsel.
- Record the reviewer, the date, and the scope reviewed. A review with no recorded scope does not clear the gate.

## Dependencies

**Upstream — this cannot be completed without:**

- `ACQ-023` — Closing-conditions checklist


**Stage gates this is required evidence for:** `SG-05`

## Typst issue version expected?

**Yes.** A paired Typst issue document is expected before this leaves the project. Base template: `publication/typst/templates/form-checklist.typ`.

Transfer reviewed content to the `.typ` deliberately — there is no automatic Markdown→Typst conversion. The Markdown draft and the Typst issue share this `artifact_id`; the Typst metadata records the draft path and its SHA-256.

Compilation is not approval. See `publication/README.md` for the issue gate.
