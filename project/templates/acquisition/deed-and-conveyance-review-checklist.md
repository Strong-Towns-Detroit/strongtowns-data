---
artifact_id: ACQ-022
artifact_type: checklist
title: Deed and conveyance review checklist
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
typst_source: publication/typst/templates/form-checklist.typ
latest_issue_id: null
created_at: 2026-08-26
updated_at: 2026-08-26
source_as_of: 2026-08-26
source_ids: [SRC-005, SRC-007]
depends_on: [ACQ-001]
supersedes: null
confidentiality: internal
---

# Deed and conveyance review checklist

`ACQ-022` · acquisition · service code `LND`

> **Parcel-specific.** Create one copy per candidate parcel under `working/candidate-parcels/<parcel-id>/`. Do not complete this template in place.

## Purpose

Reviews the conveyance instrument before closing: what is being conveyed, with what warranties, subject to what.

## When to use it

On receipt of the draft deed, before closing.

## Required inputs

- Draft deed
- Title commitment
- `ACQ-006` legal descriptions

## Instructions

- DLBA conveys by Quit Claim Deed (`SRC-005`) — no warranty of title. Understand what the title commitment does and does not cure before closing on that basis.
- A Reconveyance Deed securing post-sale performance is part of the DLBA structure (`SRC-005`). Establish exactly what triggers it and how a Release of Interest is obtained (`SRC-007`).
- Verify the legal description on the deed against `ACQ-006` character by character.
- This is a counsel review. Record it in `GOV-015`.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Deed type and its warranty consequences understood and recorded
- Reconveyance trigger and release mechanism established
- Legal description verified against the parcel schedule
- Counsel review recorded

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Sources

Requirements in this artifact trace to the following rows in `source-register.csv`. Re-verify before relying on any of them — agency requirements change without notice.

| Source | Document | Status | Pinpoint |
| --- | --- | --- | --- |
| `SRC-005` | Frequently Asked Questions | `verified` | Buyer eligibility list; deed and closing section; closing-cost estimates |
| `SRC-007` | Compliance | `verified` | Post-sale timeline table (15/45/60 day milestones); evidence rules; Release of Interest |

## Unresolved questions

_None recorded. Add any question that would change a decision if answered differently._

## Approvals and professional review

- **Required reviewer: `michigan_licensed_attorney`.** `legal_review_required: true` — every stage gate this artifact feeds is blocked until that review is recorded in `GOV-015` (professional-review tracker).
- This document is an *issue-spotting tool*. It does not contain legal advice and must not be treated as a substitute for counsel.
- Record the reviewer, the date, and the scope reviewed. A review with no recorded scope does not clear the gate.

## Dependencies

**Upstream — this cannot be completed without:**

- `ACQ-001` — Acquisition pathway decision tree


**Stage gates this is required evidence for:** `SG-05`

## Typst issue version expected?

**Yes.** A paired Typst issue document is expected before this leaves the project. Base template: `publication/typst/templates/form-checklist.typ`.

Transfer reviewed content to the `.typ` deliberately — there is no automatic Markdown→Typst conversion. The Markdown draft and the Typst issue share this `artifact_id`; the Typst metadata records the draft path and its SHA-256.

Compilation is not approval. See `publication/README.md` for the issue gate.
