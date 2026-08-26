---
artifact_id: FIN-009
artifact_type: checklist
title: Appraisal request checklist
workstream: finance
service_code: EST
status: template
template_version: "1.0"
parcel_ids: []
owner_role: contractor_program_manager
decision_role: company_decision_authority
required_reviewer_role: lender_underwriter
legal_review_required: false
typst_issue_required: true
typst_source: publication/typst/templates/form-checklist.typ
latest_issue_id: null
created_at: 2026-08-26
updated_at: 2026-08-26
source_as_of: null
source_ids: []
depends_on: [FIN-001]
supersedes: null
confidentiality: sensitive
---

# Appraisal request checklist

`FIN-009` · finance · service code `EST`

> **Sensitive.** This blank template is tracked; every *completed* copy lives under `project/private/` and is never committed. Record no credentials, account numbers, signatures, government IDs, or personal financial information in it.

## Purpose

Checklist for requesting an appraisal, and for reading the one that comes back.

## When to use it

When a lender or the Company requires a valuation.

## Required inputs

- `SCR-007` screening estimate
- Parcel and design information

## Instructions

- `SCR-007` is a screening estimate by a construction program manager and is explicitly not an appraisal. This is where a licensed appraisal is obtained.
- Give the appraiser the design and specification level. An appraisal against the wrong specification is worse than none.
- Conclusions reserved to a licensed discipline come from that professional, not from this artifact.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Appraiser engaged with correct design and specification information
- Result compared against `SCR-007` with differences explained
- Appraisal review recorded

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Sources

_No external requirements cited. If this artifact starts asserting one, add a row to `source-register.csv` first._

## Unresolved questions

_None recorded. Add any question that would change a decision if answered differently._

## Approvals and professional review

- **Required reviewer: `lender_underwriter`.** Record the review in `GOV-015` before this artifact is relied on at a gate.
- Conclusions reserved to that discipline must come from that professional, not from this document.

## Dependencies

**Upstream — this cannot be completed without:**

- `FIN-001` — Cost plan


## Typst issue version expected?

**Yes.** A paired Typst issue document is expected before this leaves the project. Base template: `publication/typst/templates/form-checklist.typ`.

Transfer reviewed content to the `.typ` deliberately — there is no automatic Markdown→Typst conversion. The Markdown draft and the Typst issue share this `artifact_id`; the Typst metadata records the draft path and its SHA-256.

Compilation is not approval. See `publication/README.md` for the issue gate.
