# STATUS — Project Proxima

State: 🚀 SHIPPED — LIVE at mikebertin.github.io/proxima
Last action: 2026-07-10 — M5 publish: public repo github.com/MikeBertin/proxima, Pages via .github/workflows/pages.yml (web/ folder, build_type=workflow). Live site verified: 51 stars, 52 planets, 28 hints served; full render checked headlessly. README got "Why Proxima" + live links per public-repo conventions.
Next action: None — project complete. (Optional future: candidate-planet refresh as new discoveries land; bump ?v= on any js/json change.)
Blocked by: Nothing.
Next milestone: —
Outcome: Working local 3D map of the Sun's stellar neighbourhood, real astrometry, sister to Orrery.
Notes:
- Local repo only for now (own git repo, no remote). Publishing to GitHub Pages deferred (M3) — same route as Orrery when ready.
- Data source: RECONS/Gliese census via Wikipedia "List of nearest stars", cross-checked 2026-07-04. 23 planet-hosting systems, 52 planets.
- Serve: `python3 -m http.server 7799 --directory web`. Rebuild data: `python3 tools/build_catalog.py`.

> *Update MEMORY.md when significant milestones are reached or the project closes.*
