---
artifact_id: FIN-005
artifact_type: comparison
title: Financing comparison
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
typst_source: publication/typst/templates/report.typ
latest_issue_id: null
created_at: 2026-08-26
updated_at: 2026-08-26
source_as_of: null
source_ids: []
depends_on: [FIN-001]
supersedes: null
confidentiality: sensitive
---

# Financing comparison

`FIN-005` · finance · service code `EST`

> **Sensitive.** This blank template is tracked; every *completed* copy lives under `project/private/` and is never committed. Record no credentials, account numbers, signatures, government IDs, or personal financial information in it.

## Purpose

Comparison of financing options on cost, timing, conditions, and what each requires of the project.

## When to use it

Before committing to a lender.

## Required inputs

- Term sheets
- `FIN-004` cash-flow forecast

## Instructions

- Compare total cost including fees, not headline rate.
- Record what each option requires of the project — draw inspections, completion deadlines, personal guarantees. Those constrain the build, not just the balance sheet.
- This is not lending advice. A lender or broker reviews it.
- Conclusions reserved to a licensed discipline come from that professional, not from this artifact.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Options compared on total cost and on project constraints
- Conditions recorded, not just pricing
- Professional review recorded

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

**Yes.** A paired Typst issue document is expected before this leaves the project. Base template: `publication/typst/templates/report.typ`.

Transfer reviewed content to the `.typ` deliberately — there is no automatic Markdown→Typst conversion. The Markdown draft and the Typst issue share this `artifact_id`; the Typst metadata records the draft path and its SHA-256.

Compilation is not approval. See `publication/README.md` for the issue gate.
