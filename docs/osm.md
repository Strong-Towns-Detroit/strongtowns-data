# OpenStreetMap data

OSM source preparation and point derivation live in `strongtowns_data.osm`.
Network calls live in `strongtowns_data.osm.acquisition`; readers and registered
builds use local evidence only.

## POIs

Use the schema-2 pipelines for new work:

```bash
strongtowns-data status
strongtowns-data fetch detroit-osm-pois-source-v2 --apply
strongtowns-data build canonical-detroit-osm-pois-v2
strongtowns-data verify detroit.osm.pois.raw.v2 detroit.osm.pois.v2
```

Run acquisition and promotion from a clean data-repository checkout. `--no-promote`
retains diagnostic staging outputs. A provider error or partial Overpass response
fails acquisition; an empty or entirely rejected dataset cannot promote.

The source contains `source_id`, `osm_type`, `osm_id`, `source_tags_json`, and
original geometry in EPSG:4326. IDs distinguish OSM nodes, ways, and relations.
All returned tags survive in JSON, including list values. Rejections retain the
source position, identity, reason, tags, and original geometry as WKB hex.

POI queries include `amenity`, `shop`, `office`, `tourism`, `leisure`, and `craft`.
Routing points prefer categories in that order. They retain the source tags,
source geometry type, and whether the point came from the original geometry or
a representative point. Full source geometry stays in the raw dataset.

Snapshots include resolved boundary geometry, query/settings fingerprints,
OSMnx version, cached response hashes and JSON, collection interval, and OSM
attribution. Cached responses can predate collection; `osm_as_of` stays null.
These are best-effort collections, not transactionally consistent OSM snapshots.

```python
from strongtowns_data import osm

source = osm.read_features("path/to/selected/source/snapshot")
points = osm.read_points("path/to/selected/point/snapshot")
```

Use the repository's lock and materialization commands to select and verify
content-addressed snapshots before opening them. Neither reader fetches data.

## Compatibility

The schema-1 dataset IDs remain registered so historical pins still validate.
`pipelines.osm` adapts the shared implementation to the old category arrays;
`pois.osm` preserves the old public column names and shop-first category order.
The latter exposes rejected records through the returned frame's
`attrs["rejections"]`. New code should use the explicit accepted/rejected tuple
from `prepare_features` or `routing_points`.

The [OSMnx reference](https://osmnx.readthedocs.io/en/stable/user-reference.html)
describes query behavior. Distributed OSM data retains
[OpenStreetMap attribution and license metadata](https://www.openstreetmap.org/copyright).

## Boundaries, water, and streets

The `detroit` and `hd9` regions have explicit source pipelines. HD-9 uses Detroit,
Hamtramck, Highland Park, and Grosse Pointe Park, matching the existing map workflow.
Acquire the boundary first; water and street acquisition reuse its pinned geometry:

```bash
strongtowns-data status
strongtowns-data fetch hd9-osm-boundaries-source --apply
# Commit the validated source manifest/pointer before subsequent promotion.
strongtowns-data fetch hd9-osm-water-source --apply
strongtowns-data fetch hd9-osm-streets-source --apply
```

Record generated manifests and pointers between promoted operations so the next
run starts from clean code. The same commands accept `detroit` in place of `hd9`.
The original `detroit.osm.basemap.raw` import stays unchanged.

Water retains all returned tags and geometries; excluding Lake St. Clair or
non-polygon geometry is a display choice in `read_map_layers`. Street snapshots
store nodes, directed `(u, v, key)` edges, geometry, and JSON attributes in
GeoParquet. List-valued highway and OSM IDs survive; `read_graph` reconstructs the
multigraph without importing OSMnx. The query retains network type, simplification,
and other OSMnx settings. Raw response JSON retains tags outside OSMnx's graph
attribute selection.

Acquire and update consumer locks from this repository, then export map layers
from the consumer without network calls:

```bash
strongtowns-data lock update hd9.osm.boundaries.raw hd9.osm.water.raw hd9.osm.streets.raw \
  --lock ../strongtowns-detroit/strongtowns-data.lock.json --apply
```

Existing legislative, housing-map, and isochrone acquisition helpers delegate to
the common acquisition module. Their routing algorithms and query filters remain
unchanged. Graph/display IO is separate from acquisition.

Krabby's independent `krabby_real_estate.pois.osm` implementation and its
`data/acquisition.py` and `geo/municipal_context.py` callers were audited. That
repository does not yet consume this package's POI adapter; its migration remains
outside this repository's implementation, as scoped in the plan.
