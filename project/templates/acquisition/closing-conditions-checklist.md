---
artifact_id: ACQ-023
artifact_type: checklist
title: Closing-conditions checklist
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
source_ids: [SRC-005, SRC-008]
depends_on: [ACQ-001]
supersedes: null
confidentiality: internal
---

# Closing-conditions checklist

`ACQ-023` · acquisition · service code `LND`

> **Parcel-specific.** Create one copy per candidate parcel under `working/candidate-parcels/<parcel-id>/`. Do not complete this template in place.

## Purpose

Tracks every condition that must be satisfied before closing, with owner and evidence.

## When to use it

From offer acceptance to closing.

## Required inputs

- Executed agreement
- Diligence status
- Approval status

## Instructions

- List conditions from the agreement itself, not from a general template.
- `SRC-005` indicates title is issued at closing roughly 30 days after agreement signing; `SRC-008` indicates roughly four months from application to close for City-owned property. Treat both as indicative, not contractual.
- A condition with no owner will not be satisfied. A condition with no evidence requirement cannot be verified.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Every condition traced to a clause
- Every condition has an owner, a due date, and an evidence requirement
- No condition marked satisfied without evidence

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Sources

Requirements in this artifact trace to the following rows in `source-register.csv`. Re-verify before relying on any of them — agency requirements change without notice.

| Source | Document | Status | Pinpoint |
| --- | --- | --- | --- |
| `SRC-005` | Frequently Asked Questions | `verified` | Buyer eligibility list; deed and closing section; closing-cost estimates |
| `SRC-008` | Property Sales and Purchase FAQs | `verified` | Review-body list; conceptual plan requirement; market-value pricing; ~4-month timeline; 10% earnest money for commercial |

## Unresolved questions

_None recorded. Add any question that would change a decision if answered differently._

## Approvals and professional review

- **Required reviewer: `michigan_licensed_attorney`.** `legal_review_required: true` — every stage gate this artifact feeds is blocked until that review is recorded in `GOV-015` (professional-review tracker).
- This document is an *issue-spotting tool*. It does not contain legal advice and must not be treated as a substitute for counsel.
- Record the reviewer, the date, and the scope reviewed. A review with no recorded scope does not clear the gate.

## Dependencies

**Upstream — this cannot be completed without:**

- `ACQ-001` — Acquisition pathway decision tree

**Downstream — these depend on this:**

- `CLO-001` — Pre-closing authorization memo
- `CLO-002` — Funds-to-close checklist
- `CLO-003` — Closing-statement checklist
- `CLO-004` — Deed-recording tracker
- `CLO-005` — Title-policy and final-document tracker
- `CLO-006` — Closing binder
- `CLO-007` — Tax and assessment calendar
- `CLO-008` — Insurance binder checklist

**Stage gates this is required evidence for:** `SG-05`

## Typst issue version expected?

**Yes.** A paired Typst issue document is expected before this leaves the project. Base template: `publication/typst/templates/form-checklist.typ`.

Transfer reviewed content to the `.typ` deliberately — there is no automatic Markdown→Typst conversion. The Markdown draft and the Typst issue share this `artifact_id`; the Typst metadata records the draft path and its SHA-256.

Compilation is not approval. See `publication/README.md` for the issue gate.
