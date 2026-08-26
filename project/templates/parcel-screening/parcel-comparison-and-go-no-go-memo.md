---
artifact_id: SCR-002
artifact_type: memo
title: Parcel comparison and go/no-go memo
workstream: parcel-screening
service_code: LND
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
depends_on: [SCR-001, SCR-008]
supersedes: null
confidentiality: internal
---

# Parcel comparison and go/no-go memo

`SCR-002` · parcel-screening · service code `LND`

> **Parcel-specific.** Create one copy per candidate parcel under `working/candidate-parcels/<parcel-id>/`. Do not complete this template in place.

## Purpose

Compares qualified candidates against the Company's acquisition criteria and states a recommendation with its basis. Under ICA §1.2 this is a contractual deliverable: a written analysis and recommendation per candidate property.

## When to use it

Once two or more candidates have complete dossiers, or when a single candidate must be decided on.

## Required inputs

- `SCR-001` dossiers for each candidate
- `SCR-004` acquisition criteria
- `SCR-006` buildable envelope
- `SCR-007` finished-value estimate
- `SCR-008` total project cost screen

## Instructions

- Compare on the criteria in `SCR-004`. Introducing a new criterion at recommendation time means the criteria were wrong; fix `SCR-004` and say so.
- State the recommendation in one sentence at the top: acquire, do not acquire, or acquire subject to stated conditions.
- Show cost and value figures with their basis and confidence. An estimate presented without its basis will be read as a quote.
- Recommend; do not decide. ICA §1.3 reserves the acquisition decision to the Company.
- Where a candidate is rejected, record why in `GOV-007` — rejected options are the part that gets re-litigated later.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Every candidate scored against the same criteria
- Every figure carries a basis and a confidence
- The recommendation is stated in one sentence and separated from the analysis
- Conditions, if any, are individually verifiable

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Unresolved questions

_None recorded. Add any question that would change a decision if answered differently._

## Approvals and professional review

- **Required reviewer: `company_decision_authority`.** Record the review in `GOV-015` before this artifact is relied on at a gate.
- Conclusions reserved to that discipline must come from that professional, not from this document.

## Dependencies

**Upstream — this cannot be completed without:**

- `SCR-001` — Candidate-parcel dossier
- `SCR-008` — Total project cost screen

**Downstream — these depend on this:**

- `DD-001` — Due-diligence plan and deadline calculator

**Stage gates this is required evidence for:** `SG-02`

## Typst issue version expected?

**Yes.** A paired Typst issue document is expected before this leaves the project. Base template: `publication/typst/templates/memo.typ`.

Transfer reviewed content to the `.typ` deliberately — there is no automatic Markdown→Typst conversion. The Markdown draft and the Typst issue share this `artifact_id`; the Typst metadata records the draft path and its SHA-256.

Compilation is not approval. See `publication/README.md` for the issue gate.
