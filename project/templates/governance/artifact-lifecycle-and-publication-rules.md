---
artifact_id: GOV-002
artifact_type: policy
title: Artifact lifecycle and publication rules
workstream: governance
service_code: ADM
status: review_required
template_version: "1.0"
parcel_ids: []
owner_role: contractor_program_manager
decision_role: company_decision_authority
required_reviewer_role: company_decision_authority
legal_review_required: false
typst_issue_required: false
typst_source: null
latest_issue_id: null
created_at: 2026-08-26
updated_at: 2026-08-26
source_as_of: null
source_ids: []
depends_on: [GOV-001]
supersedes: null
confidentiality: internal
---

# Artifact lifecycle and publication rules

`GOV-002` · governance · service code `ADM`

This document governs every artifact in `project/`. Where it conflicts with a template, this
document wins.

## 1. The status vocabulary

Seven statuses. Each names what the document *is*, not how far along it feels.

| Status | Means | Entry condition | May become |
| --- | --- | --- | --- |
| `template` | Reusable blank. Not a record. | Created in `templates/`. | — (copies leave as `research_draft`) |
| `research_draft` | Content being gathered. Claims may be uncited. | A copy is made and work starts. | `review_required`, `superseded` |
| `review_required` | Complete but unreviewed. | Author considers it content-complete. | `approved_for_internal_use`, `research_draft` |
| `approved_for_internal_use` | Cleared for internal decisions. Not for distribution. | Named reviewer has signed off, recorded in `GOV-015`. | `approved_for_issue`, `review_required` |
| `approved_for_issue` | Cleared to become a controlled PDF. | Decision authority approves issue. | `issued` |
| `issued` | A controlled PDF exists with a validated manifest. | The issue gate in §5 passes in full. | `superseded` |
| `superseded` | A later version replaces it. | A successor issue exists. | — |

Two rules that are easy to get wrong:

- **`template` never becomes anything.** Templates are copied, not completed. A template that
  has been filled in is a template that has been destroyed.
- **`planned` is not in this list.** It exists only as a value in `artifact-register.csv`,
  meaning "no file yet". If it appears in a file's frontmatter, that file is lying about
  itself, and `tools/validate.py` rejects it.

Movement backwards is normal and expected. A material change to an
`approved_for_internal_use` document returns it to `review_required` — the prior review was
scoped to the prior version.

## 2. Markdown is the default

Markdown is correct for drafts, research notes, checklists, internal memos, decision logs,
artifact instructions, source summaries, meeting notes, and anything still gathering review.
It stays correct whenever fixed pagination and visual presentation add nothing.

Most artifacts never need anything else.

## 3. When a paired Typst issue is required

Create one when — and only when — the artifact becomes one of:

- an external submission;
- a formal acquisition or due-diligence memorandum;
- a stage-gate approval package;
- an RFP or bid package;
- a professional-review handoff;
- an issued project report;
- a closing or compliance binder;
- a document intended for controlled PDF distribution.

The trigger list is deliberately enumerated rather than left to judgement. If an artifact
starts meeting one of these conditions, update `typst_issue_required` in
`artifact-register.csv` **first** — the register is the source of truth, not the file.

## 4. Transfer is deliberate, never automatic

There is no Markdown→Typst conversion, and there should not be. The reviewed `.typ` file
becomes the source for the issued version, and the transfer is done by hand so that
formatting, tables, attachments, issue metadata, and approval state are each decided rather
than inherited.

The Markdown draft and the Typst issue share the same `artifact_id`. The Typst metadata
records the source Markdown path and its SHA-256, so an issued PDF can always be traced back
to the exact draft it came from.

## 5. The issue gate

An artifact may become `issued` only when **all** of the following hold. This is a
conjunction, not a checklist of suggestions.

1. Its Markdown draft, if any, is approved for transfer.
2. The `.typ` source contains complete issue metadata.
3. Cited sources and attachments resolve.
4. Required reviewers have approved it, recorded in `GOV-015`.
5. Typst compilation succeeds.
6. The compiled PDF has been **opened and read** by a person.
7. Source and PDF SHA-256 hashes are recorded.
8. The producer Git commit is recorded.
9. The issue manifest validates against `schemas/issue-manifest.schema.json`.
10. Any prior issue is marked `superseded`.

**Compilation is never approval and never issuance.** A document that builds cleanly and says
the wrong thing is a clean build of the wrong thing. Step 6 is not ceremonial: Typst will
happily render a missing value, a broken column, or a table that silently overflows.

## 6. Builds are disposable; issues are records

`publication/build/` is gitignored. Delete it freely; it rebuilds.

`publication/issued/<artifact-id>/<issue-id>/` is a record. Each issued PDF sits beside a
manifest carrying the artifact ID, issue ID and revision, issue purpose, Typst source path and
hash, source Markdown path and hash, supporting-data hashes, compiler version, compile
command, producer Git commit, issue date, approver role, PDF hash, and the superseded issue if
any.

Issued PDFs are never edited, never regenerated in place, and never quietly replaced. A
correction is a new issue that supersedes the old one, and the old one stays.

## 7. Sensitive data

Never recorded in any tracked file, under any status, for any reason: credentials, account
numbers, signatures, government-issued identifiers, private financial statements, or personal
information about identifiable individuals.

Business contact details for counterparties acting in their professional capacity are fine.

Artifacts marked `confidentiality: sensitive` keep their blank template tracked and every
completed copy under `project/private/`, which is gitignored. Contract terms are themselves
confidential under ICA §4.1 and belong there.

## 8. What we do not draft

No artifact is written as signature-ready legal, tax, lending, architectural, engineering, or
construction advice. We do not create operative purchase agreements or construction agreements.

We do create: transaction term sheets, clause and issue checklists, records of official forms,
and professional handoff materials that state the question precisely enough to be answered.

Where an agency or counterparty supplies its own agreement or form, we link and inventory it.
We do not recreate it as a buyer-authored or contractor-authored document — a retyped official
form is a forgery-shaped object even when the intent is convenience.

## 9. Construction-phase records

ICA §7.3 states the Contractor does not supervise, direct, oversee, observe, monitor, or
inspect construction. Records that would evidence such a duty — submittal log, RFI log, pay
applications and lien waivers, safety and incident records, nonconforming work, punch list —
carry `artifact_type: received_record` and are Company-owned.

They are registered so their absence is visible at a gate. They are received and filed, never
authored here.
