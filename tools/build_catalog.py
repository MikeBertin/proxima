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

# --- per-planet detail for the info-card mini-view --------------------------
# Tuples: (name, a_AU, mass_Mearth, year, temperate/hz, disputed).
# a and mass from the discovery/refinement literature (approximate where the
# literature disagrees); "temperate" = broadly habitable-zone by the usual
# conservative-to-optimistic definitions, not a claim of habitability.
PLANETS = {
    "Sun": [
        ("Mercury", 0.39, 0.055, "—", False, False),
        ("Venus", 0.72, 0.815, "—", False, False),
        ("Earth", 1.0, 1.0, "—", True, False),
        ("Mars", 1.52, 0.107, "—", True, False),
        ("Jupiter", 5.2, 318, "—", False, False),
        ("Saturn", 9.54, 95, "—", False, False),
        ("Uranus", 19.2, 14.5, 1781, False, False),
        ("Neptune", 30.1, 17.1, 1846, False, False),
    ],
    "Proxima Centauri": [
        ("Proxima d", 0.029, 0.26, 2022, False, False),
        ("Proxima b", 0.0485, 1.07, 2016, True, False),
        ("Proxima c", 1.49, 7.0, 2019, False, False),
    ],
    "Barnard's Star": [("Barnard b", 0.023, 0.37, 2024, False, False)],
    "Wolf 359": [
        ("Wolf 359 c", 0.018, 3.8, 2019, False, True),
        ("Wolf 359 b", 1.845, 44, 2019, False, True),
    ],
    "Lalande 21185": [
        ("Lalande 21185 b", 0.079, 2.7, 2017, False, False),
        ("Lalande 21185 c", 2.94, 18, 2021, False, False),
    ],
    "Epsilon Eridani": [("Ægir (b)", 3.5, 210, 2000, False, False)],
    "Lacaille 9352": [
        ("GJ 887 b", 0.068, 4.2, 2020, False, False),
        ("GJ 887 c", 0.12, 7.6, 2020, False, False),
    ],
    "Ross 128": [("Ross 128 b", 0.049, 1.35, 2017, True, False)],
    "Groombridge 34 A": [("Groombridge 34 Ab", 0.072, 3.0, 2014, False, False)],
    "Epsilon Indi A": [("Epsilon Indi Ab", 11.6, 2000, 2018, False, False)],
    "Tau Ceti": [
        ("Tau Ceti g", 0.133, 1.75, 2017, False, False),
        ("Tau Ceti h", 0.243, 1.83, 2017, False, False),
        ("Tau Ceti e", 0.538, 3.9, 2012, True, False),
        ("Tau Ceti f", 1.334, 3.9, 2012, True, False),
    ],
    "GJ 1061": [
        ("GJ 1061 b", 0.021, 0.94, 2019, False, False),
        ("GJ 1061 c", 0.035, 1.75, 2019, True, False),
        ("GJ 1061 d", 0.054, 1.68, 2019, True, False),
    ],
    "YZ Ceti": [
        ("YZ Ceti b", 0.016, 0.70, 2017, False, False),
        ("YZ Ceti c", 0.022, 0.98, 2017, False, False),
        ("YZ Ceti d", 0.028, 1.09, 2017, False, False),
    ],
    "Luyten's Star": [
        ("GJ 273 c", 0.036, 1.18, 2017, False, False),
        ("GJ 273 b", 0.091, 2.89, 2017, True, False),
    ],
    "Teegarden's Star": [
        ("Teegarden b", 0.0252, 1.05, 2019, True, False),
        ("Teegarden c", 0.0443, 1.11, 2019, True, False),
        ("Teegarden d", 0.0791, 0.82, 2024, False, False),
    ],
    "Kapteyn's Star": [("Kapteyn b", 0.168, 4.8, 2014, True, True)],
    "Wolf 1061": [
        ("Wolf 1061 b", 0.037, 1.9, 2015, False, False),
        ("Wolf 1061 c", 0.089, 3.4, 2015, True, False),
        ("Wolf 1061 d", 0.47, 7.7, 2015, False, False),
    ],
    "TZ Arietis": [("TZ Arietis b", 0.88, 21, 2020, False, False)],
    "Gliese 674": [("Gliese 674 b", 0.039, 12, 2007, False, False)],
    "Gliese 687": [
        ("Gliese 687 b", 0.16, 18, 2014, False, False),
        ("Gliese 687 c", 1.16, 16, 2020, False, False),
    ],
    "Gliese 876": [
        ("Gliese 876 d", 0.021, 6.8, 2005, False, False),
        ("Gliese 876 c", 0.13, 227, 2000, False, False),
        ("Gliese 876 b", 0.21, 723, 1998, False, False),
        ("Gliese 876 e", 0.33, 15, 2010, False, False),
    ],
    "Gliese 832": [
        ("Gliese 832 c", 0.16, 5.4, 2014, True, False),
        ("Gliese 832 b", 3.56, 216, 2008, False, False),
    ],
    "40 Eridani A": [("40 Eridani b", 0.215, 8.5, 2018, False, True)],
}

# --- kinematics: proper motion + radial velocity ---------------------------
# Per object: (mu_RA*  [mas/yr, incl. cos-dec],  mu_Dec [mas/yr],  RV [km/s]).
# RV negative = approaching. Values from standard Hipparcos/Gaia-era literature.
# Companions inherit their primary's space motion. Where a value is genuinely
# uncertain (some ultracool dwarfs), RV defaults to 0 — it only affects how the
# line-of-sight distance evolves, not the on-sky streak.
KINEMATICS = {
    "Sun": (0, 0, 0),
    "Proxima Centauri": (-3781, 770, -22.4),
    "Rigil Kentaurus": (-3608, 686, -22.3),
    "Toliman": (-3608, 686, -22.3),
    "Barnard's Star": (-799, 10337, -110.5),
    "Luhman 16 A": (-2762, 358, 0),
    "Luhman 16 B": (-2762, 358, 0),
    "WISE 0855-0714": (-8117, 668, 0),
    "Wolf 359": (-3866, -2699, 19),
    "Lalande 21185": (-580, -4772, -85),
    "Sirius A": (-546, -1223, -5.5),
    "Sirius B": (-546, -1223, -5.5),
    "Gliese 65 A": (1972, -1523, 29),
    "Gliese 65 B": (1972, -1523, 29),
    "Ross 154": (637, -192, -4),
    "Ross 248": (112, -1592, -78),
    "Epsilon Eridani": (-975, 20, 15.5),
    "Lacaille 9352": (6767, 1327, 9.7),
    "Ross 128": (605, -1219, -31),
    "EZ Aquarii A": (-2097, -2493, 0),
    "61 Cygni A": (4133, 3202, -64.5),
    "61 Cygni B": (4107, 3144, -64),
    "Procyon A": (-716, -1035, -3.2),
    "Procyon B": (-716, -1035, -3.2),
    "Struve 2398 A": (-1330, 1840, 0),
    "Struve 2398 B": (-1400, 1850, 1),
    "Groombridge 34 A": (2889, 411, 12),
    "Groombridge 34 B": (2889, 411, 12),
    "DX Cancri": (-1118, -1204, 0),
    "Epsilon Indi A": (3967, -2537, -40),
    "Tau Ceti": (-1721, 854, -17),
    "GJ 1061": (745, -372, -20),
    "YZ Ceti": (1205, 1329, 28),
    "Luyten's Star": (571, -3694, 18),
    "Teegarden's Star": (3429, -3805, 68),
    "Kapteyn's Star": (6491, -5709, 245),
    "Lacaille 8760": (-3259, -1147, 21),
    "Kruger 60 A": (-870, -471, -34),
    "Kruger 60 B": (-870, -471, -34),
    "Wolf 1061": (-1129, -1074, -20),
    "Van Maanen's Star": (1236, -2709, 54),
    "Gliese 1": (5634, -2337, 24),
    "TZ Arietis": (1006, -1685, 34),
    "Gliese 674": (572, -880, -3),
    "Gliese 687": (-320, -1352, -29),
    "GJ 1245 A": (268, -1637, 5),
    "Gliese 876": (960, -675, -1.5),
    "Gliese 832": (-818, -1903, 13),
    "40 Eridani A": (-2240, -3420, -42),
    "40 Eridani B": (-2240, -3420, -42),
    "40 Eridani C": (-2240, -3420, -42),
}

K_VT = 4.740470          # km/s per (arcsec/yr · pc)
LY_PER_KMS_YR = 3.335641e-6   # 1 km/s sustained for 1 yr, expressed in light-years

def velocity_ly_per_yr(ra_deg, dec_deg, dist_pc, pm_ra_mas, pm_dec_mas, rv_kms):
    """Heliocentric space velocity -> (vx,vy,vz) in ly/yr, equatorial frame."""
    ra, dec = math.radians(ra_deg), math.radians(dec_deg)
    v_ra = K_VT * (pm_ra_mas / 1000.0) * dist_pc   # km/s, toward increasing RA
    v_dec = K_VT * (pm_dec_mas / 1000.0) * dist_pc  # km/s, toward increasing Dec
    v_r = rv_kms                                    # km/s, along line of sight
    r_hat = (math.cos(dec)*math.cos(ra), math.cos(dec)*math.sin(ra), math.sin(dec))
    a_hat = (-math.sin(ra), math.cos(ra), 0.0)
    d_hat = (-math.sin(dec)*math.cos(ra), -math.sin(dec)*math.sin(ra), math.cos(dec))
    vx = v_r*r_hat[0] + v_ra*a_hat[0] + v_dec*d_hat[0]
    vy = v_r*r_hat[1] + v_ra*a_hat[1] + v_dec*d_hat[1]
    vz = v_r*r_hat[2] + v_ra*a_hat[2] + v_dec*d_hat[2]
    f = LY_PER_KMS_YR
    return vx*f, vy*f, vz*f

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
        pm_ra, pm_dec, rv = KINEMATICS.get(s["name"], (0, 0, 0))
        vx, vy, vz = velocity_ly_per_yr(ra_deg, dec_deg, s["dist_ly"] / 3.26156,
                                        pm_ra, pm_dec, rv)
        pm_total = round(math.hypot(pm_ra, pm_dec), 1)
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
            "planet_data": [
                {"name": p[0], "a": p[1], "m": p[2], "yr": p[3], "hz": p[4], "disputed": p[5]}
                for p in PLANETS.get(s["name"], [])
            ],
            "pm": pm_total, "rv": rv,
            "x": round(x, 4), "y": round(y, 4), "z": round(z, 4),
            "vx": round(vx, 10), "vy": round(vy, 10), "vz": round(vz, 10),
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
