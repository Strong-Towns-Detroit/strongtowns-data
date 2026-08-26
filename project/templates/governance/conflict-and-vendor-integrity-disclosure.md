---
artifact_id: GOV-022
artifact_type: record
title: Conflict and vendor-integrity disclosure
workstream: governance
service_code: ADM
status: template
template_version: "1.0"
parcel_ids: []
owner_role: contractor_program_manager
decision_role: company_decision_authority
required_reviewer_role: company_decision_authority
legal_review_required: true
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

# Conflict and vendor-integrity disclosure

`GOV-022` · governance · service code `ADM`

> **Sensitive.** This blank template is tracked; every *completed* copy lives under
`project/private/` and is never committed. Record no credentials, account numbers,
signatures, government IDs, or personal financial information in it.

## Purpose

Records disclosures required by ICA §3.5 (vendor integrity) and §4.3 (conflicts) — any interest the Contractor or a family member holds in a candidate property or a vendor.

## When to use it

On engagement, on every new candidate parcel, on every new vendor, and whenever an interest arises. The duty is continuous, not a one-time form.

## Required inputs

- Candidate parcel list
- Vendor list

## Instructions

- Disclose direct and indirect interests, including those held by family members (§4.3).
- Record the §4.3 restriction period for every parcel presented to the Company: the Contractor may not acquire, or assist a third party in acquiring, that property for twelve months after presenting it. Calendar the expiry.
- Record any rebate, kickback, or vendor compensation offered — including offers declined (§3.5).
- This artifact is `sensitive`. It lives under `project/private/` and is never committed.

## Completion criteria

This artifact is complete when **all** of the following hold:

- Every candidate parcel presented has a disclosure entry and a calendared §4.3 expiry
- Every vendor relationship is either disclosed or affirmatively recorded as none

An item that has not been checked is recorded as `not_found` or `blocked` — never left blank
and never recorded as `verified`. Unknown conditions do not default to clear.

## Unresolved questions

- Does the twelve-month §4.3 restriction run from first presentation or from Company's decision on the parcel?

## Approvals and professional review

- **Required reviewer: `company_decision_authority`.** `legal_review_required: true` — every stage gate this artifact feeds is blocked until that review is recorded in `GOV-015` (professional-review tracker).
- This document is an *issue-spotting tool*. It does not contain legal advice and must not be treated as a substitute for counsel.
- Record the reviewer, the date, and the scope reviewed. A review with no recorded scope does not clear the gate.

## Dependencies

**Upstream:** none. This is an entry point.


## Typst issue version expected?

**No.** This artifact stays in Markdown. If it ever becomes an external submission, a stage-gate package, or a controlled-distribution PDF, update `typst_issue_required` in `artifact-register.csv` first — the register is the source of truth, not the file.
