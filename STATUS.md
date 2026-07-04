# STATUS — Project Proxima

State: 🟢 M1 BUILT & VERIFIED
Last action: 2026-07-04 — Scaffolded project; built catalogue (51 objects within 5 pc) + 3D Three.js viewer; verified in browser (render, galaxy plane, click→info card, camera-fly, deep-links, filters all working).
Next action: Decide milestone 2 focus — OG image + mobile pass, or the proper-motion "neighbourhood in N,000 years" time-scrub.
Blocked by: Nothing.
Next milestone: M2 polish (OG/mobile/planets mini-view/proper-motion scrub).
Outcome: Working local 3D map of the Sun's stellar neighbourhood, real astrometry, sister to Orrery.
Notes:
- Local repo only for now (own git repo, no remote). Publishing to GitHub Pages deferred (M3) — same route as Orrery when ready.
- Data source: RECONS/Gliese census via Wikipedia "List of nearest stars", cross-checked 2026-07-04. 23 planet-hosting systems, 52 planets.
- Serve: `python3 -m http.server 7799 --directory web`. Rebuild data: `python3 tools/build_catalog.py`.

> *Update MEMORY.md when significant milestones are reached or the project closes.*
