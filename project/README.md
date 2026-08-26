---
artifact_id: GOV-001
artifact_type: reference
title: Project operating README
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
source_as_of: null
source_ids: []
depends_on: []
supersedes: null
confidentiality: internal
---

# `project/` — parcel acquisition and home-building artifact workspace

Working artifacts, reusable templates, and issued documents for Krabby Company LLC's Detroit
parcel-acquisition and home-building program.

## What this is, and what it is not

This workspace holds **asserted claims**: recommendations, checklists, memoranda, applications,
and issued documents. Their trustworthiness comes from cited sources and recorded human
approval.

The rest of the repository holds **derived facts**: `src/`, `pipelines/`, `data/`, and `tests/`
turn public datasets into reproducible parcel-level outputs. Their trustworthiness comes from
code you can re-run.

Those are different failure modes, so they get different machinery and they stay separate.

> **Hard boundary.** Nothing in `project/` writes to `src/`, `pipelines/`, analytical schemas,
> or generated datasets. Artifacts may *link* to pipeline outputs under `data/derived/`; they
> must not restate the numbers, which go stale silently.

## Roles

Under the Independent Contractor Agreement, the Construction Program Manager **recommends**
and Krabby Company LLC **decides** (§1.3). Every artifact records both: `owner_role` produces
it, `decision_role` decides on it. This is not a formality — it is the boundary the Agreement
draws, and the artifacts should make it legible without anyone having to remember it.

## Layout

| Path | Contents |
| --- | --- |
| `artifact-register.csv` | Every planned artifact. The index and source of truth. |
| `source-register.csv` | Primary sources behind every external-requirement claim. |
| `stage-gates.csv` | The twelve decision points and their required evidence. |
| `dependency-register.csv` | Derived edges: artifact→artifact and artifact→gate. |
| `schemas/` | Column contracts and JSON Schemas. Enforced by `tools/validate.py`. |
| `templates/` | Reusable blanks, by workstream. Never completed in place. |
| `research/` | Source summaries and retrieved requirement notes. |
| `working/` | Live per-parcel and project-wide working copies. |
| `publication/` | Typst library, templates, disposable builds, issued records. |
| `private/` | Ignored. Sensitive working records. Never committed. |
| `tools/` | `validate.py` (register + frontmatter gate), `compile-check.sh` (Typst gate). |

## Workstreams and service codes

Every artifact carries a `service_code` from Exhibit B of the Agreement, so time spent inside
an artifact bills under the code the artifact already declares:

`LND` land acquisition & diligence · `DSN` plans & documents · `PMT` permits & entitlements ·
`INS` inspections & closeout · `EST` estimating & schedule · `ADM` reporting & administration

## The rules that actually matter

**Unknown never defaults to clear.** Every verifiable condition carries one of `verified`,
`not_found`, `not_applicable`, `professional_review_required`, or `blocked`. A blank is not a
pass. `not_found` means we looked and found nothing — which is not the same as confirming a
negative, and is not a clear.

**Cited or assumed, never neither.** A claim about a current external requirement traces to a
row in `source-register.csv` with a retrieval date, or it lives in the assumption log with a
test that would resolve it.

**Link official forms; do not recreate them.** Where an agency or counterparty supplies its own
agreement or form, we inventory and link it. Retyping it produces a document that looks
official and is not.

**Nothing here is professional advice.** No artifact is drafted as signature-ready legal, tax,
lending, architectural, engineering, or construction advice. Legal, title, survey,
environmental, engineering, lending, insurance, and tax artifacts name the professional who
must review them, and `GOV-015` enforces that the review actually happened.

**Never track sensitive data.** No credentials, account numbers, signatures, government IDs,
private financial statements, or personal information — in any tracked file, ever. Sensitive
working records go in `private/`, which is gitignored.

**Compilation is not approval.** A PDF that builds is a PDF that builds. See
`publication/README.md` for what issuance actually requires.

## Construction scope boundary

ICA §7.3 states the Contractor does not supervise, direct, oversee, observe, monitor, or
inspect construction. Several construction-phase records — submittal log, RFI log, pay
applications and lien waivers, safety and incident records, nonconforming work, punch list —
are therefore registered with `artifact_type: received_record` and marked Company-owned.

They exist in the register so their **absence is visible at a gate**. They are received and
filed, not authored. Authoring one would be evidence of a duty the Agreement disclaims.

## Checks

```bash
python3 project/tools/validate.py      # register integrity + frontmatter + issue manifests
./project/tools/compile-check.sh       # Typst library and template compile gate
```

Both must pass before any stage gate is recorded.

## Reading order

1. This file.
2. `templates/governance/artifact-lifecycle-and-publication-rules.md` — statuses, the
   Markdown/Typst decision, and the issue gate.
3. `schemas/artifact-register.schema.md` and `schemas/source-register.schema.md`.
4. `publication/README.md` — how to build and how to issue.
