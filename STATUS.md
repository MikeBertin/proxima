# STATUS — Project Proxima

State: 🟢 M1–M3 BUILT & VERIFIED (map + scrub + polish)
Last action: 2026-07-10 — M3 polish: OG image (web/og.jpg via headless capture, ?og mode) + meta tags; mobile pass (☰ controls sheet ≤640px, responsive time bar ≤1120px); soft light-grey 3D grid lattice (5-ly spacing, Sun at origin, frame-aware); direction arrowheads on motion trails. Verified headlessly at 1400/1000/500px.
Next action: Per-star planets mini-view, or the publish decision (public repo + Pages, sister to Orrery).
Blocked by: Nothing.
Next milestone: M4 planets mini-view / M5 publish decision.
Outcome: Working local 3D map of the Sun's stellar neighbourhood, real astrometry, sister to Orrery.
Notes:
- Local repo only for now (own git repo, no remote). Publishing to GitHub Pages deferred (M3) — same route as Orrery when ready.
- Data source: RECONS/Gliese census via Wikipedia "List of nearest stars", cross-checked 2026-07-04. 23 planet-hosting systems, 52 planets.
- Serve: `python3 -m http.server 7799 --directory web`. Rebuild data: `python3 tools/build_catalog.py`.

> *Update MEMORY.md when significant milestones are reached or the project closes.*
