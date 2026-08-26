---
artifact_id: CLO-015
artifact_type: request
title: Extension and waiver request
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
typst_source: publication/typst/templates/letter.typ
latest_issue_id: null
created_at: 2026-08-26
updated_at: 2026-08-26
source_as_of: 2026-08-26
source_ids: [SRC-007, SRC-013]
depends_on: [CON-019]
supersedes: null
confidentiality: internal
---

# Extension and waiver request

`CLO-015` · closing-compliance · service code `LND`

> **Parcel-specific.** Create one copy per candidate parcel under `working/candidate-parcels/<parcel-id>/`. Do not complete this template in place.

## Purpose

Request to an agency for an extension or waiver of a compliance deadline.

## When to use it

As soon as a deadline looks at risk — not after it passes.

## Required inputs

- `CLO-011` obligation matrix
- Evidence of progress
- Reason for the request

## Instructions

- Ask early. `SRC-007` publishes no extension or waiver procedure and states only that owners concerned about progress should communicate barriers to their Compliance Representative. That the procedure is unpublished is a finding, not a reason to wait.
- State the barrier, the revised date, and what has already been done. A request with no evidence of progress is a request to be refused.
- Note that `SRC-013` Sec. IV establishes an appeal route to the DLBA Board for tax capture waiver denials — once per property. Whether an analogous route exists for compliance deadlines is unknown.
- Issue as a Typst letter and log in `GOV-013`.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Request made before the deadline passes
- Progress evidenced
- Revised date stated with a basis
- Letter logged and copy retained

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Sources

Requirements in this artifact trace to the following rows in `source-register.csv`. Re-verify before relying on any of them — agency requirements change without notice.

| Source | Document | Status | Pinpoint |
| --- | --- | --- | --- |
| `SRC-007` | Compliance | `verified` | Post-sale timeline table (15/45/60 day milestones); evidence rules; Release of Interest |
| `SRC-013` | First Amended Tax Capture Waiver Policy | `verified` | Sec. I (statutory basis MCL 211.7gg; waiver authority MCL 211.1025a(1)); Sec. II (governs over conflicting DLBA policy); Sec. III (application); Sec. IV(C) (Projects and Infill Housing Lots); Sec. IV(D) (de minimis); Sec. VI(A) (calculation) |

## Unresolved questions

- What is the DLBA's actual procedure for requesting an extension or waiver of a compliance deadline? Unpublished on `SRC-007`.

## Approvals and professional review

- **Required reviewer: `michigan_licensed_attorney`.** `legal_review_required: true` — every stage gate this artifact feeds is blocked until that review is recorded in `GOV-015` (professional-review tracker).
- This document is an *issue-spotting tool*. It does not contain legal advice and must not be treated as a substitute for counsel.
- Record the reviewer, the date, and the scope reviewed. A review with no recorded scope does not clear the gate.

## Dependencies

**Upstream — this cannot be completed without:**

- `CON-019` — Final-completion coordination checklist


## Typst issue version expected?

**Yes.** A paired Typst issue document is expected before this leaves the project. Base template: `publication/typst/templates/letter.typ`.

Transfer reviewed content to the `.typ` deliberately — there is no automatic Markdown→Typst conversion. The Markdown draft and the Typst issue share this `artifact_id`; the Typst metadata records the draft path and its SHA-256.

Compilation is not approval. See `publication/README.md` for the issue gate.
