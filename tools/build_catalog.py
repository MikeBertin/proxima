#!/usr/bin/env python3
"""
Proxima — build the local stellar-neighbourhood catalogue.

Curated table of every stellar (and notable sub-stellar) object within ~5 pc
(~16.4 ly) of the Sun, sourced from the RECONS / Gliese census as tabulated on
Wikipedia's "List of nearest stars" (astrometry cross-checked 2026-07-04).

Each row carries the *observed* quantities — RA, Dec, distance, spectral type,
mass — plus derived display fields (colour, radius) and known-planet counts.
We convert equatorial coordinates to a right-handed Cartesian frame in
light-years (X → vernal equinox, Y → RA 6h in the equatorial plane, Z → north
celestial pole) so the web viewer can plot real 3D positions.

Run:  python3 tools/build_catalog.py
Out:  web/data/stars.json
"""
import json
import math
import os

# --- helpers ---------------------------------------------------------------

def hms(h, m, s):
    """Right ascension h:m:s -> degrees."""
    return (h + m / 60 + s / 3600) * 15.0

def dms(sign, d, m, s):
    """Declination d:m:s -> degrees (sign = +1 / -1)."""
    return sign * (d + m / 60 + s / 3600)

def cartesian(ra_deg, dec_deg, dist_ly):
    ra = math.radians(ra_deg)
    dec = math.radians(dec_deg)
    return (
        dist_ly * math.cos(dec) * math.cos(ra),
        dist_ly * math.cos(dec) * math.sin(ra),
        dist_ly * math.sin(dec),
    )

# Approximate stellar colour (hex) from spectral class, à la a real HR diagram.
SPECTRAL_COLOUR = {
    "O": "#9bb0ff", "B": "#aabfff", "A": "#f8f7ff", "F": "#fff4ea",
    "G": "#fff2a1", "K": "#ffcc6f", "M": "#ff7b4d",
    "L": "#c1440e", "T": "#8a2be2", "Y": "#4b2e83",
    "D": "#dfe9ff",  # white dwarf
}

def colour_for(spectral):
    cls = spectral[0].upper()
    return SPECTRAL_COLOUR.get(cls, "#ffffff")

def kind_for(spectral):
    c = spectral[0].upper()
    if c == "D":
        return "white dwarf"
    if c in ("L", "T", "Y"):
        return "brown dwarf"
    return "main-sequence"

# --- the catalogue ---------------------------------------------------------
# Fields per object:
#   name, other (common/other name), ra(h,m,s), dec(sign,d,m,s),
#   dist_ly, spectral, mass (Msun), radius (Rsun, approx),
#   planets (count of confirmed/notable), planet_names (list),
#   discovered (year or era, star as a catalogued object),
#   system (grouping key), note
S = []
def star(**kw):
    S.append(kw)

# The Sun — anchor at the origin.
star(name="Sun", other="Sol", ra=(0,0,0), dec=(1,0,0,0), dist_ly=0.0,
     spectral="G2V", mass=1.0, radius=1.0, planets=8,
     planet_names=["Mercury","Venus","Earth","Mars","Jupiter","Saturn","Uranus","Neptune"],
     discovered="—", system="Sun", note="Home. The reference point for everything here.")

# Alpha Centauri system + Proxima (nearest stars).
star(name="Proxima Centauri", other="Alpha Cen C", ra=(14,29,43.0), dec=(-1,62,40,46),
     dist_ly=4.2465, spectral="M5.5Ve", mass=0.122, radius=0.15, planets=3,
     planet_names=["Proxima b","Proxima c","Proxima d"],
     discovered=1915, system="Alpha Centauri",
     note="The single nearest star to the Sun. Hosts a temperate rocky planet (Proxima b).")
star(name="Rigil Kentaurus", other="Alpha Centauri A", ra=(14,39,36.5), dec=(-1,60,50,2),
     dist_ly=4.3441, spectral="G2V", mass=1.079, radius=1.22, planets=0,
     planet_names=[], discovered="antiquity", system="Alpha Centauri",
     note="A near-twin of the Sun; brightest component of the closest star system.")
star(name="Toliman", other="Alpha Centauri B", ra=(14,39,35.1), dec=(-1,60,50,14),
     dist_ly=4.3441, spectral="K1V", mass=0.909, radius=0.86, planets=0,
     planet_names=[], discovered="antiquity", system="Alpha Centauri",
     note="Orange dwarf orbiting Alpha Cen A every ~80 years.")

star(name="Barnard's Star", other="", ra=(17,57,48.5), dec=(1,4,41,36),
     dist_ly=5.9629, spectral="M4.0Ve", mass=0.144, radius=0.19, planets=1,
     planet_names=["Barnard b"], discovered=1916, system="Barnard's Star",
     note="Highest proper motion of any known star. A sub-Earth planet was confirmed in 2024.")

star(name="Luhman 16 A", other="WISE 1049-5319 A", ra=(10,49,18.9), dec=(-1,53,19,10),
     dist_ly=6.5102, spectral="L7.5", mass=0.032, radius=0.10, planets=0,
     planet_names=[], discovered=2013, system="Luhman 16",
     note="Nearest brown-dwarf pair; discovered only in 2013 despite its proximity.")
star(name="Luhman 16 B", other="WISE 1049-5319 B", ra=(10,49,18.9), dec=(-1,53,19,10),
     dist_ly=6.5102, spectral="T0.5", mass=0.027, radius=0.10, planets=0,
     planet_names=[], discovered=2013, system="Luhman 16",
     note="Shows weather — patchy clouds rotating in and out of view.")

star(name="WISE 0855-0714", other="", ra=(8,55,10.8), dec=(-1,7,14,43),
     dist_ly=7.43, spectral="Y4", mass=0.007, radius=0.09, planets=0,
     planet_names=[], discovered=2014, system="WISE 0855",
     note="Coldest known object of its kind (~250 K); a rogue sub-brown dwarf.")

star(name="Wolf 359", other="CN Leonis", ra=(10,56,29.2), dec=(1,7,0,53),
     dist_ly=7.856, spectral="M6.0V", mass=0.090, radius=0.16, planets=2,
     planet_names=["Wolf 359 b (cand.)","Wolf 359 c (cand.)"], discovered=1918,
     system="Wolf 359", note="A faint, active flare star; a science-fiction fixture.")

star(name="Lalande 21185", other="", ra=(11,3,20.2), dec=(1,35,58,12),
     dist_ly=8.3044, spectral="M2.0V", mass=0.390, radius=0.39, planets=2,
     planet_names=["Lalande 21185 b","Lalande 21185 c"], discovered=1801,
     system="Lalande 21185", note="Brightest red dwarf in the northern sky; hosts giant planets.")

star(name="Sirius A", other="Alpha Canis Majoris", ra=(6,45,8.9), dec=(-1,16,42,58),
     dist_ly=8.7094, spectral="A1V", mass=2.063, radius=1.71, planets=0,
     planet_names=[], discovered="antiquity", system="Sirius",
     note="The brightest star in Earth's night sky.")
star(name="Sirius B", other="", ra=(6,45,8.9), dec=(-1,16,42,58),
     dist_ly=8.7094, spectral="DA2", mass=1.018, radius=0.0084, planets=0,
     planet_names=[], discovered=1862, system="Sirius",
     note="Nearest white dwarf — a Sun's-worth of mass in an Earth-sized sphere.")

star(name="Gliese 65 A", other="BL Ceti / Luyten 726-8 A", ra=(1,39,1.3), dec=(-1,17,57,1),
     dist_ly=8.770, spectral="M5.5Ve", mass=0.102, radius=0.14, planets=0,
     planet_names=[], discovered=1948, system="Gliese 65",
     note="Close binary of flare stars.")
star(name="Gliese 65 B", other="UV Ceti", ra=(1,39,1.3), dec=(-1,17,57,1),
     dist_ly=8.770, spectral="M6.0Ve", mass=0.100, radius=0.14, planets=0,
     planet_names=[], discovered=1948, system="Gliese 65",
     note="The prototype UV Ceti flare star — brightens dramatically in minutes.")

star(name="Ross 154", other="V1216 Sagittarii", ra=(18,49,49.4), dec=(-1,23,50,10),
     dist_ly=9.7063, spectral="M3.5Ve", mass=0.17, radius=0.24, planets=0,
     planet_names=[], discovered=1925, system="Ross 154", note="A young, active flare star.")

star(name="Ross 248", other="HH Andromedae", ra=(23,41,54.7), dec=(1,44,10,30),
     dist_ly=10.3057, spectral="M5.5Ve", mass=0.136, radius=0.16, planets=0,
     planet_names=[], discovered=1926, system="Ross 248",
     note="Will become the nearest star to the Sun in ~36,000 years.")

star(name="Epsilon Eridani", other="Ran", ra=(3,32,55.8), dec=(-1,9,27,30),
     dist_ly=10.4749, spectral="K2V", mass=0.820, radius=0.74, planets=1,
     planet_names=["Epsilon Eridani b (Ægir)"], discovered="antiquity", system="Epsilon Eridani",
     note="A young Sun-like star with a Jupiter-mass planet and two debris belts.")

star(name="Lacaille 9352", other="GJ 887", ra=(23,5,52.0), dec=(-1,35,51,11),
     dist_ly=10.7241, spectral="M0.5V", mass=0.486, radius=0.47, planets=2,
     planet_names=["GJ 887 b","GJ 887 c"], discovered=1752, system="Lacaille 9352",
     note="One of the brightest and quietest red dwarfs; a prime imaging target.")

star(name="Ross 128", other="FI Virginis", ra=(11,47,44.4), dec=(1,0,48,16),
     dist_ly=11.0074, spectral="M4.0Vn", mass=0.168, radius=0.20, planets=1,
     planet_names=["Ross 128 b"], discovered=1926, system="Ross 128",
     note="A quiet red dwarf with a temperate Earth-mass planet.")

star(name="EZ Aquarii A", other="Luyten 789-6", ra=(22,38,33.4), dec=(-1,15,17,57),
     dist_ly=11.109, spectral="M5.0Ve", mass=0.11, radius=0.13, planets=0,
     planet_names=[], discovered=1935, system="EZ Aquarii", note="Triple flare-star system.")

star(name="61 Cygni A", other="Bessel's Star", ra=(21,6,53.9), dec=(1,38,44,58),
     dist_ly=11.4039, spectral="K5.0V", mass=0.70, radius=0.67, planets=0,
     planet_names=[], discovered=1804, system="61 Cygni",
     note="First star to have its distance measured (Bessel, 1838).")
star(name="61 Cygni B", other="", ra=(21,6,55.3), dec=(1,38,44,31),
     dist_ly=11.41, spectral="K7.0V", mass=0.63, radius=0.60, planets=0,
     planet_names=[], discovered=1804, system="61 Cygni", note="Orange-dwarf companion.")

star(name="Procyon A", other="Alpha Canis Minoris", ra=(7,39,18.1), dec=(1,5,13,30),
     dist_ly=11.463, spectral="F5IV-V", mass=1.499, radius=2.05, planets=0,
     planet_names=[], discovered="antiquity", system="Procyon",
     note="Eighth-brightest star in the night sky.")
star(name="Procyon B", other="", ra=(7,39,18.1), dec=(1,5,13,30),
     dist_ly=11.463, spectral="DQZ", mass=0.602, radius=0.012, planets=0,
     planet_names=[], discovered=1896, system="Procyon", note="Faint white-dwarf companion.")

star(name="Struve 2398 A", other="GJ 725 A", ra=(18,42,46.7), dec=(1,59,37,49),
     dist_ly=11.4908, spectral="M3.0V", mass=0.334, radius=0.35, planets=0,
     planet_names=[], discovered=1832, system="Struve 2398", note="Red-dwarf binary.")
star(name="Struve 2398 B", other="GJ 725 B", ra=(18,42,46.9), dec=(1,59,37,37),
     dist_ly=11.49, spectral="M3.5V", mass=0.248, radius=0.27, planets=0,
     planet_names=[], discovered=1832, system="Struve 2398", note="")

star(name="Groombridge 34 A", other="GX Andromedae", ra=(0,18,22.9), dec=(1,44,1,23),
     dist_ly=11.6191, spectral="M1.5V", mass=0.38, radius=0.38, planets=1,
     planet_names=["Groombridge 34 Ab"], discovered=1838, system="Groombridge 34",
     note="Flare-star binary; the primary hosts a super-Earth.")
star(name="Groombridge 34 B", other="GQ Andromedae", ra=(0,18,22.9), dec=(1,44,1,23),
     dist_ly=11.6191, spectral="M3.5V", mass=0.15, radius=0.17, planets=0,
     planet_names=[], discovered=1838, system="Groombridge 34", note="")

star(name="DX Cancri", other="G 51-15", ra=(8,29,49.5), dec=(1,26,46,37),
     dist_ly=11.6797, spectral="M6.5Ve", mass=0.09, radius=0.11, planets=0,
     planet_names=[], discovered=1900, system="DX Cancri",
     note="One of the least luminous stars known.")

star(name="Epsilon Indi A", other="", ra=(22,3,21.7), dec=(-1,56,47,10),
     dist_ly=11.8670, spectral="K5Ve", mass=0.754, radius=0.73, planets=1,
     planet_names=["Epsilon Indi Ab"], discovered="antiquity", system="Epsilon Indi",
     note="A Sun-like orange dwarf with a cold Jovian planet and two brown-dwarf companions.")

star(name="Tau Ceti", other="", ra=(1,44,4.1), dec=(-1,15,56,15),
     dist_ly=11.9118, spectral="G8.5V", mass=0.783, radius=0.79, planets=4,
     planet_names=["Tau Ceti e","Tau Ceti f","Tau Ceti g","Tau Ceti h"],
     discovered="antiquity", system="Tau Ceti",
     note="Nearest single Sun-like star; a candidate rocky planet sits near its habitable zone.")

star(name="GJ 1061", other="", ra=(3,35,59.7), dec=(-1,44,30,45),
     dist_ly=11.9839, spectral="M5.5V", mass=0.113, radius=0.16, planets=3,
     planet_names=["GJ 1061 b","GJ 1061 c","GJ 1061 d"], discovered=1974,
     system="GJ 1061", note="A quiet red dwarf with a compact planetary system.")

star(name="YZ Ceti", other="", ra=(1,12,30.6), dec=(-1,16,59,56),
     dist_ly=12.1222, spectral="M4.5V", mass=0.130, radius=0.17, planets=3,
     planet_names=["YZ Ceti b","YZ Ceti c","YZ Ceti d"], discovered=1946,
     system="YZ Ceti", note="Three sub-Earth planets; a possible radio-detected magnetic field.")

star(name="Luyten's Star", other="GJ 273", ra=(7,27,24.5), dec=(1,5,13,33),
     dist_ly=12.3485, spectral="M3.5Vn", mass=0.26, radius=0.29, planets=2,
     planet_names=["GJ 273 b","GJ 273 c"], discovered=1935, system="Luyten's Star",
     note="Hosts a temperate super-Earth; target of a 2017 interstellar message.")

star(name="Teegarden's Star", other="", ra=(2,53,0.9), dec=(1,16,52,53),
     dist_ly=12.4970, spectral="M6.5V", mass=0.08, radius=0.11, planets=3,
     planet_names=["Teegarden b","Teegarden c","Teegarden d"], discovered=2003,
     system="Teegarden's Star",
     note="A tiny, ancient red dwarf with two of the most Earth-like planets known.")

star(name="Kapteyn's Star", other="", ra=(5,11,40.6), dec=(-1,45,1,6),
     dist_ly=12.8308, spectral="M1.5VI", mass=0.281, radius=0.29, planets=1,
     planet_names=["Kapteyn b (disputed)"], discovered=1898, system="Kapteyn's Star",
     note="A halo star from an ancient, disrupted dwarf galaxy — orbiting the wrong way round the Milky Way.")

star(name="Lacaille 8760", other="AX Microscopii", ra=(21,17,15.3), dec=(-1,38,52,3),
     dist_ly=12.9472, spectral="M0.0V", mass=0.60, radius=0.51, planets=0,
     planet_names=[], discovered=1752, system="Lacaille 8760",
     note="One of the brightest red dwarfs visible from Earth.")

star(name="Kruger 60 A", other="", ra=(22,27,59.5), dec=(1,57,41,45),
     dist_ly=13.0724, spectral="M3.0V", mass=0.271, radius=0.35, planets=0,
     planet_names=[], discovered=1890, system="Kruger 60", note="Red-dwarf binary.")
star(name="Kruger 60 B", other="DO Cephei", ra=(22,27,59.5), dec=(1,57,41,45),
     dist_ly=13.0724, spectral="M4.0V", mass=0.176, radius=0.24, planets=0,
     planet_names=[], discovered=1890, system="Kruger 60", note="A flare star.")

star(name="Wolf 1061", other="GJ 628", ra=(16,30,18.1), dec=(-1,12,39,45),
     dist_ly=14.05, spectral="M3.0V", mass=0.294, radius=0.31, planets=3,
     planet_names=["Wolf 1061 b","Wolf 1061 c","Wolf 1061 d"], discovered=1919,
     system="Wolf 1061", note="Hosts a potentially habitable super-Earth (Wolf 1061 c).")

star(name="Van Maanen's Star", other="", ra=(0,49,9.9), dec=(1,5,23,19),
     dist_ly=14.0718, spectral="DZ7", mass=0.67, radius=0.011, planets=0,
     planet_names=[], discovered=1917, system="Van Maanen's Star",
     note="Nearest solitary white dwarf; its atmosphere is polluted by shredded planetary debris.")

star(name="Gliese 1", other="GJ 1", ra=(0,5,24.4), dec=(-1,37,21,27),
     dist_ly=14.1747, spectral="M1.5V", mass=0.45, radius=0.45, planets=0,
     planet_names=[], discovered=1900, system="Gliese 1",
     note="A metal-poor, high-velocity red dwarf.")

star(name="TZ Arietis", other="GJ 83.1", ra=(2,0,13.2), dec=(1,13,3,8),
     dist_ly=14.578, spectral="M4.5V", mass=0.14, radius=0.17, planets=1,
     planet_names=["TZ Arietis b"], discovered=1900, system="TZ Arietis", note="A flare star.")

star(name="Gliese 674", other="", ra=(17,28,39.9), dec=(-1,46,53,43),
     dist_ly=14.8492, spectral="M3.0V", mass=0.35, radius=0.36, planets=1,
     planet_names=["Gliese 674 b"], discovered=1957, system="Gliese 674",
     note="Hosts a Neptune-mass planet on a close orbit.")

star(name="Gliese 687", other="", ra=(17,36,25.9), dec=(1,68,20,21),
     dist_ly=14.8395, spectral="M3.0V", mass=0.401, radius=0.42, planets=2,
     planet_names=["Gliese 687 b","Gliese 687 c"], discovered=1900, system="Gliese 687",
     note="A nearby red dwarf with two known planets.")

star(name="GJ 1245 A", other="", ra=(19,53,54.2), dec=(1,44,24,55),
     dist_ly=15.2001, spectral="M5.5V", mass=0.11, radius=0.14, planets=0,
     planet_names=[], discovered=1900, system="GJ 1245", note="Triple red-dwarf system.")

star(name="Gliese 876", other="", ra=(22,53,16.7), dec=(-1,14,15,49),
     dist_ly=15.2382, spectral="M3.5V", mass=0.37, radius=0.38, planets=4,
     planet_names=["Gliese 876 d","Gliese 876 c","Gliese 876 b","Gliese 876 e"],
     discovered=1900, system="Gliese 876",
     note="First red dwarf found to host planets; a resonant chain of four worlds.")

star(name="Gliese 832", other="", ra=(21,33,34.0), dec=(-1,49,0,32),
     dist_ly=16.2005, spectral="M1.5V", mass=0.45, radius=0.48, planets=2,
     planet_names=["Gliese 832 b","Gliese 832 c"], discovered=1900, system="Gliese 832",
     note="A Jupiter analogue plus a super-Earth — a scaled-down Solar System.")

star(name="40 Eridani A", other="Keid", ra=(4,15,16.3), dec=(-1,7,39,10),
     dist_ly=16.333, spectral="K0.5V", mass=0.84, radius=0.81, planets=1,
     planet_names=["40 Eridani b (disputed)"], discovered="antiquity", system="40 Eridani",
     note="Triple system; in Star Trek lore, the star of the planet Vulcan.")
star(name="40 Eridani B", other="", ra=(4,15,16.3), dec=(-1,7,39,10),
     dist_ly=16.333, spectral="DA4", mass=0.573, radius=0.014, planets=0,
     planet_names=[], discovered=1783, system="40 Eridani",
     note="The most easily observed white dwarf in the sky.")
star(name="40 Eridani C", other="", ra=(4,15,16.3), dec=(-1,7,39,10),
     dist_ly=16.333, spectral="M4.5V", mass=0.20, radius=0.23, planets=0,
     planet_names=[], discovered=1783, system="40 Eridani", note="Red-dwarf flare star.")

# --- build output ----------------------------------------------------------

def process():
    out = []
    # Track co-located companions so we can nudge them apart for rendering.
    seen = {}
    for s in S:
        ra_deg = hms(*s["ra"])
        dec_deg = dms(*s["dec"])
        x, y, z = cartesian(ra_deg, dec_deg, s["dist_ly"])
        key = (round(ra_deg, 4), round(dec_deg, 4), round(s["dist_ly"], 3))
        n = seen.get(key, 0)
        seen[key] = n + 1
        if n:  # nth companion at identical coords — nudge ~0.03 ly so it renders distinctly
            ang = n * 2.399963  # golden angle
            x += 0.035 * math.cos(ang)
            y += 0.035 * math.sin(ang)
            z += 0.02 * n
        out.append({
            "name": s["name"],
            "other": s["other"],
            "system": s["system"],
            "ra_deg": round(ra_deg, 4),
            "dec_deg": round(dec_deg, 4),
            "dist_ly": s["dist_ly"],
            "dist_pc": round(s["dist_ly"] / 3.26156, 3),
            "spectral": s["spectral"],
            "kind": kind_for(s["spectral"]),
            "mass": s["mass"],
            "radius": s["radius"],
            "colour": colour_for(s["spectral"]),
            "planets": s["planets"],
            "planet_names": s["planet_names"],
            "discovered": s["discovered"],
            "note": s["note"],
            "x": round(x, 4), "y": round(y, 4), "z": round(z, 4),
        })
    return out

def dir_vector(ra_deg, dec_deg):
    x, y, z = cartesian(ra_deg, dec_deg, 1.0)
    return {"x": round(x, 5), "y": round(y, 5), "z": round(z, 5)}

def main():
    stars = process()
    stars.sort(key=lambda s: s["dist_ly"])
    meta = {
        "generated": "2026-07-04",
        "count": len(stars),
        "cutoff_ly": 16.4,
        "cutoff_pc": 5.03,
        "frame": "Equatorial Cartesian, light-years. X->vernal equinox, Z->north celestial pole.",
        "source": "RECONS / Gliese census via Wikipedia 'List of nearest stars' (cross-checked 2026-07-04).",
        # Direction to the Galactic Centre (Sgr A*) and the North Galactic Pole,
        # so the viewer can draw the Milky Way plane and centre correctly.
        "galactic_centre": dir_vector(266.41683, -29.00781),
        "galactic_north_pole": dir_vector(192.85949, 27.12825),
        "galactic_centre_dist_ly": 26000,
    }
    payload = {"meta": meta, "stars": stars}
    here = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(here, "..", "web", "data", "stars.json")
    with open(out_path, "w") as f:
        json.dump(payload, f, indent=1)
    print(f"Wrote {len(stars)} objects -> {os.path.relpath(out_path)}")
    withp = sum(1 for s in stars if s["planets"] > 0)
    print(f"  {withp} host known/notable planets; "
          f"{sum(s['planets'] for s in stars)} planets total.")

if __name__ == "__main__":
    main()
