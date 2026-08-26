---
artifact_id: CLO-019
artifact_type: memo
title: Lessons-learned memo
workstream: closing-compliance
service_code: ADM
status: template
template_version: "1.0"
parcel_ids: []
owner_role: contractor_program_manager
decision_role: company_decision_authority
required_reviewer_role: company_decision_authority
legal_review_required: false
typst_issue_required: true
typst_source: publication/typst/templates/memo.typ
latest_issue_id: null
created_at: 2026-08-26
updated_at: 2026-08-26
source_as_of: null
source_ids: []
depends_on: [CON-019]
supersedes: null
confidentiality: internal
---

# Lessons-learned memo

`CLO-019` · closing-compliance · service code `ADM`

> **Parcel-specific.** Create one copy per candidate parcel under `working/candidate-parcels/<parcel-id>/`. Do not complete this template in place.

## Purpose

Lessons-learned memo: what to do differently on the next parcel.

## When to use it

After completion, while the detail is still recoverable.

## Required inputs

- `GOV-007` decision log
- `GOV-009` risk register
- Variance history

## Instructions

- Compare what was assumed against what happened. `GOV-008` is the highest-value input — resolved assumptions are the cheapest lessons available.
- Record process failures, not just cost surprises. A deadline missed because it lived in two calendars is a fixable problem.
- Be specific enough to change behaviour. 'Communicate better' changes nothing.
- Issue as a Typst memo.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Assumptions compared against outcomes
- Process failures recorded alongside cost outcomes
- Recommendations specific enough to act on

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Sources

_No external requirements cited. If this artifact starts asserting one, add a row to `source-register.csv` first._

## Unresolved questions

_None recorded. Add any question that would change a decision if answered differently._

## Approvals and professional review

- **Required reviewer: `company_decision_authority`.** Record the review in `GOV-015` before this artifact is relied on at a gate.
- Conclusions reserved to that discipline must come from that professional, not from this document.

## Dependencies

**Upstream — this cannot be completed without:**

- `CON-019` — Final-completion coordination checklist


**Stage gates this is required evidence for:** `SG-12`

## Typst issue version expected?

**Yes.** A paired Typst issue document is expected before this leaves the project. Base template: `publication/typst/templates/memo.typ`.

Transfer reviewed content to the `.typ` deliberately — there is no automatic Markdown→Typst conversion. The Markdown draft and the Typst issue share this `artifact_id`; the Typst metadata records the draft path and its SHA-256.

Compilation is not approval. See `publication/README.md` for the issue gate.
