---
artifact_id: FIN-006
artifact_type: checklist
title: Lender checklist
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

# Lender checklist

`FIN-006` · finance · service code `EST`

> **Sensitive.** This blank template is tracked; every *completed* copy lives under `project/private/` and is never committed. Record no credentials, account numbers, signatures, government IDs, or personal financial information in it.

## Purpose

Checklist of what a lender will require, assembled before they ask.

## When to use it

Before approaching a lender.

## Required inputs

- Lender's published requirements
- `FIN-002` sources and uses

## Instructions

- Assemble against the lender's actual list. Do not reconstruct it from a template.
- Never store account numbers, statements, or credentials here. Record that a document exists and where the original is held.
- An unchecked condition is `not_found` or `blocked` — never `verified`, never blank.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Every requirement traced to the lender's own list
- No sensitive financial data stored in-repo
- Gaps marked `blocked`

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
