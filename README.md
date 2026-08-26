# Krabby Real Estate

Parcel-level data collection and accessibility analysis for Krabby's Detroit home search.
The parcel is the unit of analysis. Neighborhood labels may be attached later, but they do
not constrain collection, accessibility, or aggregation.

## Contract-first data engine

```text
Detroit parcels + Base Units ──> parcel routing anchors ──┐
                                                         ├──> TravelTime request/result ledger
broad OSM business catalog ──> verified destinations ────┘
```

Every production dataset is an immutable snapshot with a versioned schema, hashes, row
accounting, and pinned parent manifests. A promotion pointer is only a discovery aid;
downstream runs resolve it to an immutable manifest hash before use.

Business classification, spatial joins, exact travel-time matrices, continuous decay, and
parcel scoring are deliberately downstream of this collection foundation.

## Setup

Requires Python 3.12+.

```bash
uv sync --extra dev
uv run pytest -q
```

## Data lifecycle

Inspect the registered assets and dependency graph:

```bash
uv run krabby-data list
uv run krabby-data graph
uv run krabby-data status
```

The initial source files predate this engine. Register their actual bytes without inventing
historical URLs or timestamps, then promote only from a clean committed implementation:

```bash
uv run krabby-data import-legacy
# Inspect each completed manifest under data/sources/*/snapshots/.
uv run krabby-data import-legacy --promote
```

Future source refreshes are explicit network operations and also remain unpromoted unless
requested:

```bash
uv run krabby-data fetch parcels --apply
uv run krabby-data fetch base-units --apply
uv run krabby-data fetch osm-pois --apply
```

Build the offline canonical and routing chain. A staging-only run may use dirty code;
promotion may not.

```bash
uv run krabby-data build --no-promote
uv run krabby-data build
```

TravelTime requests require an explicit timezone-aware reference time. Arrival and departure,
walking, and a 3,600-second horizon are the defaults:

```bash
uv run krabby-data build prepare.traveltime-requests \
  --parameter reference_time_utc=2026-08-26T16:00:00Z \
  --parameter anchor_uuids=<one-reviewed-anchor-uuid>
```

Paid collection is never part of `build`. The smoke path requires one anchor and no more than
the two directional requests:

```bash
uv run krabby-data fetch traveltime --apply --allow-paid --smoke
```

Review queues are parent-pinned and round-trippable:

```bash
uv run krabby-data review export output/anchor-review.gpkg
uv run krabby-data review import output/anchor-review.gpkg
```

See [the engine lifecycle](docs/data-engine.md),
[the dataset contracts](docs/data-pipeline.md), and
[the Strong Towns reuse boundary](docs/strong-towns-reuse.md). Scripts under `pipelines/`
remain migration references; production builds consume registered asset IDs, not arbitrary
input paths.
