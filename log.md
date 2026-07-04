# Log — Project Proxima

Decisions, progress notes, session diary. Most recent first.

> *Entry format: `## YYYY-MM-DD — [what changed] | [why] | [next]`*

---

## 2026-07-04 — Project created + M1 built & verified

**Concept.** A sister to Orrery: instead of zooming into the solar system, zoom
*out* to the Sun's stellar neighbourhood — a 3D map of the nearest stars, each a
clickable object with mass / colour / size / distance / planets / discovery, plus
the Milky Way plane and Galactic Centre placed the same way Orrery places them.

**Decisions locked (with the user).**
- Codename **Proxima** (chosen from: Cynosure, Hipparchus, Parallax, Proxima).
- Sample: **within ~5 pc (~16.4 ly)** — the classic nearest-stars set. Ended up
  with 51 objects (companions included).
- **Local repo only for now**; GitHub Pages publish deferred to M3.

**Data.** Curated the 5 pc census in `tools/build_catalog.py` from the
RECONS/Gliese list (Wikipedia "List of nearest stars"), astrometry cross-checked
via two WebFetch passes. Real RA/Dec/distance → Cartesian light-years
(X→equinox, Z→NCP). Colour mapped from spectral class. Galactic-Centre (Sgr A*)
and North-Galactic-Pole directions baked into the JSON so the viewer can orient
the Milky Way disc correctly. 23 planet-hosting systems, 52 known planets.

**Viewer.** Vanilla + Three.js (importmap, unpkg) in Orrery house style: additive
glow sprites coloured per spectral type, CSS2D labels (one per system to reduce
clutter), concentric 5/10/15 ly distance rings, a soft Milky Way disc brightened
toward the GC with a signpost, background starfield. Raycast click → stat card;
camera eases to the selected star. Search box, filters (all / has-planets /
bright), toggles (labels / rings / galaxy / planet-hosts), `#Name` deep-links.

**Verified in browser** (localhost:7799): 51 objects load, no console errors,
galaxy band renders across the field, Sun anchored at origin, click→info card
shows correct stats (checked Tau Ceti = 4 planets, Sirius A = A1V/2.06 M☉/0
planets), camera-fly and deep-link both work. Pulled the fly-in distance back
after first pass (glow was filling the frame).

**Next.** M2 polish — OG image, mobile pass, a per-star planets mini-view, and
maybe a proper-motion time-scrub ("the neighbourhood in 40,000 years" — Ross 248
becomes our nearest neighbour). Then the M3 publish decision.
