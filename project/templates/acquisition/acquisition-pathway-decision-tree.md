---
artifact_id: ACQ-001
artifact_type: decision_tool
title: Acquisition pathway decision tree
workstream: acquisition
service_code: LND
status: review_required
template_version: "1.0"
parcel_ids: []
owner_role: contractor_program_manager
decision_role: company_decision_authority
required_reviewer_role: michigan_licensed_attorney
legal_review_required: true
typst_issue_required: false
typst_source: null
latest_issue_id: null
created_at: 2026-08-26
updated_at: 2026-08-26
source_as_of: 2026-08-26
source_ids: [SRC-001, SRC-004, SRC-008, SRC-009, SRC-011, SRC-014]
depends_on: []
supersedes: null
confidentiality: internal
---

# Acquisition pathway decision tree

`ACQ-001` · acquisition · service code `LND`

> **Reusable.** One copy project-wide, under `working/project-wide/`.

## Purpose

Routes a specific parcel to the correct acquisition pathway in a fixed order, so the choice is
made on ownership and eligibility facts rather than on which listing happened to surface.
`ACQ-002` holds the detailed comparison; this decides which row of it applies.

> **Currency.** Verified **2026-08-26** against the DLBA Vacant Land Policy adopted
> **2025-11-11**. Not legal advice — an issue-spotting tool requiring counsel review.

## The tree

Work the branches in order. Do not skip ahead: ownership determines the rulebook, and
eligibility determines whether the cheapest route is even open.

```
START — one parcel, identified by parcel ID
│
├─ Q1. Who owns it?  → Detroit Development Opportunities map (SRC-011)
│   │                   Never infer ownership from a listing.
│   ├─ Privately owned ──────────────────────────► BRANCH P
│   ├─ City of Detroit owned ───────────────────► BRANCH C
│   └─ DLBA owned ──────────────────────────────► Q2
│
├─ Q2. Is the parcel already listed on a DLBA platform?
│   ├─ Listed as Marketed Property ──────────────► PATHWAY 2
│   │     60-day listing; proposal to the listing broker; ~90 days to close (SRC-009).
│   │     Retrieve the "New Build Opportunities" proposal guideline first — NOT YET RETRIEVED.
│   ├─ Listed on Auction / Own-It-Now ───────────► structure sales; out of scope for
│   │     vacant-land new build unless acquiring to demolish (see SRC-012, not retrieved).
│   └─ Not listed ───────────────────────────────► Q3
│
├─ Q3. Does the parcel satisfy Infill Housing Lot LOT criteria?  (SRC-001 Ch. VI(B))
│   │   ALL of:
│   │     (a) vacant residential, no structure
│   │     (b) no delinquent or currently due taxes on the lot
│   │     (c) zoned R1/R1-H/R2/R3/R3H/R4/R5/R5-H/R6/R6-H/PD/PD-H/SD1/SD1-H/SD2/SD2-H/SD4
│   │     (d) does NOT exceed 7,500 sq ft
│   │     (e) within an Inclusive Housing Opportunity Area, or an area approved by a
│   │         City Revitalization Office
│   ├─ All satisfied ────────────────────────────► Q4
│   └─ Any not satisfied ────────────────────────► Q5
│         Record WHICH criterion failed. (d) and (e) are the usual failures and they
│         are the ones that change the strategy, not just the paperwork.
│
├─ Q4. Does Krabby satisfy Infill Housing Lot PURCHASER criteria?  (Ch. VI(C))
│   │   ALL of:
│   │     (a) will use the lot to develop new housing
│   │     (b) can provide a thorough description of the proposed development
│   │     (c) can demonstrate capacity to FINANCE AND COMPLETE a 1–4 unit project
│   │     (d) current on taxes for ALL Detroit property owned directly or indirectly
│   │     (e) has NOT purchased 3+ Infill Housing Lots in the preceding 12 months
│   │     (f) in good standing on every DLBA agreement
│   ├─ All satisfied ────────────────────────────► PATHWAY 1  ★ primary route
│   │     Note Ch. VI(E)(3): if the lot is also Side Lot eligible, DLBA offers it as a
│   │     Side Lot for 30 days first. Build that delay into the schedule.
│   └─ (e) fails on volume ──────────────────────► defer, or route to PATHWAY 3/5.
│         This is a PROGRAMME-level cap. Check SCR-005 before assuming it is clear.
│
├─ Q5. Is this a multi-parcel assemblage, or larger than 7,500 sq ft?
│   ├─ Yes ──────────────────────────────────────► PATHWAY 5 (then 3)
│   │     SRC-001 Intro p.iii does NOT supersede the Projects Procedures and Guidelines,
│   │     and Ch. VI(D)(2) routes additional discounts through them. SRC-014 is the
│   │     governing document and is NOT YET RETRIEVED. Retrieve before committing.
│   └─ No ───────────────────────────────────────► PATHWAY 3
│         Public Property Purchase Application (SRC-004, SRC-010).
│         Expect a DLBA callback within 2–4 weeks if DLBA owns it.
│
├─ BRANCH C. City-owned  ─────────────────────────► PATHWAY 4
│     Different rulebook entirely (SRC-008). Reviewed across Mayor's Office, HRD, P&DD,
│     DEGC, Law, DBA, DLBA and Dept of Neighborhoods. DETROIT CITY COUNCIL IS THE FINAL
│     DECISION MAKER. Generally sold at market value; ~4 months application to close.
│     Requires a conceptual plan: proposed use, scope of work, estimated costs and
│     financing sources, prior experience.
│
└─ BRANCH P. Privately owned ─────────────────────► PATHWAY 6 (broker) or 7 (direct)
      No programme eligibility, no development agreement, no reverter — and no
      discount and no DLBA title clearing. Title position is established entirely
      through diligence (DD-003, DD-004, DD-006).
```

## Routes that are closed to us

Recorded so they are not re-derived each time a parcel appears:

- **Side Lot** — requires the purchaser to already hold title to a Street Adjacent *occupied*
  residential property (`SRC-001` Ch. I(C)(1)). Not available to a developer acquiring land.
- **Neighborhood Lot** — requires a Principal Residence Exemption; not a construction
  programme. Also **prohibited outright inside Inclusive Housing Opportunity Areas**
  (Ch. IX(E)(1)) — the very areas where Infill Housing Lots exist.
- **Create-a-Project** — the adopted pilot is for neighborhood community groups and block clubs
  building art installations, playgrounds and community gardens. No housing use. See `ACQ-002`
  Conflict B: the website's use of this name does not match the adopted policy.

## Instructions

- Answer each question from a primary source with a retrieval date, and record the answer.
  A branch taken on an assumption is an assumption, and belongs in `GOV-008`.
- Where a criterion cannot be established, mark it `blocked` and stop. Do not route the parcel
  on an unknown — every downstream artifact will inherit that unknown as if it were a fact.
- Record the pathway *and the rejected alternatives* in `GOV-007`. Which routes were closed,
  and why, is the part that gets re-litigated.
- Re-run the tree if ownership, zoning, or the Land Review Area map changes. Ch. IX(C) requires
  the map to be updated at least annually, so eligibility under criterion (e) can lapse.

## Completion criteria

- Ownership established from `SRC-011`, with a date
- Every Ch. VI(B) lot criterion and Ch. VI(C) purchaser criterion individually answered
- Cumulative Infill Housing Lot count checked against `SCR-005`, not assumed
- Selected pathway and rejected alternatives recorded in `GOV-007`
- No branch taken on an unverified condition

## Unresolved questions

1. Does the three-lot cap aggregate across affiliated entities? (Ch. VI(C)(5), "directly or
   indirectly", undefined.)
2. Where is the current Land Review Area map, and which areas are Inclusive Housing Opportunity
   Areas today? Required to answer Q3(e) at all.
3. What does `SRC-014` (Projects Procedures and Guidelines) permit for assemblage?
4. Does the Development Opportunities map expose a queryable service, so Q1 can be answered in
   the pipeline rather than by hand per parcel?

## Approvals and professional review

- **Required reviewer: `michigan_licensed_attorney`.** Recorded in `GOV-015` before this routes
  a real transaction.
- Contains no legal advice. Pathway eligibility conclusions are provisional until counsel
  confirms them against the executed instruments.

## Dependencies

**Upstream:** none. This is the entry point of the acquisition workstream.

**Downstream:** `ACQ-002` and, through it, every other acquisition artifact.

**Stage gates:** feeds `SG-03` (Application or offer ready).
