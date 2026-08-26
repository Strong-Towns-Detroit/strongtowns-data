---
artifact_id: SCR-004
artifact_type: policy
title: Acquisition criteria definition
workstream: parcel-screening
service_code: LND
status: template
template_version: "1.0"
parcel_ids: []
owner_role: contractor_program_manager
decision_role: company_decision_authority
required_reviewer_role: company_decision_authority
legal_review_required: false
typst_issue_required: false
typst_source: null
latest_issue_id: null
created_at: 2026-08-26
updated_at: 2026-08-26
source_as_of: null
source_ids: []
depends_on: [SCR-003]
supersedes: null
confidentiality: internal
---

# Acquisition criteria definition

`SCR-004` · parcel-screening · service code `LND`

> **Reusable.** One copy project-wide, under `working/project-wide/`.

## Purpose

The screening criteria candidates are measured against: location, dimensions, zoning, utilities, setbacks, access, and comparables, per ICA Exhibit A.

## When to use it

Before screening begins. Revised only deliberately, never mid-comparison.

## Required inputs

- `SCR-003` owner's project requirements
- Buildable-envelope constraints
- Target finished value

## Instructions

- Derive criteria from the program. A criterion that does not trace to `SCR-003` is a personal preference.
- Separate hard filters (a parcel fails outright) from scored factors (a parcel is better or worse).
- Make each criterion decidable from evidence. 'Good location' is not a criterion; a stated travel-time or adjacency threshold is.
- Where the analytical pipeline can evaluate a criterion at parcel level, say which output does it — that keeps screening reproducible rather than impressionistic.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Every criterion is decidable from a stated evidence source
- Hard filters are separated from scored factors
- Criteria trace to the owner's project requirements
- The Company has agreed the criteria before screening begins

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Unresolved questions

_None recorded. Add any question that would change a decision if answered differently._

## Approvals and professional review

- **Required reviewer: `company_decision_authority`.** Record the review in `GOV-015` before this artifact is relied on at a gate.
- Conclusions reserved to that discipline must come from that professional, not from this document.

## Dependencies

**Upstream — this cannot be completed without:**

- `SCR-003` — Owner's project requirements brief

**Downstream — these depend on this:**

- `SCR-001` — Candidate-parcel dossier

**Stage gates this is required evidence for:** `SG-01`

## Typst issue version expected?

**No.** This artifact stays in Markdown. If it ever becomes an external submission, a stage-gate package, or a controlled-distribution PDF, update `typst_issue_required` in `artifact-register.csv` first — the register is the source of truth, not the file.
