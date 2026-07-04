# STATUS — Project Proxima

State: 🟢 M1 + PROPER-MOTION SCRUB BUILT & VERIFIED
Last action: 2026-07-04 — Added the proper-motion time-scrub: real space-velocity vectors (μ + RV → 3D velocity) drive a ±80,000 yr slider with play/pause, a live "nearest star" readout, and motion trails. Verified in browser — reproduces published close approaches (Proxima 3.10 ly @ +28k, Ross 248 becomes nearest @ +36k = 3.02 ly, Barnard closes to 3.76 ly).
Next action: Decide remaining M2 polish — OG image, mobile pass, or per-star planets mini-view.
Blocked by: Nothing.
Next milestone: M2 remainder (OG/mobile/planets mini-view), then M3 publish decision.
Outcome: Working local 3D map of the Sun's stellar neighbourhood, real astrometry, sister to Orrery.
Notes:
- Local repo only for now (own git repo, no remote). Publishing to GitHub Pages deferred (M3) — same route as Orrery when ready.
- Data source: RECONS/Gliese census via Wikipedia "List of nearest stars", cross-checked 2026-07-04. 23 planet-hosting systems, 52 planets.
- Serve: `python3 -m http.server 7799 --directory web`. Rebuild data: `python3 tools/build_catalog.py`.

> *Update MEMORY.md when significant milestones are reached or the project closes.*
