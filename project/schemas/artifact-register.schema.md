# `artifact-register.csv` — column schema

The register is the index of every artifact the project plans to produce, whether or not a
file exists yet. It is the source of truth for IDs, ownership, review requirements, and
publication obligations. `project/tools/validate.py` enforces this schema.

| Column | Type | Rules |
| --- | --- | --- |
| `artifact_id` | string | `^(GOV\|SCR\|PUB\|ACQ\|DD\|DSN\|FIN\|APR\|PRO\|CON\|CLO)-\d{3}$`. Unique. Never reused, never renumbered. |
| `title` | string | Human title. Drives the default filename slug. |
| `workstream` | enum | One of the eleven workstream directories. |
| `service_code` | enum | `LND` `DSN` `PMT` `INS` `EST` `ADM` — Contract Exhibit B codes. Time spent on this artifact bills under this code. |
| `artifact_type` | string | Shape of the document: `checklist`, `register`, `memo`, `log`, `matrix`, `rfp`, `binder`, `received_record`, … |
| `scope` | enum | `reusable` (one copy, project-wide) or `parcel_specific` (one copy per candidate parcel). |
| `status` | enum | The seven document statuses, **plus** the register-only value `planned`. |
| `owner_role` | string | Who produces it. |
| `decision_role` | string | Who decides on it. Under the ICA the Contractor recommends; the Company decides. |
| `required_reviewer_role` | string | Named reviewer. `internal_peer` means no licensed professional is required. |
| `legal_review_required` | boolean | `true` blocks any gate this artifact feeds until counsel signs off. |
| `typst_issue_required` | boolean | `true` means a paired Typst issue document is expected before this leaves the project. |
| `typst_template` | string | Base template basename under `publication/typst/templates/`. Empty when not required. |
| `confidentiality` | enum | `public` \| `internal` \| `sensitive`. `sensitive` artifacts live under `project/private/`. |
| `depends_on` | string | `;`-separated artifact IDs. Every ID must exist in this file. Must be acyclic. |
| `batch` | integer | Generation batch 1–4. |
| `file_path` | string | Path relative to `project/`. Must exist when `status != planned`. |
| `notes` | string | Free text. Used to record contract clauses that drive the artifact. |

## `planned` is register-only

The seven document statuses describe a file that exists. `planned` describes a row with no
file behind it yet. It is deliberately **not** in `artifact-manifest.schema.json`: if
`planned` ever appears in a file's frontmatter, that file is lying about itself.

## Company-owned records

Rows whose `artifact_type` is `received_record` are **not** Contractor work product. ICA
§7.3 states the Contractor does not supervise, observe, monitor, or inspect construction.
These rows exist so the record can be received and filed, and so its absence is visible at a
gate — not so the Contractor authors it. Authoring one would be evidence of a duty the
Agreement disclaims.
