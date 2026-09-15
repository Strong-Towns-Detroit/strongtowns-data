# OSM simplification — implementation complete

Implemented September 15, 2026. See [OSM usage and maintenance](osm.md) for commands,
schemas, compatibility, and source provenance.

## Delivered

- One shared source normalizer and explicit OSMnx acquisition module in
  `strongtowns_data.osm`, with schema-1 adapters for existing POI callers.
- Separate schema-2 POI source and routing-point datasets. Sources retain all
  returned tags and original geometry; rejected rows retain identities, reasons,
  tags, and geometry evidence. Shop-first and amenity-first legacy category
  interpretations remain distinct.
- Query fingerprints include boundary geometry, endpoint, tags, OSMnx version,
  and relevant settings. Snapshots retain boundary and cached response evidence,
  collection intervals, and attribution. Settings restore after success/failure;
  partial Overpass responses fail acquisition.
- Explicit Detroit and HD-9 boundary, water, and street source pipelines. Water
  and streets reuse pinned boundary geometry. Street GeoParquet preserves node
  IDs, directed multiedge keys, curved geometry, and list-valued attributes.
- Legislative, housing-map, and isochrone acquisition callers delegate to the
  shared module. Routing algorithms, network parameters, and map query filters
  are preserved. Arterial display filtering handles all highway tags.
- Detroit's legislative export reads verified lock references without fetching.
  The SDK dependency and three HD-9 dataset references are pinned in the consumer.
- Shared OSM tests run in CI. Existing import-formatting failures are corrected.

## Validated data

| Dataset | Result |
| --- | --- |
| Detroit POI source, schema 2 | 15,226 features; 0 rejected |
| Detroit routing points, schema 2 | 15,226 points; built offline |
| Detroit boundary | 1 municipality |
| HD-9 boundaries | 4 municipalities |
| Detroit water source | 170 features; 0 rejected |
| HD-9 water source | 174 features; 0 rejected |
| HD-9 street source | 21,483 nodes; 61,833 directed edges |

All listed sources validated and promoted from clean code; their manifests and
pointers are committed. Acquisition responses and data artifacts are materialized
in the local snapshot store. The Detroit street pipeline is registered and tested;
the live street collection used the HD-9 region required by the consumer.

The Detroit source contains 6,383 named POIs and retains 9,240 non-point source
geometries separately from routing points. Existing baseline dataset IDs and
immutable snapshots remain resolvable.

## Verification and basemap decision

The data suite passed 510 tests with one optional-provider skip. A separate run
with real OSMnx passed the six routing tests plus two graph/display tests. The
Detroit repository-boundary/lock tests passed, and the pinned export produced
four city boundaries, 174 water polygons, and 61,833 street edges with OSMnx import
and network connections blocked. CI passed on the implementation commits.

The preserved basemap and newly acquired Detroit water layer were compared
visually and spatially. The historical water query has 218 features versus 170
for the narrower `natural=water` query. The boundary symmetric difference is
208,686 square metres (about 0.056% of the old area), with a 188-metre Hausdorff
distance. Keep the existing `detroit.osm.basemap.raw` pin; use the new HD-9 sources
for the legislative workflow. Comparison artifacts are in
`build/osm-simplification/basemap-comparison.{png,json}` locally.

## Separately scoped follow-up

Krabby retains an independent `krabby_real_estate.pois.osm` collector, used by
`data/acquisition.py` and `geo/municipal_context.py`. Those callers were audited;
changing that repository remains outside this implementation, as specified in
the original plan. Its eventual migration should use the public compatibility
adapter and validate existing tests before removing its duplicate implementation.
