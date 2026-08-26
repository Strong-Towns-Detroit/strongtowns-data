---
artifact_id: APR-004
artifact_type: checklist
title: Variance submission checklist
workstream: approvals
service_code: PMT
status: template
template_version: "1.0"
parcel_ids: []
owner_role: contractor_program_manager
decision_role: company_decision_authority
required_reviewer_role: michigan_licensed_attorney
legal_review_required: true
typst_issue_required: true
typst_source: publication/typst/templates/application-package.typ
latest_issue_id: null
created_at: 2026-08-26
updated_at: 2026-08-26
source_as_of: 2026-08-26
source_ids: [SRC-016, SRC-014]
depends_on: [APR-001]
supersedes: null
confidentiality: internal
---

# Variance submission checklist

`APR-004` · approvals · service code `PMT`

> **Parcel-specific.** Create one copy per candidate parcel under `working/candidate-parcels/<parcel-id>/`. Do not complete this template in place.

## Purpose

Checklist for a variance, rezoning or zoning appeal submission.

## When to use it

When `DD-012` establishes that relief is needed.

## Required inputs

- `DD-012` variance issue brief
- `SRC-016` Zoning/Special Land Use division
- Submission requirements

## Instructions

- Zoning/Special Land Use conducts site plan review and public hearings for conditional land uses (`SRC-016`). Establish which process applies — variance, conditional use, rezoning, or appeal — before assembling anything.
- Note the option-agreement mechanism in `SRC-014` Sec. III(A)(2): on the Projects pathway, DLBA may grant an option while a purchaser pursues rezoning, a variance, or an appeal. That converts a zoning problem into a priced, time-boxed risk rather than a disqualifier.
- A hearing date is a schedule event with a lead time. Get it on `CON-003` as soon as it exists.
- Conclusions reserved to a licensed discipline come from that professional, not from this artifact.
- An unchecked condition is `not_found` or `blocked` — never `verified`, never blank.

## Completion criteria

This artifact is complete when **all** of the following hold:

- The correct relief process identified
- Submission assembled against the authority's actual requirements
- Hearing lead time reflected in the schedule
- Counsel review recorded in `GOV-015`

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Sources

Requirements in this artifact trace to the following rows in `source-register.csv`. Re-verify before relying on any of them — agency requirements change without notice.

| Source | Document | Status | Pinpoint |
| --- | --- | --- | --- |
| `SRC-016` | Buildings, Safety Engineering and Environmental Department (divisions index) | `verified` | Division list and responsibilities |
| `SRC-014` | Neighborhood Development Projects Policy (Procedures Governing the Disposition of Properties to Support City of Detroit Economic Development Projects) | `verified` | Sec. II (Qualified Properties); Sec. III(A) (zoning gate and option agreement); Sec. III(B)(1) (option deposit); Sec. III(C) (FMV, 12-month price expiry); Sec. III(C)(3)(b) (pricing credits); Sec. V(A)-(B) (approval thresholds) |

## Unresolved questions

_None recorded. Add any question that would change a decision if answered differently._

## Approvals and professional review

- **Required reviewer: `michigan_licensed_attorney`.** `legal_review_required: true` — every stage gate this artifact feeds is blocked until that review is recorded in `GOV-015` (professional-review tracker).
- This document is an *issue-spotting tool*. It does not contain legal advice and must not be treated as a substitute for counsel.
- Record the reviewer, the date, and the scope reviewed. A review with no recorded scope does not clear the gate.

## Dependencies

**Upstream — this cannot be completed without:**

- `APR-001` — Permit and approval matrix


## Typst issue version expected?

**Yes.** A paired Typst issue document is expected before this leaves the project. Base template: `publication/typst/templates/application-package.typ`.

Transfer reviewed content to the `.typ` deliberately — there is no automatic Markdown→Typst conversion. The Markdown draft and the Typst issue share this `artifact_id`; the Typst metadata records the draft path and its SHA-256.

Compilation is not approval. See `publication/README.md` for the issue gate.
