---
artifact_id: GOV-011
artifact_type: register
title: Contact and stakeholder register
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

# Contact and stakeholder register

`GOV-011` · governance · service code `ADM`

> **Reusable.** One copy project-wide, under `working/project-wide/`.

## Purpose

Directory of every party the project deals with: agency staff, utilities, counsel, surveyors, environmental and geotechnical consultants, title company, lender, and builders.

## When to use it

Whenever a new counterparty enters the project.

## Required inputs

- Correspondence
- Engagement records

## Instructions

- Record role and authority, not just contact details — who can actually decide matters more than who answers the phone.
- Record the single point of contact for any active solicitation (see the RFP template's contact restriction).
- Do not record credentials, account numbers, or any personal information beyond business contact details.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Every active counterparty has a named contact and a stated role
- No sensitive personal information is present

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
