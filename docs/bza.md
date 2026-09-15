# BZA cases

Explore Detroit Board of Zoning Appeals cases, requested relief, hearings, and outcomes.

```bash
strongtowns bza list
strongtowns bza list --search "side setback" --project-type single-family
strongtowns bza list --outcome granted --from 2020-01-01 --to 2025-12-31
strongtowns bza list --unit hearing
strongtowns bza show CASE_HISTORY_ID
strongtowns bza export --search "side setback" --output setbacks.csv
strongtowns bza status
strongtowns bza fetch
```

Queries fetch data on first use. Later runs use the local copy, including offline.
`status` shows availability and coverage; `fetch` checks for and installs updates.

Public downloads are awaiting the first dataset release. Until then, use
`--directory PATH` for a local bundle or `--lock PATH --repository PATH` for project data.

## Filters and exports

- `--search`: search case text, addresses, and recorded decisions.
- `--relief`: select a category, such as `setbacks_yards` or `lot_dimensions`.
- `--project-type`: select a family or label, such as `housing`, `single-family`, or `duplex`.
- `--outcome`: select an outcome; `granted` and `denied` are accepted shortcuts.
- `--from` and `--to`: include hearings within the date range, including both endpoints.

Different filters narrow the selection together. Repeat a filter to accept any
of its values. A case is included when any of its hearings falls within the date
range; `--unit hearing` returns only hearings within that range.

Exports support `.csv` and `.json`. For JSON on screen, use
`strongtowns --json bza list`. Counts refer to distinct cases unless you select
`--unit hearing`. Unknown project types, locations, and intake dates remain unknown.

## Updates

When newer coverage is available, commands display:

```text
New BZA case coverage is available: 2025-09-20 -> 2026-09-15. To update, run:

    strongtowns bza fetch
```

The new date is green and the command is bold cyan. `NO_COLOR` disables color.
Notices do not appear in exported data. Update checks happen at most once daily;
failed checks do not interrupt work with local data.

Use `--version VERSION` to keep an analysis on a specific release. Fetching an
update does not change an explicit version pin. Use `--cache PATH` to choose
where downloaded datasets are stored.

## Python

```python
from strongtowns_data import bza

dataset = bza.open()
setbacks = dataset.cases(search="side setback", project_type="single-family")
hearings = dataset.hearings(date_from="2025-01-01")
details = dataset.case("CASE_HISTORY_ID")
dataset.export("setbacks.csv", search="side setback")
print(dataset.status())

bza.fetch()  # Update the local dataset.
```

Queries return pandas DataFrames. Case details include hearing history, source
references, relief, site matches, and review notes. Use `bza.open(version="VERSION")`
to pin a notebook, or `bza.open(directory="PATH")` to read a local bundle.
Project snapshots can be opened with
`bza.open(lock="strongtowns-data.lock.json", repository="../strongtowns-data")`.

Try the [example notebook](../examples/bza_cases.ipynb) to export cases and draw a chart.
