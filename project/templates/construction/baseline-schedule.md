---
artifact_id: CON-003
artifact_type: schedule
title: Baseline schedule
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
depends_on: [PRO-002]
supersedes: null
confidentiality: internal
---

# Baseline schedule

`CON-003` · construction · service code `EST`

> **Parcel-specific.** Create one copy per candidate parcel under `working/candidate-parcels/<parcel-id>/`. Do not complete this template in place.

## Purpose

The baseline construction schedule ICA §1.2 requires, including critical path, long-lead items and inspection milestones.

## When to use it

At notice to proceed; maintained through construction.

## Required inputs

- `PRO-002` bid schedules
- `APR-008` permit expiries
- `APR-009` inspection sequence
- `CON-004` long-lead register

## Instructions

- Exhibit A requires critical path, long-lead items, and inspection milestones explicitly. All three must be on the baseline, not added later.
- Place municipal inspections at their real sequence positions (`APR-009`) — they are constraints, not reporting events.
- Show permit expiry dates on the schedule. A permit lapsing mid-build is a schedule risk that is invisible unless drawn.
- Freeze the baseline. Updates go to `CON-008` as variance, not back into the baseline.
- ICA §7.2 makes the Company solely responsible for construction means, methods, sequencing, workmanship, field code compliance, and job site safety. Nothing here changes that.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Critical path identified
- Long-lead items and inspection milestones on the baseline
- Permit expiries shown
- Baseline frozen and approved

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

- `PRO-002` — Builder and general-contractor RFP

**Downstream — these depend on this:**

- `CON-004` — Long-lead register
- `CON-005` — Change-event and change-order log
- `CON-006` — Allowance and contingency log
- `CON-007` — Committed cost, actuals and cost-to-complete tracker
- `CON-008` — Schedule update and variance report
- `CON-009` — Weekly progress report
- `CON-010` — Constructability and value-engineering review
- `CON-011` — Value-engineering options register
- `CON-012` — Submittal log (Company-owned)
- `CON-013` — RFI log (Company-owned)
- _…and 7 more (see `dependency-register.csv`)_

**Stage gates this is required evidence for:** `SG-09`

## Typst issue version expected?

**Yes.** A paired Typst issue document is expected before this leaves the project. Base template: `publication/typst/templates/report.typ`.

Transfer reviewed content to the `.typ` deliberately — there is no automatic Markdown→Typst conversion. The Markdown draft and the Typst issue share this `artifact_id`; the Typst metadata records the draft path and its SHA-256.

Compilation is not approval. See `publication/README.md` for the issue gate.
