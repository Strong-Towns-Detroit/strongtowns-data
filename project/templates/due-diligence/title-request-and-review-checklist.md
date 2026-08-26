---
artifact_id: DD-003
artifact_type: checklist
title: Title request and review checklist
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
typst_source: publication/typst/templates/form-checklist.typ
latest_issue_id: null
created_at: 2026-08-26
updated_at: 2026-08-26
source_as_of: 2026-08-26
source_ids: [SRC-005, SRC-009]
depends_on: [DD-001]
supersedes: null
confidentiality: internal
---

# Title request and review checklist

`DD-003` · due-diligence · service code `LND`

> **Parcel-specific.** Create one copy per candidate parcel under `working/candidate-parcels/<parcel-id>/`. Do not complete this template in place.

## Purpose

Orders and reviews the title commitment — the foundational diligence product, since everything about what can be built rests on what is actually owned.

## When to use it

As early as possible; it gates the exception review, the survey scope, and the lien register.

## Required inputs

- `ACQ-006` parcel schedule and legal descriptions
- Title company engagement

## Instructions

- Order against the legal description from the recorded instrument, not the assessor record.
- DLBA conveys by Quit Claim Deed (`SRC-005`) — no warranty of title. What the commitment cures, and at what cost, is therefore the whole question, not a formality.
- `SRC-009` states marketed DLBA properties have clear title; that is a marketing statement, not a title opinion. Verify.
- Read the requirements schedule as carefully as the exceptions schedule. Requirements are what must happen before the policy issues.
- Any conclusion reserved to a licensed discipline comes from that professional, not from this artifact.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Commitment obtained against the correct legal description
- Every requirement and exception logged into `DD-004`
- Deed type and its warranty consequences recorded
- Counsel review recorded in `GOV-015`

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Sources

Requirements in this artifact trace to the following rows in `source-register.csv`. Re-verify before relying on any of them — agency requirements change without notice.

| Source | Document | Status | Pinpoint |
| --- | --- | --- | --- |
| `SRC-005` | Frequently Asked Questions | `verified` | Buyer eligibility list; deed and closing section; closing-cost estimates |
| `SRC-009` | Marketing Programs (marketed properties) | `verified` | 60-day listing; ~90 days to close; scoring categories; six proposal-guideline categories including New Build Opportunities |

## Unresolved questions

- What will the title company insure over, and at what premium?

## Approvals and professional review

- **Required reviewer: `michigan_licensed_attorney`.** `legal_review_required: true` — every stage gate this artifact feeds is blocked until that review is recorded in `GOV-015` (professional-review tracker).
- This document is an *issue-spotting tool*. It does not contain legal advice and must not be treated as a substitute for counsel.
- Record the reviewer, the date, and the scope reviewed. A review with no recorded scope does not clear the gate.

## Dependencies

**Upstream — this cannot be completed without:**

- `DD-001` — Due-diligence plan and deadline calculator


## Typst issue version expected?

**Yes.** A paired Typst issue document is expected before this leaves the project. Base template: `publication/typst/templates/form-checklist.typ`.

Transfer reviewed content to the `.typ` deliberately — there is no automatic Markdown→Typst conversion. The Markdown draft and the Typst issue share this `artifact_id`; the Typst metadata records the draft path and its SHA-256.

Compilation is not approval. See `publication/README.md` for the issue gate.
