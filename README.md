# 🔷 Proxima — the Sun's stellar neighbourhood in 3D

> *A live, interactive map of every star within five parsecs of the Sun — where they are, what they're made of, and which ones have planets.*

Sister project to **Orrery** (the solar system in 3D). Where Orrery zooms *into*
our system, Proxima zooms *out* to the ~50 nearest stellar objects, plotted from
real astrometry, with the Milky Way plane and Galactic Centre for orientation.
Vanilla JavaScript + Three.js; ships as a static site.

## What This Is

A rotatable, zoomable 3D star-map. Click any star to see its stats — **mass,
colour (spectral type), size, distance, known planets, and when it entered the
catalogues.** The Sun sits at the origin; concentric 5 / 10 / 15 ly rings give a
sense of scale; a faint Milky Way disc shows the galactic plane the whole
neighbourhood is embedded in, with a signpost pointing 26,000 ly toward the
Galactic Centre (Sgr A*).

51 objects within ~5 pc (16.4 ly): 3 Sun-like stars, dozens of red dwarfs, the
white dwarfs Sirius B / Procyon B / Van Maanen's Star, brown dwarfs (Luhman 16,
WISE 0855), and 23 planet-hosting systems (52 known planets) — from Proxima b to
the four-world resonant chain of Gliese 876.

## The data

Every position is real. The catalogue is the RECONS / Gliese census of the solar
neighbourhood (as tabulated in Wikipedia's *List of nearest stars*, cross-checked
2026-07-04). Each object's right ascension, declination and distance are converted
to a right-handed Cartesian frame in light-years:

> X → vernal equinox · Y → RA 6ʰ in the equatorial plane · Z → north celestial pole

Colour is mapped from spectral class the way a real HR diagram reads (blue-white A,
yellow G, orange K, red M, dark L/T/Y brown dwarfs, blue-white degenerate dwarfs).
The Galactic Centre and North Galactic Pole directions are baked into the data so
the viewer can orient the Milky Way plane correctly relative to the equatorial grid.

```
tools/build_catalog.py   # curated table → web/data/stars.json (positions computed here)
web/index.html           # UI shell + styling
web/proxima.js           # Three.js scene, interaction, info card
web/data/stars.json      # generated catalogue (51 objects)
```

Rebuild the catalogue: `python3 tools/build_catalog.py`

## Run it

```
python3 -m http.server 7799 --directory web
# → http://localhost:7799
```

Deep-link to a star with a hash: `#Barnard's%20Star`, `#Tau%20Ceti`, `#Sirius%20A`.

## Milestones

| # | Milestone | State |
|---|-----------|-------|
| 1 | 3D neighbourhood: real positions, per-star stats, galaxy plane + GC, search / filters / deep-links | ✅ 2026-07-04 |
| 2 | **Proper-motion time-scrub** (±80,000 yr, real space velocities, live nearest-star readout, motion trails) | ✅ 2026-07-04 |
| 3 | Polish: OG image, mobile pass, per-star "planets" mini-view | — |
| 4 | Deploy to GitHub Pages (public repo, sister to Orrery) — *pending decision* | — |

## Controls

- **drag** orbit · **scroll** zoom · **click** a star for its stat card
- **Time-scrub**: drag the slider (±80,000 yr) or hit play to watch the neighbourhood
  rearrange under real proper motion — the "nearest star" readout updates live, and
  **motion trails** show each star's path. Watch **Ross 248** slide in to become our
  nearest neighbour ~36,000 years from now.
- **Show**: labels · distance rings · galaxy · planet-hosts (highlights the 23 hosts) · motion trails
- **Filter**: all · has planets · bright (spectral O–K)
- **Find a star**: type a name / catalogue designation

## Notes

- Companion stars sharing a line of sight (Sirius A/B, Alpha Cen A/B, 40 Eri A/B/C…)
  are nudged a few hundredths of a light-year apart so both render and remain clickable.
- Star *display* sizes are scaled for legibility, not to true physical scale — at real
  scale every star would be an invisible point. Relative sizing (dwarf vs. giant vs.
  white dwarf) is preserved.
- Local repo only for now; publishing decision deferred (see STATUS).

> *Any quotes used in this project must be real, sourced attributions. No invented quotes.*
