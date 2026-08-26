---
artifact_id: SCR-006
artifact_type: worksheet
title: Buildable-envelope and site-yield worksheet
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

# Buildable-envelope and site-yield worksheet

`SCR-006` · parcel-screening · service code `LND`

> **Parcel-specific.** Create one copy per candidate parcel under `working/candidate-parcels/<parcel-id>/`. Do not complete this template in place.

## Purpose

Establishes what can actually be built on a parcel: the buildable envelope after setbacks, easements, access requirements, and dimensional standards are applied.

## When to use it

On every candidate that passes hard filters, before any cost or value estimate is attempted.

## Required inputs

- Parcel dimensions and shape
- Zoning dimensional standards (setbacks, height, lot coverage, FAR)
- Known easements and access requirements
- `SCR-003` program's dimensional needs

## Instructions

- Compute the envelope from the dimensional standards, then check the program fits inside it. Doing it the other way round produces a design that needs a variance nobody has agreed to seek.
- Treat unrecorded easements as an open risk, not as absent. An envelope computed before a survey is provisional and must say so.
- Where the program does not fit, state the gap precisely and the relief that would close it — that becomes the input to `DD-012` (variance issue brief).
- Any conclusion requiring interpretation of the zoning ordinance is flagged for the reviewer named on this artifact, not resolved here.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Envelope computed from cited dimensional standards
- Program fit stated as fits / does not fit / fits subject to named relief
- Provisional status is explicit where no survey exists
- Dimensional standards cited to a source with a retrieval date

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Unresolved questions

- Which dimensional standards are confirmed from the ordinance text rather than a summary table?

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
