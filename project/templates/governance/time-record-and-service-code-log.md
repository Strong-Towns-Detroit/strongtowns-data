---
artifact_id: GOV-018
artifact_type: log
title: Time record and service-code log
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
confidentiality: sensitive
---

# Time record and service-code log

`GOV-018` · governance · service code `ADM`

> **Sensitive.** This blank template is tracked; every *completed* copy lives under
`project/private/` and is never committed. Record no credentials, account numbers,
signatures, government IDs, or personal financial information in it.

## Purpose

The contemporaneous time record supporting every hour invoiced. ICA §2.2 requires date, property, task, hours to the nearest quarter hour, and service code; §2.7 requires three-year retention.

## When to use it

Daily. Reconstructing a week from memory produces a record that cannot survive scrutiny.

## Required inputs

- Work performed
- Service code taxonomy: LND, DSN, PMT, INS, EST, ADM

## Instructions

- Record contemporaneously, to the nearest quarter hour.
- Every line names the property. Project-wide work is coded to a project-wide identifier, not left blank.
- Pick the service code from the artifact worked in — `artifact-register.csv` assigns one to every artifact.
- Retain for three years after the Term (§2.7).

## Completion criteria

This artifact is complete when **all** of the following hold:

- Every line has date, property, task, hours, and service code
- Hours reconcile to the invoice worksheet for the period

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Unresolved questions

- What identifier is used for project-wide, non-property time?

## Approvals and professional review

- **Required reviewer: `internal_peer`.** No licensed professional is required for this artifact.
- The Company still decides; the Contractor recommends (ICA §1.3).

## Dependencies

**Upstream:** none. This is an entry point.

**Downstream — these depend on this:**

- `GOV-019` — Semi-monthly invoice worksheet

## Typst issue version expected?

**No.** This artifact stays in Markdown. If it ever becomes an external submission, a stage-gate package, or a controlled-distribution PDF, update `typst_issue_required` in `artifact-register.csv` first — the register is the source of truth, not the file.
