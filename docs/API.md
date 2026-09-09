# Data SDK reference

The HTML API reference is generated from the public Python modules, docstrings,
type annotations, and signatures with [pdoc](https://pdoc.dev/). It is not
edited by hand.

```bash
uv sync --frozen --extra docs
uv run pdoc --output-directory build/docs strongtowns_data
```

Open `build/docs/strongtowns_data.html` after generation. CI runs the same
command and uploads the complete site as the `strongtowns-data-sdk-docs`
artifact.

Public documentation belongs in a Python docstring immediately below the
relevant module, class, method, function, or property definition. Type
annotations supply the generated signatures. Names beginning with an
underscore are treated as implementation details.
