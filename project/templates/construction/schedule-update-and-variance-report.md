---
artifact_id: CON-008
artifact_type: report
title: Schedule update and variance report
workstream: construction
service_code: EST
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
depends_on: [CON-003]
supersedes: null
confidentiality: internal
---

# Schedule update and variance report

`CON-008` · construction · service code `EST`

> **Parcel-specific.** Create one copy per candidate parcel under `working/candidate-parcels/<parcel-id>/`. Do not complete this template in place.

## Purpose

Schedule update and variance report against baseline. ICA Exhibit A requires maintaining the master schedule, tracking actual progress against baseline, and proposing revisions.

## When to use it

Weekly, feeding `GOV-017`.

## Required inputs

- `CON-003` baseline
- Actual progress reported by the Company's builder

## Instructions

- Report progress **as reported by the Company's builder**. ICA §7.3 means the Contractor does not observe or verify field progress — the source of the progress data is the builder, and the report should say so.
- Report variance against baseline, and forecast completion. A schedule update with no forecast is a status, not a report.
- Propose revisions where the baseline is no longer achievable. Exhibit A requires proposing revisions, not silently re-baselining.
- ICA §7.2 makes the Company solely responsible for construction means, methods, sequencing, workmanship, field code compliance, and job site safety. Nothing here changes that.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Variance against the frozen baseline stated
- Forecast completion date given
- Source of progress data attributed to the builder
- Revisions proposed rather than absorbed

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

- `CON-003` — Baseline schedule

**Downstream — these depend on this:**

- `GOV-017` — Weekly status report

**Stage gates this is required evidence for:** `SG-10`

## Typst issue version expected?

**Yes.** A paired Typst issue document is expected before this leaves the project. Base template: `publication/typst/templates/report.typ`.

Transfer reviewed content to the `.typ` deliberately — there is no automatic Markdown→Typst conversion. The Markdown draft and the Typst issue share this `artifact_id`; the Typst metadata records the draft path and its SHA-256.

Compilation is not approval. See `publication/README.md` for the issue gate.
