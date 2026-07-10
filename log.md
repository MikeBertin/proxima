# Log — Project Proxima

Decisions, progress notes, session diary. Most recent first.

> *Entry format: `## YYYY-MM-DD — [what changed] | [why] | [next]`*

---

## 2026-07-10 — Planets mini-view (log-AU system strips)

Enriched the catalogue with **per-planet detail** for all 52 planets across the
23 host systems + the Sun: `PLANETS` dict in the builder → `planet_data` in the
JSON, each planet carrying `(a AU, mass M⊕, discovery year, temperate flag,
disputed flag)` from the discovery literature. Count-checked against the
existing `planets` fields (no mismatches).

The info card now renders a **system strip** for any planet-host: an inline SVG
with the host star peeking in from the left, planets as dots on a **log-AU
axis** (ticks 0.1/1/10 AU), dot size = mass class, colour = rocky tan /
Neptune teal / Jovian orange, **green ring = temperate orbit**, dashed =
disputed (Kapteyn b, 40 Eri b, the Wolf 359 candidates). Tapping a dot prints
its numbers (a, mass — M⊕ or MJ, year, flags). The Sun's own strip doubles as
a legend by familiarity: inner rockies, ringed Earth/Mars, big Jupiter/Saturn,
teal ice giants.

Verified headlessly: Tau Ceti (4 dots, e/f ringed) and the Sun (8 dots) render;
a probe-tap on Earth returned "Earth · 1 AU · 1 M⊕ · temperate".

## 2026-07-10 — OG image, mobile pass, 3D grid, trail arrows

**OG/social card.** Orrery-style meta tags (og:/twitter:, image URLs pre-pointed
at the future Pages home). `?og` URL param = clean-capture mode (UI hidden,
wordmark enlarged, trails on). Captured headlessly at 1200×630 → `web/og.jpg`.
Headless gotchas learned: `--disable-gpu` kills WebGL context creation → the
whole ES module dies (use `--use-angle=swiftshader --enable-unsafe-swiftshader`);
headless Chrome enforces a ~500px minimum window width, so "375px" screenshots
are actually 500px layouts clipped — the missing mobile toggle chip was a
capture artefact, not a bug (proved via a temporary ?debug DOM probe).

**Mobile pass.** ≤640px: controls collapse behind a ☰ chip (slide-in sheet,
auto-closes on star select), info card becomes a full-width sheet, time bar goes
full-width, legend/hint hidden, bigger touch targets. Mid widths (≤1120px): the
centred time bar used to overlap the corner panels — now docks between the
legend and the right edge; hint hides earlier.

**Soft 3D grid** (user request): light-grey semi-transparent lattice
(5-ly spacing over ±15 ly) with brighter axes through the Sun at the origin;
own toggle (default on); re-orients with the galactic/equatorial view. First
pass was too dark against the background — brightened to #aab3d0 @ 0.22.

**Trail arrows** (user request): each motion trail now ends in a colour-matched
cone at the +80,000 yr end, marking the star's direction of travel.

Verified headlessly at 1400/1000/500px widths: grid legible, no panel overlap,
chip toggles the sheet (`controls: none → block`), arrows render.

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
