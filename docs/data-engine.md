# Krabby data-engine lifecycle

## The safety boundary

Source acquisition, transformation, validation, and approval are separate events. A build
first writes to `.staging/<run-uuid>`, validates row accounting and artifacts, and then moves
the completed attempt to an immutable `snapshots/<date>_<uuid>` directory. It does not become
canonical until `PROMOTED.json` is atomically advanced.

Dirty working trees may stage diagnostic builds. Promotion requires a clean Git tree so a
canonical manifest always names committed producer code. UUID4 identifies build attempts;
UUIDv5 identifies stable POIs, routing anchors, and provider requests.

Each snapshot manifest records:

- dataset contract and semantic version, plus its Arrow schema hash;
- producer package version, Git commit, and dirty state;
- immutable parent manifest paths and SHA-256 hashes;
- parameters and acquisition fingerprint without credentials;
- `input = accepted + rejected` counts and enumerated rejection counts;
- CRS, geometry types, artifact media types, byte counts, and SHA-256 hashes;
- the reserved `local_only` archive state for v1.

Legacy data is never upgraded by guesswork. Unknown historical URLs and timestamps remain
null and the manifest says `provenance_grade=legacy`.

## Operating rules

1. Use `krabby-data list`, `graph`, and `status` to discover state.
2. Run `validate` before promotion or after moving or restoring data.
3. Use `build --no-promote` while changing pipeline code.
4. Commit and rerun tests before promotion.
5. Do not edit a completed snapshot, manifest, or generated Parquet file.
6. Do not make a paid provider call through `build`; use the explicit `fetch` command.
7. Never put credentials, signed URLs, or API headers in parameters or manifests.

## Extending the engine

Register a stable `DataAsset`, semantic `DatasetContract`, and `PipelineDefinition` in the
catalog. Declare every input and output by asset ID. Typed geospatial tables use GeoParquet;
raw JSON, HTML, PDFs, rasters, and archives retain native media types with their own
validators. A canonicalizer must emit accepted and rejected records, stable source-row
locators, enumerated reasons, and tests for corrupt as well as successful input.

The `project/` artifact workspace is an independent document-production system. Data-engine
code must not rewrite its registers, templates, captures, or generated publications.

## Nontechnical interpretation

“Promoted” means a dataset passed its declared checks and was deliberately selected for use.
It does not mean every record is substantively trustworthy. For example, a routing anchor can
be geometrically valid while still requiring human review. Structural validity and
eligibility for paid routing are deliberately separate fields.
