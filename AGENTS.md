# Data safety

- Run `strongtowns-data status` before building or fetching.
- `build` is offline; never fetch because an input is missing.
- Never use a paid provider without explicit authorization.
- Do not edit immutable snapshots, manifests, or promoted pointers.
- Dirty-code runs may stage diagnostics but may not promote.
- Preserve rejection records, source identities, hashes, and null provenance.
- Do not commit or push unless explicitly asked.
