# STATUS — Project Proxima

State: 🟢 M1–M4 BUILT & VERIFIED (map + scrub + polish + planets mini-view)
Last action: 2026-07-10 — M4 planets mini-view: all 52 planets enriched with a/mass/year/temperate/disputed (PLANETS dict in builder → planet_data in JSON); info card renders a log-AU system strip per host (dot size = mass class, colour = rocky/Neptune/Jovian, green ring = temperate, dashed = disputed; tap a dot for its numbers). Verified headlessly (Tau Ceti, Sun; probe-tap on Earth OK).
Next action: Publish decision — public repo + GitHub Pages, sister to Orrery.
Blocked by: Nothing.
Next milestone: M5 publish decision.
Outcome: Working local 3D map of the Sun's stellar neighbourhood, real astrometry, sister to Orrery.
Notes:
- Local repo only for now (own git repo, no remote). Publishing to GitHub Pages deferred (M3) — same route as Orrery when ready.
- Data source: RECONS/Gliese census via Wikipedia "List of nearest stars", cross-checked 2026-07-04. 23 planet-hosting systems, 52 planets.
- Serve: `python3 -m http.server 7799 --directory web`. Rebuild data: `python3 tools/build_catalog.py`.

> *Update MEMORY.md when significant milestones are reached or the project closes.*
