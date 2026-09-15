# Travel times and accessibility

Draw areas reachable by driving, walking, or cycling, and measure travel times
to amenities. Run these commands from the data repository after installation.

## Reachable areas

```bash
python pipelines/isochrones/generate_isochrones.py \
  --point 42.3400 -83.0550 --dist 3500 --mode walk \
  --origins 42.3314,-83.0458 --minutes 5 10 15 \
  --output output/isochrones.gpkg --map output/isochrones.png
```

Choose a region with `--place "City, State, USA"` or `--point LAT LON --dist METRES`.
Modes are `drive`, `walk`, and `bike`. Polygon methods are `buffer` (default),
`smooth`, `alpha`, and `convex`; hull methods can include areas beyond reachable streets.

## Amenity access

```bash
python pipelines/isochrones/walkability_score.py \
  --point 42.3400 -83.0550 --dist 3500 --mode walk \
  --points pipelines/isochrones/examples/detroit_coords.csv \
  --categories grocery transit park school pharmacy restaurant \
  --output output/walkability.gpkg --map output/walkability.png
```

Inputs accept CSV, GeoPackage, or GeoJSON. Outputs include travel time in minutes,
category scores, a combined score from 0 to 100, and the weakest category.
Unreachable destinations have infinite travel time and a score of zero.

## Data and interpretation

Networks are saved under `--cache-dir` (default `./cache`). Driving queries can
use `--reuse-graphml PATH` when the saved network covers the requested location.
Walking and cycling use their respective networks.

Walking speed is 4.8 km/h; cycling speed is 15 km/h. Transit proximity measures
access to stops, not scheduled journey time. Locations are matched to nearby
network nodes, which can introduce errors near barriers or widely spaced nodes.

Run either command with `--help` for all options.
