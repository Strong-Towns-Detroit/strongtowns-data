---
artifact_id: FIN-001
artifact_type: plan
title: Cost plan
workstream: finance
service_code: EST
status: template
template_version: "1.0"
parcel_ids: []
owner_role: contractor_program_manager
decision_role: company_decision_authority
required_reviewer_role: company_decision_authority
legal_review_required: false
typst_issue_required: true
typst_source: publication/typst/templates/report.typ
latest_issue_id: null
created_at: 2026-08-26
updated_at: 2026-08-26
source_as_of: 2026-08-26
source_ids: [SRC-018, SRC-017, SRC-013]
depends_on: [SCR-008]
supersedes: null
confidentiality: sensitive
---

# Cost plan

`FIN-001` · finance · service code `EST`

> **Sensitive.** This blank template is tracked; every *completed* copy lives under `project/private/` and is never committed. Record no credentials, account numbers, signatures, government IDs, or personal financial information in it.

## Purpose

The cost plan: the full construction cost estimate ICA §1.2 requires per project.

## When to use it

Once the design basis is firm enough to quantify; maintained through construction.

## Required inputs

- `DSN-002` areas
- `DD-017` soil and fill findings
- `SRC-018` fee schedule
- Subcontractor quotes

## Instructions

- Every figure states its basis (quote, estimate, published figure, placeholder) and a confidence. A placeholder that looks like an estimate is how a cost plan misleads.
- Carry site work and foundation with wider contingency than superstructure on an infill lot — `DD-018` buried-structure risk is the characteristic Detroit cost surprise.
- Include permit and plan review fees from `SRC-018`, and note that a deposit is due at log-in with the balance at permit issuance (`SRC-017`).
- Include the DLBA tax capture buy-out where the pathway requires it (`SRC-013` Sec. IV(C)) — it is a cost, not a contingency.
- Conclusions reserved to a licensed discipline come from that professional, not from this artifact.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Every line has a basis and a confidence
- Contingency sized to the confidence profile
- Permit fees and tax capture included
- Reconciles to `FIN-002` sources and uses

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Sources

Requirements in this artifact trace to the following rows in `source-register.csv`. Re-verify before relying on any of them — agency requirements change without notice.

| Source | Document | Status | Pinpoint |
| --- | --- | --- | --- |
| `SRC-018` | Fee Schedule (BSEED) | `verified` | Filename carries effective and modification dates; line items not yet abstracted |
| `SRC-017` | Residential Building Permit/Plan Submittal Checklist | `verified` | Preamble (submittal quantities, sealed-drawing statement, fee deposit); Plot Plan; Foundation Plans; Floor Plans; Elevations; Framing Plans; Electrical; Mechanical; Details and General Notes |
| `SRC-013` | First Amended Tax Capture Waiver Policy | `verified` | Sec. I (statutory basis MCL 211.7gg; waiver authority MCL 211.1025a(1)); Sec. II (governs over conflicting DLBA policy); Sec. III (application); Sec. IV(C) (Projects and Infill Housing Lots); Sec. IV(D) (de minimis); Sec. VI(A) (calculation) |

## Unresolved questions

_None recorded. Add any question that would change a decision if answered differently._

## Approvals and professional review

- **Required reviewer: `company_decision_authority`.** Record the review in `GOV-015` before this artifact is relied on at a gate.
- Conclusions reserved to that discipline must come from that professional, not from this document.

## Dependencies

**Upstream — this cannot be completed without:**

- `SCR-008` — Total project cost screen

**Downstream — these depend on this:**

- `FIN-002` — Project sources and uses
- `FIN-003` — Soft-cost and contingency register
- `FIN-004` — Cash-flow and draw forecast
- `FIN-005` — Financing comparison
- `FIN-006` — Lender checklist
- `FIN-007` — Incentive, abatement, grant and rebate register
- `FIN-008` — Proof-of-funds package index
- `FIN-009` — Appraisal request checklist
- `FIN-010` — Insurance matrix

**Stage gates this is required evidence for:** `SG-07`

## Typst issue version expected?

**Yes.** A paired Typst issue document is expected before this leaves the project. Base template: `publication/typst/templates/report.typ`.

Transfer reviewed content to the `.typ` deliberately — there is no automatic Markdown→Typst conversion. The Markdown draft and the Typst issue share this `artifact_id`; the Typst metadata records the draft path and its SHA-256.

Compilation is not approval. See `publication/README.md` for the issue gate.
