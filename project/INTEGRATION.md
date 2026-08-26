---
artifact_id: GOV-025
artifact_type: reference
title: Pipeline integration notes
workstream: governance
service_code: ADM
status: review_required
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
source_as_of: 2026-08-26
source_ids: [SRC-001, SRC-010, SRC-011, SRC-019]
depends_on: [GOV-001, GOV-002]
supersedes: null
confidentiality: internal
---

# Pipeline integration notes

`GOV-025` · governance · service code `ADM`

For whoever maintains the analytical pipeline in `src/` and `pipelines/`. This is the seam
between the two halves of the repository — what each side owes the other, and the one place
where a small amount of pipeline work unlocks a lot of artifact work.

## The two halves

| | `src/` `pipelines/` `data/` | `project/` |
| --- | --- | --- |
| Holds | **derived facts** from public datasets | **asserted claims** — recommendations, checklists, memos |
| Trusted because | code you can re-run | cited sources and recorded human approval |
| Fails by | a bug, a stale snapshot | an uncited claim, a skipped review |
| Guarded by | tests | `tools/validate.py`, `tools/compile-check.sh` |

Neither writes to the other. `project/` artifacts **link to** pipeline outputs; they must never
restate the numbers, because a number copied into a memo goes stale silently and a memo has no
test suite to catch it.

## The integration that matters most

The DLBA **Infill Housing Lot** programme is the primary acquisition pathway (see
`templates/acquisition/acquisition-pathway-matrix.md`). Its *lot* eligibility criteria are
`SRC-001` Ch. VI(B) — and they are almost entirely **machine-evaluable**. Today they are
answered by hand, one parcel at a time. They should be a pipeline filter.

| Criterion | Cite | Data needed | Available today? |
| --- | --- | --- | --- |
| Vacant residential, no structure | VI(B)(1) | parcel + structure attributes | likely — parcel catalog |
| No delinquent or currently due taxes | VI(B)(3) | parcel tax status | needs a source |
| Zoned R1, R1-H, R2, R3, R3H, R4, R5, R5-H, R6, R6-H, PD, PD-H, SD1, SD1-H, SD2, SD2-H, SD4 | VI(B)(4) | zoning district per parcel | needs a zoning layer |
| **Does not exceed 7,500 sq ft** | VI(B)(5) | parcel area | yes — parcel geometry |
| **Within an Inclusive Housing Opportunity Area** | VI(B)(6) | see below | **derivable — see below** |
| DLBA-owned | Ch. VI generally | ownership | `SRC-011` map; service unknown |

Two of these are worth calling out.

### Inclusive Housing Opportunity Areas are computable

`SRC-001` Ch. IX(B)(1) defines an Inclusive Housing Opportunity Area as an area **where
on-market home sales have averaged $100/sq ft or more over the last 12 months**.

That is a definition, not a lookup. Given sales data with dates, prices and floor areas, the
surface can be computed directly. The DLBA is required to publish an authoritative map at least
annually (Ch. IX(C)) and **we have not located it** — it is open question 5 in the pathway
matrix.

So there are two things here and they must not be conflated:

- **The authoritative map.** Binding. Still to be found. Until then, criterion VI(B)(6) cannot
  be answered definitively for any parcel.
- **A derived IHOA surface.** Computable now, useful for *screening and prioritisation*, and
  **not** an eligibility determination.

If the pipeline produces the derived surface, label it unambiguously — something like
`iho_area_derived` with a `basis: computed_from_sales` field — so no artifact can mistake it for
the published map. The screening artifacts (`SCR-004`, `SCR-001`) can use it to rank candidates;
`ACQ-003` and `ACQ-001` must still record VI(B)(6) as `blocked` until the real map is in hand.
That distinction is the whole point of the `verified` / `not_found` / `blocked` vocabulary.

### The 7,500 sq ft ceiling is a programme-shaping filter

It is a hard cap per lot, so anything larger requires assemblage — which routes to a different
policy with a different approval threshold (4 parcels or $75,000 at staff level; above either,
the DLBA Board). A parcel-area filter therefore doesn't just screen parcels, it selects the
acquisition strategy. Worth surfacing as a flag, not just a boolean.

## Data sources the artifacts are waiting on

Recorded in `source-register.csv`; these are the ones with a plausible machine interface.

| Source | What it is | Why it matters | Status |
| --- | --- | --- | --- |
| `SRC-011` | Detroit Development Opportunities map | First branch of `ACQ-001` — who owns the parcel | not retrieved; **check for an ArcGIS service behind the viewer** |
| `SRC-010` | Public Property Purchase Application portal | Field set for `ACQ-007` | not retrieved; field inventory needed |
| `SRC-019` | Accela / eLAPS permit portal (`aca-prod`) | Permit status for `APR-007`, inspections for `APR-009` | not retrieved; **check for a queryable status endpoint before scraping** |
| — | Land Review Area map | Criterion VI(B)(6) | **not located** — highest-value gap |
| — | Parcel tax status | Criterion VI(B)(3) and `DD-005` | no source identified |
| — | Zoning district per parcel | Criterion VI(B)(4), `DD-010`, `DD-011` | no source identified |

Two cautions worth carrying into any fetcher:

- `detroitmi.gov` emits **`detroitmi.localhost`** URLs in its document links — a staging
  hostname in production output. Rewrite the host; don't assume the link is dead.
- `SRC-019` is `aca-prod.accela.com`. Accela deployments commonly expose an `aca-test` twin.
  Pin production explicitly and record which you read.

## If you supply data to `project/`

Artifacts reference pipeline outputs by **path plus manifest**, following the pattern already in
`data/derived/` (`*.manifest.json` alongside the data). Two rules:

1. **A manifest with a hash, or it can't be cited.** `schemas/issue-manifest.schema.json` has a
   `supporting_data` array taking `{path, sha256, role}`. Any figure appearing in an issued PDF
   must resolve to a hashed file, and `validate.py` re-checks those hashes.
2. **Date the snapshot.** Artifacts carry `source_as_of` separately from `updated_at` precisely
   because external facts go stale independently of the document. A dataset with no capture date
   can't populate that field.

## If you touch `project/`

Mostly: don't need to. But if you do —

- **`artifact-register.csv` is the source of truth**, not the files. Add the row before creating
  the file. IDs are never reused or renumbered.
- **`planned` is register-only.** It must never appear in a file's frontmatter; the validator
  rejects it.
- **Frontmatter must agree with the register** on status, confidentiality,
  `legal_review_required`, and `typst_issue_required`. The validator cross-checks all four.
- **Run the gates before considering anything done:**

```bash
python3 project/tools/validate.py     # registers, frontmatter, cross-refs, source hashes
./project/tools/compile-check.sh      # Typst compile gate — warnings are failures
./project/tools/refresh-sources.sh    # re-download sources, diff against registered hashes
```

- **Never put anything sensitive in a tracked file** — no credentials, account numbers,
  signatures, government IDs, or private financial statements. `project/private/` is gitignored
  and is where completed copies of `confidentiality: sensitive` artifacts belong.

## What is deliberately unresolved

Three official sources conflict with each other and are recorded as conflicts rather than
reconciled (`source-register.csv`, `conflicts_with`). Five sources are known to exist but have
not been retrieved. Thirty-one open questions sit in the artifacts that need them.

None of that is a backlog to tidy away. `validate.py` warns whenever an artifact leans on an
unretrieved source, and that warning is doing its job. Resolve them by **going and reading the
source**, then updating the register — not by removing the citation.
