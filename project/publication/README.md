---
artifact_id: PUB-003
artifact_type: reference
title: Build and issue instructions
workstream: publication
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
source_as_of: null
source_ids: []
depends_on: [PUB-002]
supersedes: null
confidentiality: public
---

# `project/publication/` — Typst build and issue instructions

`PUB-003`

## Layout

```
publication/
  typst/
    lib/          shared components  (PUB-001)
    templates/    nine base document classes  (PUB-002)
    examples/     one compilable instance per template — the compile gate's fixtures
    lib-selftest.typ   renders every component for visual inspection  (PUB-005)
  build/          DISPOSABLE. gitignored. delete freely.
  issued/         RECORDS. <artifact-id>/<issue-id>/ — never edited in place.
```

## Requirements

Typst 0.14.2 or later. `brew install typst`.

If Typst is unavailable, sources can still be authored — but compilation is **blocked**, and no
publication gate may be reported as passed.

## Building

```bash
./project/tools/compile-check.sh          # everything; any warning is a failure
```

Or a single document:

```bash
typst compile <source>.typ project/publication/build/<name>.pdf \
  --root "$(git rev-parse --show-toplevel)"
```

`--root` must be the repository root so relative imports resolve identically for everyone.

Warnings are treated as failures. In practice a Typst warning here means a missing font or an
unresolved import — both of which change how an issued PDF looks on someone else's machine.

## Component library

`#import "../lib/lib.typ": *` gives you everything. Documents never reach into individual
modules.

| Module | Provides |
| --- | --- |
| `theme.typ` | Page geometry presets, typography, tone ramp, branding placeholders |
| `status.typ` | Status vocabulary, chips, banners, non-final watermark |
| `doc.typ` | `formal-doc` chassis, title page, document control, revision history, running head/foot |
| `callouts.typ` | Note, info, warning, review-required, professional-review, assumption, unresolved |
| `tables.typ` | Condition chips, checklists, risk, parcel schedule, budget, approvals, key/value |
| `sources.typ` | Source table, inline `src()` cross-reference, currency stamp |
| `appendix.typ` | `appendix` show rule, attachment index, binder dividers |

Two API notes that will bite otherwise:

- `appendix` is a **show rule**: `#show: appendix`. Calling `#appendix()` would restart the
  heading counter without changing the numbering scheme, silently leaving appendices numbered
  as body sections.
- Status accepts either `review_required` or `review-required`. An unrecognised status renders
  a loud `UNRECOGNISED STATUS` banner rather than falling back to something benign.

## Branding

`lib/theme.typ` carries neutral placeholders — `[ORGANIZATION NAME]`, `logo: none`, a muted
navy accent. Replace those values and set `logo` to an `image(...)`. Nothing else in the
library hardcodes a name or a colour.

Fonts are pinned to families verified present on the build machine. Typst warns for every
unknown family in a fallback list, which would drown real diagnostics in the compile gate — so
add a new face only after installing it.

## Document classes

| Template | Use for |
| --- | --- |
| `memo.typ` | Recommendations, term sheets, go/no-go, pre-closing authorization |
| `report.typ` | Diligence findings, red-flag memoranda, progress reports, cost plans |
| `application-package.typ` | External submissions; carries a submission-control block |
| `rfp.typ` | Solicitations; carries the single-point-of-contact restriction |
| `letter.typ` | Agency and counterparty correspondence |
| `form-checklist.typ` | Fillable forms and completion checklists |
| `stage-gate-package.typ` | Gate evidence and decision records |
| `professional-handoff.typ` | Counsel and licensed-professional instruction packages |
| `binder.typ` | Closing and compliance binders; wider bind gutter, tab dividers |

## Metadata

Every formal document opens with the `artifact` dictionary. Omitted fields render as
`— not supplied —` in red rather than as blank space, because a blank approver field and a
missing approver field look identical on paper and are not the same thing.

```typst
#show: report.with(artifact: (
  artifact-id: "DD-026", title: "Red-Flag Memorandum — 1234 Example St",
  issue-id: "ISS-001", revision: "A", status: "review-required",
  issue-purpose: "Counsel review of title and access findings",
  parcel-ids: ("21001234.",),
  owner-role: "contractor_program_manager",
  required-reviewer-role: "michigan_licensed_attorney",
  source-draft: "project/working/candidate-parcels/21001234/red-flag-memo.md",
  source-draft-sha256: "<64 hex>",
  source-as-of: "2026-08-26", confidentiality: "internal",
  prepared-by: "[CONTRACTOR NAME]", prepared-for: "Krabby Company LLC",
))
```

Any status other than `approved-for-issue` or `issued` renders a banner on the cover, a banner
at the head of the body, and a diagonal watermark on every page. A draft that escapes into the
world announces itself.

## Issuing

**Compilation is not approval and not issuance.** See `GOV-002 §5` for the ten-condition gate.

Once those conditions hold:

```bash
./project/tools/issue.sh <artifact-id> <issue-id> <revision> <source.typ> "<issue purpose>" <approver-role>
```

That script refuses to run on a dirty working tree, compiles from the recorded commit, writes
the PDF and manifest to `issued/<artifact-id>/<issue-id>/`, and records every hash. It does
**not** decide that the document is correct — a human still has to open the PDF and read it.

Issued PDFs are never edited, never regenerated in place, never quietly replaced. A correction
is a new issue that supersedes the old one, and the old one stays.
