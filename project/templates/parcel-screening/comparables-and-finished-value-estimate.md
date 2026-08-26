---
artifact_id: SCR-007
artifact_type: worksheet
title: Comparables and finished-value estimate
workstream: parcel-screening
service_code: LND
status: template
template_version: "1.0"
parcel_ids: []
owner_role: contractor_program_manager
decision_role: company_decision_authority
required_reviewer_role: internal_peer
legal_review_required: false
typst_issue_required: false
typst_source: null
latest_issue_id: null
created_at: 2026-08-26
updated_at: 2026-08-26
source_as_of: null
source_ids: []
depends_on: [SCR-001]
supersedes: null
confidentiality: internal
---

# Comparables and finished-value estimate

`SCR-007` · parcel-screening · service code `LND`

> **Parcel-specific.** Create one copy per candidate parcel under `working/candidate-parcels/<parcel-id>/`. Do not complete this template in place.

## Purpose

Estimates the finished value of the completed home, from comparables, to support the total project cost screen and the acquisition recommendation.

## When to use it

On candidates that have a buildable envelope and a program fit.

## Required inputs

- Recent comparable sales
- `SCR-003` program specification level
- `SCR-006` buildable envelope and resulting size

## Instructions

- Use closed sales, not listings. A listing is an asking price and evidences nothing.
- Record each comparable's address, sale date, size, and condition, and state the adjustment applied. An unadjusted comparable is not a comparable.
- State the confidence and the range, not a single number. A point estimate implies a precision this method does not have.
- This is a screening estimate by a construction program manager. It is not an appraisal and must not be presented as one; where a lender or the Company needs a valuation, that goes to a licensed appraiser via `FIN-009`.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Every comparable has address, date, size, condition, and stated adjustment
- Result is stated as a range with a confidence
- The document states on its face that it is not an appraisal

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Unresolved questions

- Does the Company require a licensed appraisal at this stage, or is a screening estimate sufficient?

## Approvals and professional review

- **Required reviewer: `internal_peer`.** No licensed professional is required for this artifact.
- The Company still decides; the Contractor recommends (ICA §1.3).

## Dependencies

**Upstream — this cannot be completed without:**

- `SCR-001` — Candidate-parcel dossier

**Downstream — these depend on this:**

- `SCR-008` — Total project cost screen

**Stage gates this is required evidence for:** `SG-02`

## Typst issue version expected?

**No.** This artifact stays in Markdown. If it ever becomes an external submission, a stage-gate package, or a controlled-distribution PDF, update `typst_issue_required` in `artifact-register.csv` first — the register is the source of truth, not the file.
