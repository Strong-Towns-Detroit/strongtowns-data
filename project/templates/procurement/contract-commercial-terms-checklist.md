---
artifact_id: PRO-008
artifact_type: checklist
title: Contract commercial-terms checklist
workstream: procurement
service_code: EST
status: template
template_version: "1.0"
parcel_ids: []
owner_role: contractor_program_manager
decision_role: company_decision_authority
required_reviewer_role: michigan_licensed_attorney
legal_review_required: true
typst_issue_required: true
typst_source: publication/typst/templates/form-checklist.typ
latest_issue_id: null
created_at: 2026-08-26
updated_at: 2026-08-26
source_as_of: null
source_ids: []
depends_on: [DSN-012]
supersedes: null
confidentiality: internal
---

# Contract commercial-terms checklist

`PRO-008` · procurement · service code `EST`

> **Parcel-specific.** Create one copy per candidate parcel under `working/candidate-parcels/<parcel-id>/`. Do not complete this template in place.

## Purpose

Checklist of commercial terms to settle in a construction or consultant agreement. An issue list for counsel — not an agreement.

## When to use it

Before any agreement is signed.

## Required inputs

- Draft agreement from the counterparty
- `PRO-005` levelled bid

## Instructions

- Work the commercial issues: scope, price basis, allowances, contingency, schedule and liquidated damages, payment and retainage, change procedure, lien waivers, insurance and indemnity, warranty, termination, and dispute resolution.
- Do not draft the agreement. ICA §7 keeps construction contracting with the Company; this artifact spots issues for counsel.
- Where the Company's builder proposes its own form, inventory and link it (`ACQ-021`) rather than recreating it.
- Every issue marked acceptable, negotiate, or refer to counsel.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Every commercial issue addressed
- Nothing drafted as an operative agreement
- Every issue marked with a disposition
- Counsel review recorded in `GOV-015`

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Sources

_No external requirements cited. If this artifact starts asserting one, add a row to `source-register.csv` first._

## Unresolved questions

_None recorded. Add any question that would change a decision if answered differently._

## Approvals and professional review

- **Required reviewer: `michigan_licensed_attorney`.** `legal_review_required: true` — every stage gate this artifact feeds is blocked until that review is recorded in `GOV-015` (professional-review tracker).
- This document is an *issue-spotting tool*. It does not contain legal advice and must not be treated as a substitute for counsel.
- Record the reviewer, the date, and the scope reviewed. A review with no recorded scope does not clear the gate.

## Dependencies

**Upstream — this cannot be completed without:**

- `DSN-012` — Design deliverables register


## Typst issue version expected?

**Yes.** A paired Typst issue document is expected before this leaves the project. Base template: `publication/typst/templates/form-checklist.typ`.

Transfer reviewed content to the `.typ` deliberately — there is no automatic Markdown→Typst conversion. The Markdown draft and the Typst issue share this `artifact_id`; the Typst metadata records the draft path and its SHA-256.

Compilation is not approval. See `publication/README.md` for the issue gate.
