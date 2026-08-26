# Strong Towns Detroit reuse boundary

Source assessed: `Strong-Towns-Detroit/strong-towns-detroit-mono-repo` at commit `6cf23a9`.

## Ported now

- `geo/isochrones.py`: network build/cache, directed travel times, point snapping,
  isochrone geometry, amenity access, and site/destination ranking.
- `parcels/fetcher.py`: Detroit ArcGIS parcel bulk and filtered retrieval.
- `parcels/lot_geometry.py`: conservative dimensional screening that preserves unknowns.
- `mapping/colors.py` and `mapping/layers.py`: consistent geographic context rendering.
- Offline synthetic tests for the travel-time core.
- Base Units geometry helpers for parcel-ID normalization, street-facing-edge inference, and
  building/parcel overlap evidence.

Imports were changed from `strongtowns_detroit` to `krabby_real_estate`. Behavior remains
deliberately close to the source so fixes can be compared or ported later.

The new Base Units retrieval, parcel routing-anchor builder, resumable snapshots, manifests,
and multi-anchor contract were written for this repository. They are intentionally stricter
than the original exploratory scripts: ambiguous duplicate parcel keys fail, fallbacks are
labeled, and no inferred parcel grouping is promoted to a legal-lot claim.

## Deferred

- zoning ordinance parsers and rule engine;
- BZA minutes extraction;
- legislative-district and advocacy analyses;
- the Land Forum website and its design system;
- large generated datasets and cached street networks.

The parcel-comparison stage may later reuse the zoning evaluation layer, but importing it now
would make the collection foundation unnecessarily large and harder to validate.
