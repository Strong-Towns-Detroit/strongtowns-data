---
artifact_id: SCR-001
artifact_type: dossier
title: Candidate-parcel dossier
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
depends_on: [SCR-004]
supersedes: null
confidentiality: internal
---

# Candidate-parcel dossier

`SCR-001` · parcel-screening · service code `LND`

> **Parcel-specific.** Create one copy per candidate parcel under `working/candidate-parcels/<parcel-id>/`. Do not complete this template in place.

## Purpose

The per-parcel fact base. Everything known about one candidate property, assembled once so that screening, diligence, design, and the acquisition recommendation all read from the same record.

## When to use it

On every parcel that survives initial filtering and is worth spending time on.

## Required inputs

- Parcel identifier and legal description from the City parcel catalog
- Assessor and tax records
- Zoning district and dimensional standards
- Utility availability indications
- Ownership and disposition path
- Accessibility outputs from the analytical pipeline (`data/derived/`), where available

## Instructions

- Record the parcel ID exactly as the authoritative source writes it — Detroit parcel identifiers carry a trailing period, and silently normalising it breaks joins against the pipeline outputs.
- Separate observed facts from inferences. An inference belongs in the assumption log with a resolving test.
- Cite the source for anything that could change: zoning, tax status, ownership, utility availability. Record the retrieval date.
- Do not copy conclusions from a listing or a broker. Record who asserted it and treat it as unverified until confirmed against a primary source.
- Where the analytical pipeline has produced accessibility results for this parcel, link them; do not restate the numbers, which go stale.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Parcel identifier matches the authoritative catalog exactly
- Ownership and disposition path identified
- Zoning district recorded with its source
- Every unverified assertion is flagged as such and has an owner

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Unresolved questions

- Is the parcel's disposition path confirmed by the owning entity, or inferred from the record?

## Approvals and professional review

- **Required reviewer: `internal_peer`.** No licensed professional is required for this artifact.
- The Company still decides; the Contractor recommends (ICA §1.3).

## Dependencies

**Upstream — this cannot be completed without:**

- `SCR-004` — Acquisition criteria definition

**Downstream — these depend on this:**

- `SCR-002` — Parcel comparison and go/no-go memo
- `SCR-005` — Candidate pipeline record
- `SCR-006` — Buildable-envelope and site-yield worksheet
- `SCR-007` — Comparables and finished-value estimate

**Stage gates this is required evidence for:** `SG-02`

## Typst issue version expected?

**No.** This artifact stays in Markdown. If it ever becomes an external submission, a stage-gate package, or a controlled-distribution PDF, update `typst_issue_required` in `artifact-register.csv` first — the register is the source of truth, not the file.
