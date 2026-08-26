# Parcel data-pipeline contracts

## Governing rule

`parcel_id` is the analytical key. Neighborhood membership is optional downstream metadata.
No stage may discard, average away, or preselect a parcel because of its neighborhood.

## Pipe 0: versioned source snapshots

The current Detroit parcel source is ArcGIS item `3c784c118e5c4083b37038e9b38573df`,
`Parcels (Current)`. The older item `9ca25373d4f747be85850344186dda3c` is now labeled
`Parcels (Deprecated)` and must not silently replace it.

The Base Units adapter independently snapshots addresses, streets, and buildings from the
City's `BaseUnitFeatures` FeatureServer. Retrieval is object-ID paged, resumable, atomic per
page, and accompanied by counts and SHA-256 manifests. Raw records remain raw evidence.

## Pipe 1: parcel routing anchors

The implemented anchor stage joins Base Units addresses to parcels by normalized `parcel_id`,
then addresses to centerlines by `street_id`. It estimates the parcel edge facing each linked
street and projects the linked address point onto that edge. This represents the pedestrian
connection between parcel and street; it does not assert the location of a building entrance.

Corner and through parcels may emit multiple anchors. When no usable address↔street relation
exists, the stage emits a low-confidence anchor at the midpoint of the edge facing the nearest
Base Units street. It does not silently discard duplicate normalized parcel IDs.

Minimum contract:

| Field | Meaning |
|---|---|
| `parcel_id` | Stable City of Detroit parcel identifier |
| `parcel_key` | Normalized cross-source parcel join key |
| `anchor_id` | Stable key for this parcel/street anchor |
| `street_id` | Base Units street relation used |
| `latitude` / `longitude` | WGS84 coordinate on the selected parcel edge |
| `routing_anchor_method` | Address projection, linked-edge midpoint, or nearest-street fallback |
| `frontage_source` | Whether evidence came from a Base Units relation or fallback |
| `frontage_confidence` / `anchor_confidence` | Geometry and overall evidence confidence |
| `address_objectids_json` | Base Units address records supporting the anchor |

The GeoPackage retains point anchors and the inferred front-edge geometries. The companion CSV
is the direct TravelTime input. A manifest hashes every input snapshot.

The separate QA stage reconciles source relations against the output, reports confidence and
street-distance distributions, and emits review geometries for fallbacks, multiple anchors,
and front edges more than 80 feet from their linked centerline. The 80-foot criterion mirrors
the geometry model's high-confidence boundary; it is a review flag, not an analytical cutoff.
Parcel improvement status and property class are attached only to the review artifact.

## Pipe 2: citywide POI catalog

The first source adapter collects broad OpenStreetMap features across Detroit. It stores:

1. raw source geometry, unchanged except for GeoJSON serialization;
2. one normalized routing point per feature;
3. source identity and selected original tags;
4. a timestamped manifest.

Minimum normalized contract:

| Field | Meaning |
|---|---|
| `poi_id` | Namespaced stable identifier, such as `osm:node:123` |
| `source` / `source_id` | Provenance and source record identity |
| `name` | Best available source name |
| `primary_category` / `category_value` | Uninterpreted source classification |
| `source_geometry_type` | Original Point/Polygon/etc. |
| `latitude` / `longitude` | Routing point |
| `source_tags_json` | Preserved source attributes used for later classification |

Additional adapters can emit the same contract. Cross-source entity resolution is a later
pipe; no source record should be lost during collection.

## Pipe 3: TravelTime polygons

Inputs are parcel routing anchors and explicit time-map specifications:

| Parameter | Example |
|---|---|
| direction | `departure`, `arrival` |
| transportation | `walking` |
| travel-time horizon | `3600` seconds |
| reference time | timezone-aware ISO-8601 timestamp |

Each TravelTime search ID embeds the parcel and anchor keys, direction, mode, and horizon:

```text
parcel:01000001.:anchor:01000001-1001-1:departure:walking:3600
parcel:01000001.:anchor:01000001-1001-1:arrival:walking:3600
```

The output is a GeoJSON FeatureCollection plus a credential-free request manifest. Polygons
remain individual and parcel/anchor-keyed. Union, intersection, business selection, and
scoring do not belong in this collection stage. Multiple anchors are preserved rather than
combined by this pipe.

Grocery destinations will use their own entrance-quality field. Base Units footprints,
imagery, and human review can establish those entrances; a VLM may propose candidates but is
not treated as authoritative evidence.

## Next pipes—not part of the current implementation

1. spatially join POIs to parcel time-map polygons;
2. classify and verify businesses, beginning with groceries;
3. request exact directional parcel-to-POI travel-time matrices;
4. attach optional neighborhood and corridor labels;
5. build continuous-decay and other parcel-comparison models.
