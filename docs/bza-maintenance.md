# BZA maintenance

Run these commands from the data repository. Start with `strongtowns-data status`
and copy the complete existing evidence bundle into a writable working directory.
Keep immutable snapshots unchanged.

## Collect minutes

```bash
python -m strongtowns_data.bza._pipeline minutes --output build/bza-sources --apply
python -m strongtowns_data.bza._pipeline extract \
  --source build/bza-sources --output build/bza-evidence --limit 1
```

Install `strongtowns-data[minutes]` and set `GEMINI_API_KEY` in the environment
or repository `.env`. Extraction previews by default. Add `--apply --allow-paid`
to run it. Use `--all` for all missing documents, `--model` to choose a model,
and `--force` to repeat an extraction. BZA extraction and project classification
default to `gemini-3.8-flash` in code; `GEMINI_MODEL` is not consulted. Review results against the original minutes.

## Build and review

```bash
python -m strongtowns_data.bza._pipeline build \
  --source build/bza-evidence --reviews resources/bza --output build/bza-atlas
```

Use a new empty output directory. Add `--parcels PATH` and `--addresses PATH`
for local parcel and Base Units data. Without those inputs, recorded matches are
reused where available and gaps are listed in the audit.

Edit reviewed corrections in `resources/bza`. Site suggestions appear in
`site_review_suggestions.csv`; review them before updating the correction ledger.
Map categories require at least 10 cases and an 80% site match rate.

To rebuild the registered dataset from existing repository evidence:

```bash
strongtowns-data build detroit-bza-atlas --no-promote
```

## Add project types and intake candidates

```bash
python -m strongtowns_data.bza._pipeline project-types \
  --source build/bza-atlas/case_histories.csv \
  --output build/bza-evidence/project_type_enrichment --all
python -m strongtowns_data.bza._pipeline intake \
  --source build/bza-atlas/case_histories.csv --output build/bza-evidence
```

Both commands preview by default. Project classification requires
`--apply --allow-paid`; intake lookup requires `--apply` and `ACCELA_APP_ID`
or `ACCELA_ACCESS_TOKEN`. Rebuild into a new directory to include the results.
Review missing and low-confidence project labels. Intake dates remain candidates
until their case matches are confirmed. See [intake dates](bza-intake-dates.md).

## Prepare a release

```bash
python -m strongtowns_data.bza._pipeline package \
  --source build/bza-atlas --output build/bza-release --version YOUR_VERSION \
  --release-url https://github.com/Strong-Towns-Detroit/strongtowns-data/releases/download/YOUR_TAG/bza-YOUR_VERSION.zip
```

For later releases, supply `--prior-index PATH` to retain access to older versions.
Review the archive and `bza-index.json`, then upload both to GitHub Releases.
Keep the index on the latest release, including code-only releases. Version IDs
must be unique; retain published archives for pinned analyses.

Dataset releases use `MAJOR.MINOR.PATCH`: increment the major version for schema
changes, the minor version for refreshed or expanded data with the same schema,
and the patch version for corrections. Dataset versions are independent of the
Python package version. The first public schema-1 release is `1.1.0` (tag
`bza-v1.1.0`); reserve the 1.x line for schema 1.
