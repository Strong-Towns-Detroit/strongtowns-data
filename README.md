# Strong Towns Data

Reproducible acquisition, cleaning, canonical datasets, routing and
accessibility features, and parcel-level modeling for civic research.

```bash
strongtowns-data status
strongtowns-data build
strongtowns-data verify detroit.parcels.raw
strongtowns-data materialize \
  --repository . \
  --lock ../strongtowns-detroit/strongtowns-data.lock.json \
  --output ../strongtowns-detroit/.data
```

Builds consume promoted inputs. Network acquisition is always an explicit
`fetch` operation. Immutable dataset payloads remain outside Git.

Consumer lock files identify snapshots by dataset ID, snapshot ID, and manifest
SHA-256. Materialization only copies already-present validated snapshots; it
never builds or fetches them.

Only code, schemas, reviewed fixtures, and provenance metadata belong in Git.
Raw downloads and generated dataset payloads remain in the external archive.
See [DATA_LICENSING.md](DATA_LICENSING.md).

The software is available under the MIT License.
