# Next simplification: OpenStreetMap

## Decision

Consolidate OSM acquisition and POI normalization next. Start with POIs, then
move boundary, street, and water acquisition onto the same source-evidence
conventions. Keep the existing fetch/build distinction: fetching is explicit;
opening or rebuilding prepared data is offline.

## What exists today

| Location | Responsibility | Problem to resolve |
| --- | --- | --- |
| `src/strongtowns_data/pipelines/osm.py` | Registered POI fetch, raw geometry, routing points, rejection records | Keeps five category tags; loses names, addresses, and other source tags. |
| `src/strongtowns_data/pois/osm.py` | Public collector and a second normalizer | Includes `craft`, names, and display tags, but silently skips missing geometry and uses a different identity/column contract. |
| `src/strongtowns_data/legislative/osm.py` | Place boundaries, drive streets, water, GPKG output | Fetches directly; drops graph edge identities and flattens highway tags for display. |
| `src/strongtowns_data/geo/isochrones.py` | Routing network and water acquisition | Another acquisition path mixed with analysis. |
| `pipelines/housingDataAnalysis/` | Historical map rendering and street simplification | Direct OSMnx calls and independent output conventions. |

The registered basemap source currently imports existing boundary/water evidence;
it does not share an acquisition implementation with the legislative fetchers.
The POI raw and canonical datasets were missing or invalid at the September 15
status check, while the imported basemap was promoted. Preserve that basemap.

The two POI implementations also choose a primary category in different orders
(`amenity` first versus `shop` first). Consolidation must not silently reclassify
existing consumers. Empty/all-rejected input handling needs explicit coverage;
the registered implementation currently accesses `result.source_id` even when
no output columns were constructed.

## Target

One `strongtowns_data.osm` package owns source identities, query descriptions,
source serialization, and pure normalization. Internal acquisition functions
own OSMnx access. The registered pipeline remains the entry point for fetch,
validation, and promotion; public readers open prepared snapshots.

A source snapshot retains original geometry, OSM element type and ID, all
returned tags, boundary geometry and hash, requested tags, endpoint, OSMnx
version, acquisition timestamps, response/cache hashes, and rejection records.
Keep node/way/relation identities distinct. Street graphs retain edge keys and
connectivity; display layers are derived products. Record actual collection
intervals without implying a transactionally consistent OSM snapshot.

Routing points remain separate from source geometry and record how each point
was derived. Names and categories are downstream interpretations with explicit
precedence. Keep OSM attribution and license metadata with distributed data.

## Implementation sequence

### 1. Establish the shared POI contract

- Inventory existing manifests and consumers before changing columns. Compare
  `tests/test_data_osm.py` and `tests/test_krabby_pois.py` fixtures.
- Define one category query including `craft`; preserve all returned tags, not
  just the selected category keys. Distinguish a changed query from a changed
  normalization rule in fingerprints.
- Define typed empty outputs, explicit missing-CRS failures, duplicate-ID
  rejection, list/null tag handling, invalid geometry behavior, and input =
  accepted + rejected accounting.
- Introduce the source contract as a new major schema version when it changes
  existing columns or meanings. Preserve existing immutable snapshots and pins.

### 2. Replace the duplicate normalizers

- Move source preparation and routing-point derivation to the shared package.
- Route registered POI fetch/build through it. Keep a temporary compatibility
  adapter for the public POI columns; it performs no independent acquisition.
- Preserve each legacy primary-category rule in its adapter until consumers
  explicitly migrate. Compare IDs, tags, geometries, and rejection counts.
- Run one explicit Detroit fetch, validate, build offline, and open the prepared
  output from a clean checkout. Document the new snapshot before switching pins.

### 3. Migrate consumers and remove duplicate paths

- Move Detroit's legislative street-fetch script to explicit registered
  acquisition and prepared layers. Keep `filter_arterials` as a pure display
  operation with coverage for list-valued highway tags.
- Audit the independent Krabby POI implementation and its acquisition and
  municipal-context callers; migrate with adapters only after its tests pass.
  Those files are in another repository and are outside this implementation.
- Replace active housing-map and isochrone acquisition callers incrementally.
  Preserve graph topology and analysis behavior; do not combine a routing
  algorithm rewrite with this acquisition cleanup.
- Delete old collectors and wrappers once repository searches show no callers.

### 4. Extend the same acquisition contract to basemaps

- Add explicit boundary, water, and street source pipelines using the common
  query/provenance helpers, with separate schemas for features and graphs.
- Fingerprint resolved boundary geometry, endpoint, query, and relevant OSMnx
  settings. Isolate and restore OSMnx global settings between calls.
- Reuse boundary evidence across water/street builds. Preserve the existing
  imported basemap until the replacement passes a visual and spatial comparison.

## Acceptance checks

- There is one POI source normalizer and one explicit POI acquisition path.
- Offline builds/readers cannot invoke OSMnx or the network.
- Tests cover mixed tags, list values, all-empty/all-rejected inputs, absent CRS,
  duplicate identities, invalid geometry, and deterministic output ordering.
- Source polygons survive unchanged; routing points carry their derivation.
- Cache identity changes with query, boundary, or endpoint, and failed or partial
  acquisition cannot promote a misleading complete dataset.
- Existing callers pass through an adapter or migrate with reviewed schema and
  category differences. Clean-code promotion and historical pins still work.

First implementation PR: shared POI contract, unified normalization, registered
fetch/build integration, and compatibility adapters. Basemap migration follows
in a separate PR so the first change has a bounded review and measurable result.
