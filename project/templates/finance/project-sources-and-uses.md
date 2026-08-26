---
artifact_id: FIN-002
artifact_type: worksheet
title: Project sources and uses
workstream: finance
service_code: EST
status: template
template_version: "1.0"
parcel_ids: []
owner_role: contractor_program_manager
decision_role: company_decision_authority
required_reviewer_role: cpa_or_tax_advisor
legal_review_required: false
typst_issue_required: true
typst_source: publication/typst/templates/report.typ
latest_issue_id: null
created_at: 2026-08-26
updated_at: 2026-08-26
source_as_of: 2026-08-26
source_ids: [SRC-001]
depends_on: [FIN-001]
supersedes: null
confidentiality: sensitive
---

# Project sources and uses

`FIN-002` · finance · service code `EST`

> **Sensitive.** This blank template is tracked; every *completed* copy lives under `project/private/` and is never committed. Record no credentials, account numbers, signatures, government IDs, or personal financial information in it.

## Purpose

Project sources and uses: where the money comes from and where it goes.

## When to use it

With the cost plan; required by most application pathways.

## Required inputs

- `FIN-001` cost plan
- Financing evidence
- Equity commitment

## Instructions

- Uses must reconcile to `FIN-001` exactly. A sources and uses that does not tie to the cost plan is two documents disagreeing in public.
- Include acquisition, diligence spend already incurred (`DD-025`), soft costs, and the tax capture buy-out.
- `SRC-001` Ch. VI(C)(3) requires demonstrated capacity to finance AND complete. Sources must cover completion, not just acquisition.
- Every figure states its basis (quote, estimate, published figure, placeholder) and a confidence. A placeholder that looks like an estimate is how a cost plan misleads.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Uses tie to `FIN-001`
- Sources cover completion, not just acquisition
- Every source evidenced
- No credentials or account numbers recorded

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Sources

Requirements in this artifact trace to the following rows in `source-register.csv`. Re-verify before relying on any of them — agency requirements change without notice.

| Source | Document | Status | Pinpoint |
| --- | --- | --- | --- |
| `SRC-001` | Second Amended and Restated Vacant Land Policy | `verified` | Ch. VI (Infill Housing Lots), pp.16-18; Ch. VIII (Land-Based Projects) pp.21-23; Ch. IX (Land Review Areas) pp.24-25 |

## Unresolved questions

_None recorded. Add any question that would change a decision if answered differently._

## Approvals and professional review

- **Required reviewer: `cpa_or_tax_advisor`.** Record the review in `GOV-015` before this artifact is relied on at a gate.
- Conclusions reserved to that discipline must come from that professional, not from this document.

## Dependencies

**Upstream — this cannot be completed without:**

- `FIN-001` — Cost plan


**Stage gates this is required evidence for:** `SG-07`

## Typst issue version expected?

**Yes.** A paired Typst issue document is expected before this leaves the project. Base template: `publication/typst/templates/report.typ`.

Transfer reviewed content to the `.typ` deliberately — there is no automatic Markdown→Typst conversion. The Markdown draft and the Typst issue share this `artifact_id`; the Typst metadata records the draft path and its SHA-256.

Compilation is not approval. See `publication/README.md` for the issue gate.
