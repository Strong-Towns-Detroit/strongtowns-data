# Parcel data-pipeline contracts

The parcel is the unit of analysis. Neighborhood labels may be attached downstream but never
preselect or average away a parcel.

## Sources and canonical tables

Parcels, Base Units addresses, streets, buildings, and broad OSM POIs enter as immutable raw
snapshots. Canonicalization preserves raw identity as text, uses explicit normalized join
keys, emits typed GeoParquet, and reconciles every input as accepted or rejected. Existing
2026-08-26 files have fixed migration baselines: 377,940 parcels, 486,646 addresses, 36,104
streets, 364,096 buildings, and 15,202 OSM candidates.

ArcGIS acquisition fingerprints layer metadata, schema, last edit time, and the complete
object-ID set before and after pagination. A changed source, duplicate ID, incomplete page,
or server/local count mismatch rejects the attempt. Page caches are scoped to that complete
fingerprint.

OSM keeps its source geometry separate from its routing point. Source tags and categories are
typed key/value collections. A point uses `source_point`; a non-point uses a labeled
`representative_point`. Grocery interpretation remains downstream.

## Routing anchors

Each parcel/street candidate receives a stable UUIDv5 derived from a versioned natural-key
tuple. Address evidence, frontage geometry, and review disposition are separate datasets.
Base Units `address_id` is distinct from the source snapshot-row object ID.

The structural gates require unique keys, valid WGS84 geometry, exactly one frontage per
anchor, linked-address evidence for linked anchors, no evidence for fallbacks, and a maximum
0.01-US-survey-foot distance from the parcel boundary. Building count is null only when the
building source was not supplied and zero when a supplied source matched none.

Review state controls provider eligibility:

- `not_required` and `approved` are eligible;
- `required` needs a recorded per-anchor override;
- `rejected` is never eligible;
- fallback, low/not-evaluated confidence, or street distance over 80 feet requires review.

Review CSV/GeoPackage exports carry immutable anchor and disposition parent hashes. Imports
reject stale parents, unknown or duplicate UUIDs, invalid states, and incomplete decisions.

## TravelTime ledger

The request dataset is promoted before provider contact. UUIDv5 request identity includes the
anchor UUID, direction, mode, horizon, UTC reference time, provider, and request-contract
version. Provider search IDs are opaque and explicitly mapped back to request UUIDs.

Both arrival and departure from the same point are supported. Walking requests enforce a
3,600-second absolute upper limit; continuous decay and parcel scoring are later pipes.

Every raw provider response is immutable evidence. A batch is valid only when:

```text
expected request IDs = successful result IDs + explicit provider error IDs
```

Missing, duplicate, unexpected, empty, malformed, or non-polygon results reject the attempt.
Transport, rate-limit, and server failures receive at most five bounded exponential-backoff
attempts, respecting `Retry-After`. Any terminal provider result leaves the attempt staged and
prevents result promotion. The only initially authorized live operation is one reviewed
anchor, walking, 3,600 seconds, in both directions.

## Later pipes

Business verification, parcel/POI spatial joins, exact travel-time matrices, continuous-decay
scores, and optional neighborhood or corridor labels remain downstream of this collection
foundation.
