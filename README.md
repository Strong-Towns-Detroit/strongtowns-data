# Strong Towns Data

Tools and datasets for civic research: BZA cases, parcels, housing, maps, and accessibility.

## Get started

Install with Python 3.12+ and Git:

```bash
python -m pip install 'strongtowns-cli @ git+https://github.com/Strong-Towns-Detroit/strongtowns-cli.git@main'
strongtowns doctor --require data
strongtowns bza list --search "side setback"
```

The installation includes the CLI, data SDK, and graphics SDK.

## BZA cases

```python
from strongtowns_data import bza

dataset = bza.open()
cases = dataset.cases(search="side setback")
dataset.export("setbacks.csv", search="side setback")
```

Read the [BZA guide](docs/bza.md) or try the [example notebook](examples/bza_cases.ipynb).

## Project datasets

Inspect available data and copy the snapshots required by a project:

```bash
strongtowns data status --repository .
strongtowns data materialize ../strongtowns-detroit/strongtowns-data.lock.json \
  ../strongtowns-detroit/.data --repository .
```

A project's data lock records the dataset versions used by its analyses.

## More

- [Python API reference](docs/API.md)
- [Data maintenance](docs/data-pipelines.md)
- [BZA maintenance](docs/bza-maintenance.md)
- [Data licensing](DATA_LICENSING.md)

The software is available under the MIT License.
