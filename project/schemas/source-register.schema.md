# `source-register.csv` — column schema

Every claim about a *current external requirement* — an eligibility rule, a fee, a submission
deadline, a required form — must trace to a row here. A requirement without a row is an
assumption, and belongs in the assumption log instead.

| Column | Type | Rules |
| --- | --- | --- |
| `source_id` | string | `^SRC-\d{3}$`. Unique, never reused. |
| `document_title` | string | Title as published, not a paraphrase. |
| `publishing_authority` | string | The body that publishes it (agency, department, utility). Not the website vendor. |
| `url` | string | Direct URL to the document, not a search page or a portal landing page. |
| `environment` | enum | `production` \| `qa` \| `staging` \| `archived`. Production is preferred; a non-production source must say so. |
| `retrieved_at` | date | ISO date the URL was actually fetched. Not the document's own date. |
| `requirement_supported` | string | The specific requirement this source establishes. One requirement per row; split rather than combine. |
| `supports_artifact_ids` | string | `;`-separated artifact IDs citing this source. |
| `verification_status` | enum | `verified` \| `unavailable` \| `conflicting` \| `superseded` \| `not_found`. |
| `superseded_by` | string | `SRC-` ID that replaces this one, if any. |
| `notes` | string | Conflicts, ambiguities, and what was checked before recording `unavailable`. |

## Rules that matter more than the columns

**Retrieval date is not optional.** Agencies change fee schedules, forms, and eligibility
rules without versioning or notice. A citation without a retrieval date cannot be audited and
cannot be re-verified.

**Production over QA.** Agencies frequently expose staging copies of forms that differ from
what intake will accept. Where both exist, cite production and record the QA URL in `notes`.

**Unavailable is a finding, not a gap to paper over.** If a requirement cannot be established
from a primary source, record the row with `verification_status = unavailable`, list what was
checked in `notes`, and mark the dependent condition `blocked` — never `verified`, and never
silently omitted.

**Conflicts stay conflicts.** Where two official sources disagree, record both rows with
`verification_status = conflicting` and resolve it with the authority, not by picking the more
convenient one.

**Link official forms; do not reconstruct them.** Where an agency or counterparty supplies its
own agreement or form, the register points at it. Retyping it into a project-authored document
creates a document that looks official and is not.
