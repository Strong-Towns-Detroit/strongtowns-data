---
artifact_id: GOV-013
artifact_type: log
title: Correspondence log
workstream: governance
service_code: ADM
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
depends_on: []
supersedes: null
confidentiality: internal
---

# Correspondence log

`GOV-013` · governance · service code `ADM`

> **Reusable.** One copy project-wide, under `working/project-wide/`.

## Purpose

Chronological record of substantive correspondence with agencies, utilities, counterparties, and consultants.

## When to use it

Every substantive outbound or inbound communication that creates, changes, or evidences an obligation.

## Required inputs

- Email, portal messages, letters, call notes

## Instructions

- Log the fact and the substance, and store the artifact itself under the relevant working folder.
- A phone call that changes a requirement gets logged the same day, with who said it and their role — verbal guidance from agency staff is not a source, and must be confirmed in writing before it can be cited in `GOV-004`.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Every logged item points at a stored copy
- Verbal guidance is flagged as unconfirmed until written confirmation is received

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Unresolved questions

_None recorded. Add any question that would change a decision if answered differently._

## Approvals and professional review

- **Required reviewer: `internal_peer`.** No licensed professional is required for this artifact.
- The Company still decides; the Contractor recommends (ICA §1.3).

## Dependencies

**Upstream:** none. This is an entry point.


## Typst issue version expected?

**No.** This artifact stays in Markdown. If it ever becomes an external submission, a stage-gate package, or a controlled-distribution PDF, update `typst_issue_required` in `artifact-register.csv` first — the register is the source of truth, not the file.
