# 🔷 Proxima — the Sun's stellar neighbourhood in 3D

> *A live, interactive map of every star within five parsecs of the Sun — where they are, what they're made of, and which ones have planets.*

Sister project to [Orrery](https://mikebertin.github.io/orrery/) (the solar system
in 3D). Where Orrery zooms *into* our system, Proxima zooms *out* to the ~50
nearest stellar objects, plotted from real astrometry, with the Milky Way plane
and Galactic Centre for orientation. Vanilla JavaScript + Three.js; ships as a
static site.

**▶ Live: [mikebertin.github.io/proxima](https://mikebertin.github.io/proxima/)** —
try [Tau Ceti's four planets](https://mikebertin.github.io/proxima/#Tau%20Ceti)
or scrub 36,000 years forward and watch Ross 248 become our nearest neighbour.

## Why "Proxima"

*Proxima* is Latin for "nearest" — and Proxima Centauri is exactly that: the
single nearest star to the Sun, a red dwarf 4.25 light-years away hiding a
temperate rocky planet. A map of the Sun's nearest neighbours could hardly be
called anything else.

## What This Is

A rotatable, zoomable 3D star-map. Click any star to see its stats — **mass,
colour (spectral type), size, distance, known planets, and when it entered the
catalogues.** The Sun sits at the origin; concentric 5 / 10 / 15 ly rings give a
sense of scale; a faint Milky Way disc shows the galactic plane the whole
neighbourhood is embedded in, with a signpost pointing 26,000 ly toward the
Galactic Centre (Sgr A*).

51 objects within ~5 pc (16.4 ly): 3 Sun-like stars, dozens of red dwarfs, the
white dwarfs Sirius B / Procyon B / Van Maanen's Star, brown dwarfs (Luhman 16,
WISE 0855), and 23 planet-hosting systems (55 known planets) — from Proxima b to
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
| 3 | Polish: OG image, mobile pass, soft 3D grid, trail direction arrows | ✅ 2026-07-10 |
| 4 | Per-star "planets" mini-view (log-AU system strips, every known planet enriched) | ✅ 2026-07-10 |
| 5 | Deploy to GitHub Pages (public repo, sister to Orrery) | ✅ 2026-07-10 |

## Controls

- **drag** orbit · **scroll** zoom · **click** a star for its stat card
- **Planetary-system strip** (on the stat card, for the 23 planet-hosts + Sun): each
  planet plotted on a log-AU axis — dot size = mass class (rocky/Neptune/Jovian by
  colour), green ring = temperate orbit, dashed = disputed. Tap a dot for distance,
  mass and discovery year.
- **"Why no planets found"** — every zero-planet star explains its own gap (flare-star
  noise, binary glare, hot-star spectra, white-dwarf history, or plain survey depth),
  because no confirmed planet almost never means no planets.
- **Time-scrub**: drag the slider (±80,000 yr) or hit play to watch the neighbourhood
  rearrange under real proper motion — the "nearest star" readout updates live, and
  **motion trails** show each star's path. Watch **Ross 248** slide in to become our
  nearest neighbour ~36,000 years from now.
- **Orient**: *galactic plane* (default — galactic north up, so the Milky Way reads flat
  and the Galactic Centre sits in the background) or *equatorial* (RA/Dec frame). Orbiting
  keeps whichever plane you chose level.
- **Show**: labels · distance rings · galaxy · planet-hosts (highlights the 23 hosts) ·
  motion trails (with arrowheads marking direction of travel) · 3D grid (soft light-grey
  lattice at 5-ly spacing, Sun at the origin, oriented to the chosen frame)
- **Filter**: all · has planets · bright (spectral O–K)
- **Find a star**: type a name / catalogue designation

## Notes

- Companion stars sharing a line of sight (Sirius A/B, Alpha Cen A/B, 40 Eri A/B/C…)
  are nudged a few hundredths of a light-year apart so both render and remain clickable.
- Star *display* sizes are scaled for legibility, not to true physical scale — at real
  scale every star would be an invisible point. Relative sizing (dwarf vs. giant vs.
  white dwarf) is preserved.
- Deploys to GitHub Pages via `.github/workflows/pages.yml` (serves the `web/` folder).

> *Any quotes used in this project must be real, sourced attributions. No invented quotes.*
