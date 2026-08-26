# DLBA research

Findings live in the artifacts, not here. This directory holds the **captures** and the trail.

- **Analysis:** `templates/acquisition/acquisition-pathway-matrix.md` (`ACQ-002`) and
  `acquisition-pathway-decision-tree.md` (`ACQ-001`).
- **Citations:** `source-register.csv`, rows `SRC-001` … `SRC-014`.
- **Archived captures:** `research/_captures/2026-08-26/` — the PDFs as they existed on the
  retrieval date, hashed in the register.

## Why the captures are committed

These pathways are governed by board-adopted PDFs on an S3 bucket, not by an API. The DLBA can
republish at any URL at any time with no version marker. Archiving the bytes we actually read,
and hashing them, is the only way to answer "what did the policy say when we relied on it".

Run `tools/refresh-sources.sh` to re-download and diff against the registered hashes. A changed
hash is a signal to re-read, not a failure.

## Retrieved 2026-08-26

| Source | Document | Adopted | Captured |
| --- | --- | --- | --- |
| `SRC-001` | Second Amended and Restated Vacant Land Policy | 2025-11-11 | yes |
| `SRC-002` | Neighborhood Create-a-Project Pilot Policy | unconfirmed | yes |
| `SRC-013` | First Amended Tax Capture Waiver Policy | unconfirmed | yes |
| `SRC-014` | Neighborhood Development Projects Policy | 2025-11-11 | yes |

## Still open

- `SRC-010` Public Property Purchase Application portal — field set not inventoried.
- `SRC-011` Detroit Development Opportunities map — not visited; check for a queryable service.
- `SRC-009` "New Build Opportunities" proposal guideline PDF — referenced, not retrieved.
- `SRC-012` Structure Sales Policy — retrieve only if a structure-bearing parcel is a candidate.
- The current **Land Review Area map**. `SRC-001` Ch. IX(C) requires annual publication on the
  DLBA website. Without it, Infill Housing Lot criterion VI(B)(6) cannot be evaluated at all.
