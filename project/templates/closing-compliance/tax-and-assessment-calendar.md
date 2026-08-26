---
artifact_id: CLO-007
artifact_type: calendar
title: Tax and assessment calendar
workstream: closing-compliance
service_code: ADM
status: template
template_version: "1.0"
parcel_ids: []
owner_role: contractor_program_manager
decision_role: company_decision_authority
required_reviewer_role: cpa_or_tax_advisor
legal_review_required: false
typst_issue_required: false
typst_source: null
latest_issue_id: null
created_at: 2026-08-26
updated_at: 2026-08-26
source_as_of: 2026-08-26
source_ids: [SRC-007, SRC-013]
depends_on: [ACQ-023]
supersedes: null
confidentiality: internal
---

# Tax and assessment calendar

`CLO-007` · closing-compliance · service code `ADM`

> **Parcel-specific.** Create one copy per candidate parcel under `working/candidate-parcels/<parcel-id>/`. Do not complete this template in place.

## Purpose

Calendar of tax and assessment dates following acquisition.

## When to use it

Immediately post-closing.

## Required inputs

- Recorded deed
- Assessment records
- Tax capture position

## Instructions

- Record the Property Transfer Affidavit obligation — `SRC-007` places it within 45 days for DLBA purchases. Missing it has assessment consequences.
- Calendar the DLBA five-year tax capture period where it applies, and any buy-out payment schedule under `SRC-013`.
- Calendar any abatement or exemption filing deadline from `FIN-007`.
- An unchecked condition is `not_found` or `blocked` — never `verified`, never blank.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Property Transfer Affidavit filed and evidenced
- Tax capture period calendared
- Abatement deadlines calendared
- CPA review recorded

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Sources

Requirements in this artifact trace to the following rows in `source-register.csv`. Re-verify before relying on any of them — agency requirements change without notice.

| Source | Document | Status | Pinpoint |
| --- | --- | --- | --- |
| `SRC-007` | Compliance | `verified` | Post-sale timeline table (15/45/60 day milestones); evidence rules; Release of Interest |
| `SRC-013` | First Amended Tax Capture Waiver Policy | `verified` | Sec. I (statutory basis MCL 211.7gg; waiver authority MCL 211.1025a(1)); Sec. II (governs over conflicting DLBA policy); Sec. III (application); Sec. IV(C) (Projects and Infill Housing Lots); Sec. IV(D) (de minimis); Sec. VI(A) (calculation) |

## Unresolved questions

_None recorded. Add any question that would change a decision if answered differently._

## Approvals and professional review

- **Required reviewer: `cpa_or_tax_advisor`.** Record the review in `GOV-015` before this artifact is relied on at a gate.
- Conclusions reserved to that discipline must come from that professional, not from this document.

## Dependencies

**Upstream — this cannot be completed without:**

- `ACQ-023` — Closing-conditions checklist


## Typst issue version expected?

**No.** This artifact stays in Markdown. If it ever becomes an external submission, a stage-gate package, or a controlled-distribution PDF, update `typst_issue_required` in `artifact-register.csv` first — the register is the source of truth, not the file.
