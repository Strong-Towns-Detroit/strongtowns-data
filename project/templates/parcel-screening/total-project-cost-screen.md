---
artifact_id: SCR-008
artifact_type: worksheet
title: Total project cost screen
workstream: parcel-screening
service_code: EST
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
depends_on: [SCR-006, SCR-007]
supersedes: null
confidentiality: internal
---

# Total project cost screen

`SCR-008` · parcel-screening · service code `EST`

> **Parcel-specific.** Create one copy per candidate parcel under `working/candidate-parcels/<parcel-id>/`. Do not complete this template in place.

## Purpose

Screens total project cost — acquisition, site work, construction, soft costs, and contingency — against estimated finished value, to decide whether a candidate is worth diligence spend.

## When to use it

Before authorising diligence expenditure on a candidate.

## Required inputs

- Acquisition cost or expected price
- `SCR-006` buildable envelope and resulting size
- Site work indications from the dossier
- `SCR-007` finished-value estimate
- Soft-cost and contingency assumptions

## Instructions

- Every line states its basis: quote, estimate, published figure, or placeholder. A placeholder that looks like an estimate is the single most common way a screen misleads.
- Carry contingency explicitly and size it to the confidence of the underlying lines. Low-confidence lines need more contingency, not more precision.
- State the margin as a range derived from the value range in `SCR-007`, not as a single number.
- Screening is not estimating. The full construction cost estimate is `FIN-001`/`CON-002` and comes later; this screen exists only to decide whether to spend on diligence.
- Where the screen is marginal, say so and name the two or three inputs that would resolve it.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Every line has a basis and a confidence
- Contingency is explicit and justified by the confidence profile
- Result is a range, not a point
- The document distinguishes itself from the full cost estimate

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Unresolved questions

- What margin threshold does the Company require before authorising diligence spend?

## Approvals and professional review

- **Required reviewer: `internal_peer`.** No licensed professional is required for this artifact.
- The Company still decides; the Contractor recommends (ICA §1.3).

## Dependencies

**Upstream — this cannot be completed without:**

- `SCR-006` — Buildable-envelope and site-yield worksheet
- `SCR-007` — Comparables and finished-value estimate

**Downstream — these depend on this:**

- `SCR-002` — Parcel comparison and go/no-go memo
- `FIN-001` — Cost plan

**Stage gates this is required evidence for:** `SG-02`

## Typst issue version expected?

**No.** This artifact stays in Markdown. If it ever becomes an external submission, a stage-gate package, or a controlled-distribution PDF, update `typst_issue_required` in `artifact-register.csv` first — the register is the source of truth, not the file.
