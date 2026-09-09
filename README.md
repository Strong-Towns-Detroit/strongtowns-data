# Strong Towns Data

Reproducible acquisition, cleaning, canonical datasets, routing and
accessibility features, and parcel-level modeling for civic research.

Use the unified CLI for read-only status checks and materializing a consumer's
pinned snapshots. With Python 3.12+ and Git installed, one command installs
the CLI and both the data and graphics SDKs:

```bash
python -m pip install 'strongtowns-cli @ git+https://github.com/Strong-Towns-Detroit/strongtowns-cli.git@main'
strongtowns doctor --require data
strongtowns data status --repository .
strongtowns data materialize ../strongtowns-detroit/strongtowns-data.lock.json \
  ../strongtowns-detroit/.data --repository .
```

The unified CLI deliberately does not fetch, build, promote, or change locks.
Use this package's domain CLI for those data-producing operations:

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

Resolve one verified artifact through the public repository API:

```python
from strongtowns_data import DataBuildSystem, DataLock, DataRepository

lock = DataLock.load("strongtowns-data.lock.json")
repository = DataRepository(DataBuildSystem.find("../strongtowns-data"))
parcels = repository.artifact(lock.asset("detroit.parcels"), "accepted.parquet")
```

See the [generated Data SDK reference](docs/API.md) for the complete public
Python interface and instructions for building the docstring-derived HTML docs.

Update selected lock entries from separately prepared promoted snapshots. The
command previews by default and writes only with `--apply`:

```bash
strongtowns-data lock update \
  --repository . \
  --lock ../strongtowns-detroit/strongtowns-data.lock.json \
  detroit.parcels
strongtowns-data lock update --apply \
  --repository . \
  --lock ../strongtowns-detroit/strongtowns-data.lock.json \
  detroit.parcels
```

Only code, schemas, reviewed fixtures, and provenance metadata belong in Git.
Raw downloads and generated dataset payloads remain in the external archive.
See [DATA_LICENSING.md](DATA_LICENSING.md).

The software is available under the MIT License.
