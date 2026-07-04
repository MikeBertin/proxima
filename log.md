# Log — Project Proxima

Decisions, progress notes, session diary. Most recent first.

> *Entry format: `## YYYY-MM-DD — [what changed] | [why] | [next]`*

---

## 2026-07-04 — Galactic-plane orientation (fixes hard-to-orient feedback)

Feedback: hard to orient so the galactic plane is flat with the centre in the
background — because everything is stored equatorial, the plane sits ~62° tilted.
Added an **Orient** toggle: *galactic plane* (default) sets `camera.up` to the
North Galactic Pole direction (plane reads flat), positions the camera on the
anti-centre side looking toward the GC (so Sgr A* sits in the background), and
re-tilts the distance rings into the galactic plane; *equatorial* restores the
RA/Dec frame. Orbiting keeps the chosen plane level. Default is now galactic.
World frame stays equatorial (so selection/target/velocity math is untouched);
only the camera up-vector + ring group rotate.

## 2026-07-04 — Proper-motion time-scrub

Turned the static map into a moving one. Added per-object **proper motion**
(μ_RA*, μ_Dec, mas/yr) + **radial velocity** (km/s) to `KINEMATICS` in the
builder, from standard Hipparcos/Gaia-era literature (companions inherit the
primary's motion; a couple of ultracool-dwarf RVs default to 0). The builder
converts μ + RV + distance into a real heliocentric **3D space-velocity vector**
(`velocity_ly_per_yr`, using v_t = 4.74·μ·d and the RA/Dec/line-of-sight basis)
and writes `vx,vy,vz` in ly/yr to the JSON, alongside `pm` and `rv` for display.

Viewer: positions are now `pos0 + vel·t`. A bottom scrubber spans **±80,000 yr**
with play/pause + reset, a live **"nearest star"** readout, and a **motion-trails**
toggle (straight lines, since propagation is linear). The selected star's stat
card updates its distance live and the camera recentres on it as it drifts.

Sanity-checked against the literature and it lands on the real numbers: nearest
star is Proxima now → **Alpha Cen/Proxima closest ~3.10 ly at +28,000 yr** →
**Ross 248 takes over as our nearest neighbour at +36,000 yr (3.02 ly)** →
Kruger 60 later; Barnard's Star streaks fastest and closes to ~3.76 ly. Verified
in browser (no errors; scrub, trails, readout, play all working).

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
