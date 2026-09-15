# Python reference

Start with the [BZA guide](bza.md) for case queries and exports, or the
[example notebook](../examples/bza_cases.ipynb) for a chart.

Build the complete API reference:

```bash
uv sync --frozen --extra docs
uv run pdoc --output-directory build/docs strongtowns_data
```

Open `build/docs/strongtowns_data.html` for modules, functions, arguments, and examples.
