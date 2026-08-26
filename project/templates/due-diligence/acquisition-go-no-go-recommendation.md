---
artifact_id: DD-027
artifact_type: recommendation
title: Acquisition go/no-go recommendation
workstream: due-diligence
service_code: LND
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
depends_on: [DD-001]
supersedes: null
confidentiality: internal
---

# Acquisition go/no-go recommendation

`DD-027` · due-diligence · service code `LND`

> **Parcel-specific.** Create one copy per candidate parcel under `working/candidate-parcels/<parcel-id>/`. Do not complete this template in place.

## Purpose

The acquisition go/no-go recommendation: proceed, withdraw, or proceed subject to stated conditions. Recommends; the Company decides.

## When to use it

At `SG-04`, once the red-flag memorandum is complete.

## Required inputs

- `DD-026` red-flag memorandum
- `DD-002` integrated checklist
- `SCR-008` cost screen
- `ACQ-017` term sheet

## Instructions

- State the recommendation in one sentence, then the basis.
- Every condition attached to a conditional recommendation must be individually verifiable and individually owned.
- A gate cannot pass while any required artifact is absent, any condition is silently unknown, any required professional review is missing, or any cited requirement lacks source support.
- ICA §1.3 reserves the decision to the Company. Record recommendation and decision separately in `GOV-007`.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Recommendation stated in one sentence
- Every condition verifiable and owned
- No condition silently unknown
- All required professional reviews recorded in `GOV-015`
- Typst issue compiled and visually inspected

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

- `DD-001` — Due-diligence plan and deadline calculator


**Stage gates this is required evidence for:** `SG-04`

## Typst issue version expected?

**Yes.** A paired Typst issue document is expected before this leaves the project. Base template: `publication/typst/templates/report.typ`.

Transfer reviewed content to the `.typ` deliberately — there is no automatic Markdown→Typst conversion. The Markdown draft and the Typst issue share this `artifact_id`; the Typst metadata records the draft path and its SHA-256.

Compilation is not approval. See `publication/README.md` for the issue gate.
