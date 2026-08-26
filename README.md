# Krabby Real Estate

Parcel-level data collection and accessibility analysis for Krabby's Detroit home search.

The parcel is the unit of analysis. Neighborhoods may be attached later as descriptive
labels, but they do not constrain data collection, define accessibility, or determine how
results are aggregated. An unusually strong parcel in a weaker neighborhood must remain
visible.

## Current pipeline

```text
Detroit parcel catalog
        │
        └── parcel geometry
Detroit Base Units
        │
        ├── address↔parcel↔street relationships
        └── one or more parcel routing anchors
        │
Citywide POI catalog
        │
        └── source identity + source tags + routing point
                         │
                         ▼
            TravelTime polygon collection
            ├── departure polygons from each parcel
            └── arrival polygons to each parcel
```

These stages collect facts. Business classification, spatial joins, exact travel-time
matrices, quality review, and parcel scoring are deliberately downstream.

See [the pipeline contracts](docs/data-pipeline.md) for precise inputs and outputs.

## Setup

Requires Python 3.12+.

```bash
uv sync --extra dev
uv run pytest -q
```

## Collect the citywide OSM POI catalog

This broad collection includes all mapped `shop`, `amenity`, `leisure`, `tourism`, `office`,
and `craft` features. It does not decide which records count as groceries.

```bash
uv run python pipelines/collect_osm_pois.py \
  --place "Detroit, Michigan, USA" \
  --output-dir data/raw/pois/osm/2026-08-26
```

The stage writes the original OSM geometries, normalized routing points, and a collection
manifest separately.

## Fetch Base Units and build parcel routing anchors

First snapshot the current parcel catalog (the City export is large and may take time to
generate):

```bash
uv run python pipelines/fetch_parcels.py \
  --output-dir data/raw/parcels/2026-08-26
```

Base Units is collected as three independent, resumable source snapshots. The page cache can
be retained to resume interrupted citywide downloads.

```bash
uv run python pipelines/fetch_base_units.py \
  --output-dir data/raw/base-units/2026-08-26
```

Build anchors only after the parcel, address, and street snapshots are fixed:

```bash
uv run python pipelines/build_parcel_routing_anchors.py \
  --parcels data/raw/parcels/2026-08-26/parcels.geojson \
  --addresses data/raw/base-units/2026-08-26/base_units_addresses.geojson \
  --streets data/raw/base-units/2026-08-26/base_units_streets.geojson \
  --buildings data/raw/base-units/2026-08-26/base_units_buildings.geojson \
  --output-gpkg data/derived/parcel-routing-anchors.gpkg \
  --output-csv data/derived/parcel-routing-anchors.csv
```

An address-linked street gets an anchor projected onto the inferred street-facing parcel
edge. Corner and through parcels can therefore retain multiple anchors. Parcels without a
usable address↔street link receive an explicitly low-confidence nearest-street fallback.

Generate source-relation statistics, flagged review layers, distance outliers, and a compact
citywide QA map:

```bash
uv run python pipelines/audit_parcel_routing_anchors.py \
  --anchors-gpkg data/derived/parcel-routing-anchors.gpkg \
  --parcels data/raw/parcels/2026-08-26/parcels.geojson \
  --addresses data/raw/base-units/2026-08-26/base_units_addresses.geojson \
  --streets data/raw/base-units/2026-08-26/base_units_streets.geojson \
  --output-dir output/parcel-routing-qa/2026-08-26
```

The QA thresholds select records for inspection; they do not exclude parcels or alter the
underlying evidence.

## Generate per-parcel TravelTime polygons

Input CSV:

```csv
parcel_id,anchor_id,latitude,longitude
01000001.,01000001-1001-1,42.3501,-83.0812
01000002.,01000002-1001-1,42.3504,-83.0808
```

Set credentials without committing them:

```bash
export TRAVELTIME_APP_ID=...
export TRAVELTIME_API_KEY=...
```

Collect both directions for a one-hour walking horizon:

```bash
uv run python pipelines/build_traveltime_polygons.py \
  --parcels data/derived/parcel-routing-anchors.csv \
  --direction departure \
  --direction arrival \
  --transportation walking \
  --travel-time-seconds 3600 \
  --reference-time 2026-08-26T12:00:00-04:00 \
  --output data/raw/traveltime/walking-3600.geojson
```

The client batches requests at TravelTime's ten-search limit and writes a credential-free
manifest beside the GeoJSON. Each polygon is keyed to both `parcel_id` and `anchor_id`.

## Tooling lineage

The geospatial foundation selectively reuses John Bolt's private
`Strong-Towns-Detroit/strong-towns-detroit-mono-repo`. See
[the reuse boundary](docs/strong-towns-reuse.md).
