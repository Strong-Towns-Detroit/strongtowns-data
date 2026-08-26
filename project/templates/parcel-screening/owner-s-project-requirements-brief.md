---
artifact_id: SCR-003
artifact_type: brief
title: Owner's project requirements brief
workstream: parcel-screening
service_code: DSN
status: template
template_version: "1.0"
parcel_ids: []
owner_role: contractor_program_manager
decision_role: company_decision_authority
required_reviewer_role: company_decision_authority
legal_review_required: false
typst_issue_required: true
typst_source: publication/typst/templates/report.typ
latest_issue_id: null
created_at: 2026-08-26
updated_at: 2026-08-26
source_as_of: null
source_ids: []
depends_on: []
supersedes: null
confidentiality: internal
---

# Owner's project requirements brief

`SCR-003` · parcel-screening · service code `DSN`

> **Reusable.** One copy project-wide, under `working/project-wide/`.

## Purpose

Captures the Company's written program: what is being built, to what standard, for what budget, on what schedule. ICA §6 measures the Contractor's standard of care partly against this document, which makes getting it written down a protective act as well as a productive one.

## When to use it

At the outset, before parcel screening criteria are set. Revisited whenever the program changes.

## Required inputs

- Company's stated objectives
- Target market and finished-value expectations
- Budget envelope
- Schedule expectations
- Quality and specification level

## Instructions

- Get it in writing and get it agreed. §6 refers to 'Company's written program' — if no written program exists, the standard of care has no anchor.
- State what is fixed and what is negotiable. A program with no priorities cannot resolve a trade-off.
- Record the specification level explicitly. 'Good quality' is not a specification.
- Where the Company has not yet decided something, record it as an open question with a decision owner and a needed-by date — do not fill it in on their behalf.
- Changes to this document after design begins are Company-directed scope changes, billable under §6. Version it accordingly.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Program is written, dated, and agreed by the Company
- Fixed constraints are distinguished from preferences
- Every open item has a decision owner and a needed-by date
- Version history is intact so scope changes are provable

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Unresolved questions

- Has the Company agreed this document in writing, or has it only been discussed?

## Approvals and professional review

- **Required reviewer: `company_decision_authority`.** Record the review in `GOV-015` before this artifact is relied on at a gate.
- Conclusions reserved to that discipline must come from that professional, not from this document.

## Dependencies

**Upstream:** none. This is an entry point.

**Downstream — these depend on this:**

- `SCR-004` — Acquisition criteria definition
- `DSN-001` — Owner's project requirements
- `DSN-002` — Room and program schedule
- `DSN-003` — Site-planning criteria
- `DSN-004` — Accessibility goals
- `DSN-005` — Sustainability and energy goals
- `DSN-006` — Consultant scope matrix
- `DSN-007` — Concept-design review
- `DSN-008` — Zoning and code assumptions
- `DSN-009` — Preliminary code analysis
- _…and 5 more (see `dependency-register.csv`)_

**Stage gates this is required evidence for:** `SG-01`

## Typst issue version expected?

**Yes.** A paired Typst issue document is expected before this leaves the project. Base template: `publication/typst/templates/report.typ`.

Transfer reviewed content to the `.typ` deliberately — there is no automatic Markdown→Typst conversion. The Markdown draft and the Typst issue share this `artifact_id`; the Typst metadata records the draft path and its SHA-256.

Compilation is not approval. See `publication/README.md` for the issue gate.
