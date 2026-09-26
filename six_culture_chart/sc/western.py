"""Step 4D: Western/Hellenistic (tropical, whole-sign, seven traditional planets)."""
from datetime import datetime, timedelta, timezone

import swisseph as swe

from .astro import angles, solar_longitude_crossing
from .common import SIGNS, TRADITIONAL, angdiff, deg_in_sign, jd_from_utc, norm, sign_of, utc_from_jd

DOMICILE = ["Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury", "Venus", "Mars",
            "Jupiter", "Saturn", "Saturn", "Jupiter"]
EXALT = {"Sun": (0, 19), "Moon": (1, 3), "Mercury": (5, 15), "Venus": (11, 27),
         "Mars": (9, 28), "Jupiter": (3, 15), "Saturn": (6, 21)}
# Dorothean triplicity rulers (day, night, participating)
TRIPLICITY = {"fire": ("Sun", "Jupiter", "Saturn"), "earth": ("Venus", "Moon", "Mars"),
              "air": ("Saturn", "Mercury", "Jupiter"), "water": ("Venus", "Mars", "Moon")}
ELEMENT = ["fire", "earth", "air", "water"]
# Egyptian bounds (Ptolemy, Tetrabiblos I.20, "Egyptian" table)
BOUNDS = [
    [("Jupiter", 6), ("Venus", 12), ("Mercury", 20), ("Mars", 25), ("Saturn", 30)],
    [("Venus", 8), ("Mercury", 14), ("Jupiter", 22), ("Saturn", 27), ("Mars", 30)],
    [("Mercury", 6), ("Jupiter", 12), ("Venus", 17), ("Mars", 24), ("Saturn", 30)],
    [("Mars", 7), ("Venus", 13), ("Mercury", 19), ("Jupiter", 26), ("Saturn", 30)],
    [("Jupiter", 6), ("Venus", 11), ("Saturn", 18), ("Mercury", 24), ("Mars", 30)],
    [("Mercury", 7), ("Venus", 17), ("Jupiter", 21), ("Mars", 28), ("Saturn", 30)],
    [("Saturn", 6), ("Mercury", 14), ("Jupiter", 21), ("Venus", 28), ("Mars", 30)],
    [("Mars", 7), ("Venus", 11), ("Mercury", 19), ("Jupiter", 24), ("Saturn", 30)],
    [("Jupiter", 12), ("Venus", 17), ("Mercury", 21), ("Saturn", 26), ("Mars", 30)],
    [("Mercury", 7), ("Jupiter", 14), ("Venus", 22), ("Saturn", 26), ("Mars", 30)],
    [("Mercury", 7), ("Venus", 13), ("Jupiter", 20), ("Mars", 25), ("Saturn", 30)],
    [("Venus", 12), ("Jupiter", 16), ("Mercury", 19), ("Mars", 28), ("Saturn", 30)],
]
CHALDEAN = ["Mars", "Sun", "Venus", "Mercury", "Moon", "Saturn", "Jupiter"]
DIURNAL = {"Sun", "Jupiter", "Saturn"}
NOCTURNAL = {"Moon", "Venus", "Mars"}
ASPECTS = {0: "conjunction", 2: "sextile", 3: "square", 4: "trine", 6: "opposition"}
KOLLESIS_ORB = 3.0


def bound_ruler(lon):
    d = deg_in_sign(lon)
    for p, end in BOUNDS[sign_of(lon)]:
        if d < end:
            return p


def face_ruler(lon):
    return CHALDEAN[int(norm(lon) // 10) % 7]


def essential(planet, lon, day):
    s = sign_of(lon)
    trip = TRIPLICITY[ELEMENT[s % 4]]
    r = {"domicile_ruler": DOMICILE[s], "exaltation_sign_of": [p for p, (es, _) in EXALT.items() if es == s],
         "triplicity_rulers": list(trip), "bound_ruler": bound_ruler(lon), "face_ruler": face_ruler(lon)}
    dign = []
    if DOMICILE[s] == planet:
        dign.append("domicile")
    if DOMICILE[(s + 6) % 12] == planet:
        dign.append("detriment")
    if planet in EXALT and EXALT[planet][0] == s:
        dign.append("exaltation")
    if planet in EXALT and (EXALT[planet][0] + 6) % 12 == s:
        dign.append("fall")
    if planet == (trip[0] if day else trip[1]):
        dign.append("triplicity (sect ruler)")
    elif planet in trip:
        dign.append("triplicity (other/participating)")
    if r["bound_ruler"] == planet:
        dign.append("bound")
    if r["face_ruler"] == planet:
        dign.append("face")
    r["planet_dignities"] = dign or ["peregrine"]
    return r


def chart(base, asc, mc, day):
    b = base["bodies"]
    asc_s = sign_of(asc)
    sun = b["Sun"]["lon"]
    planets = {}
    for p in TRADITIONAL:
        lon = b[p]["lon"]
        h = (sign_of(lon) - asc_s) % 12 + 1
        sep = abs(angdiff(lon, sun))
        vis = None
        if p not in ("Sun",):
            vis = ("cazimi" if sep <= 17 / 60 else "combust" if sep <= 8.5 else
                   "under the beams" if sep <= 15 else "free of the beams")
        diurnal = (p in DIURNAL) if p != "Mercury" else angdiff(lon, sun) < 0  # Mercury: morning star => diurnal
        sect = "of the sect" if diurnal == day else "contrary to sect"
        planets[p] = {"lon": lon, "sign": SIGNS[sign_of(lon)], "deg": deg_in_sign(lon), "whole_sign_house": h,
                      "angular": h in (1, 4, 7, 10), "angularity": "angular" if h in (1, 4, 7, 10) else
                      "succedent" if h in (2, 5, 8, 11) else "cadent",
                      "speed": b[p]["speed_deg_day"], "retrograde": b[p]["retrograde"],
                      "stationary": abs(b[p]["speed_deg_day"]) < 0.05 and p not in ("Sun", "Moon"),
                      "distance_from_sun": sep, "visibility": vis, "sect_status": sect,
                      "essential": essential(p, lon, day)}
    # Aspects: whole-sign configuration + degree-based applying/separating within 3 deg
    asps = []
    for i, x in enumerate(TRADITIONAL):
        for y in TRADITIONAL[i + 1:]:
            sd = (sign_of(b[y]["lon"]) - sign_of(b[x]["lon"])) % 12
            k = min(sd, 12 - sd)
            if k not in ASPECTS:
                continue
            exact = k * 30
            d = abs(angdiff(b[x]["lon"], b[y]["lon"]))
            orb = abs(d - exact)
            # applying if orb is shrinking
            dt = 1 / 24
            lx = b[x]["lon"] + b[x]["speed_deg_day"] * dt
            ly = b[y]["lon"] + b[y]["speed_deg_day"] * dt
            orb2 = abs(abs(angdiff(lx, ly)) - exact)
            asps.append({"a": x, "b": y, "aspect": ASPECTS[k], "by_sign": True, "degree_orb": orb,
                         "within_kollesis_3deg": orb <= KOLLESIS_ORB,
                         "applying": orb2 < orb})
    # Lots
    moon = b["Moon"]["lon"]
    fortune = norm(asc + moon - sun) if day else norm(asc + sun - moon)
    spirit = norm(asc + sun - moon) if day else norm(asc + moon - sun)
    # Dispositor chains (domicile)
    chains = {}
    for p in TRADITIONAL:
        seen = [p]
        cur = p
        while True:
            nxt = DOMICILE[sign_of(b[cur]["lon"])]
            if nxt in seen:
                seen.append(nxt)
                break
            seen.append(nxt)
            cur = nxt
        chains[p] = seen
    finals = {c[-1] for c in chains.values() if c[-1] == c[-2]}
    loops = sorted({tuple(sorted(c[c.index(c[-1]):-1])) for c in chains.values() if c[-1] != c[-2]})
    houses = {h: {"sign": SIGNS[(asc_s + h - 1) % 12], "ruler": DOMICILE[(asc_s + h - 1) % 12],
                  "occupants": [p for p in TRADITIONAL if planets[p]["whole_sign_house"] == h]}
              for h in range(1, 13)}
    for h in houses.values():
        r = h["ruler"]
        h["ruler_condition"] = {"sign": planets[r]["sign"], "house": planets[r]["whole_sign_house"],
                                "dignities": planets[r]["essential"]["planet_dignities"],
                                "retrograde": planets[r]["retrograde"], "visibility": planets[r]["visibility"]}
    return {"asc": {"lon": asc, "sign": SIGNS[asc_s], "deg": deg_in_sign(asc)},
            "mc": {"lon": mc, "sign": SIGNS[sign_of(mc)], "deg": deg_in_sign(mc),
                   "whole_sign_house_of_mc": (sign_of(mc) - asc_s) % 12 + 1},
            "sect": "day" if day else "night", "planets": planets, "aspects": asps,
            "lots": {"fortune": {"lon": fortune, "sign": SIGNS[sign_of(fortune)],
                                 "house": (sign_of(fortune) - asc_s) % 12 + 1,
                                 "formula": "day: Asc + Moon - Sun" if day else "night: Asc + Sun - Moon"},
                     "spirit": {"lon": spirit, "sign": SIGNS[sign_of(spirit)],
                                "house": (sign_of(spirit) - asc_s) % 12 + 1,
                                "formula": "day: Asc + Sun - Moon" if day else "night: Asc + Moon - Sun"}},
            "houses": houses, "dispositor_chains": chains,
            "final_dispositor": sorted(finals) if finals else None,
            "terminal_loops": [list(l) for l in loops],
            "mutual_receptions_by_domicile": sorted({tuple(sorted((a, DOMICILE[sign_of(b[a]['lon'])])))
                                                     for a in TRADITIONAL
                                                     if DOMICILE[sign_of(b[a]['lon'])] != a and
                                                     DOMICILE[sign_of(b[DOMICILE[sign_of(b[a]['lon'])]]['lon'])] == a})}


def profections(asc_sign, birth_date, today, n_years=3):
    out = []
    age_now = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    for age in range(age_now, age_now + n_years):
        s = (asc_sign + age) % 12
        start = birth_date.replace(year=birth_date.year + age)
        end = birth_date.replace(year=birth_date.year + age + 1)
        out.append({"age": age, "start": start.isoformat(), "end": end.isoformat(),
                    "activated_house": age % 12 + 1, "profected_sign": SIGNS[s], "lord_of_year": DOMICILE[s]})
    return out


def solar_return(natal_sun, year, places):
    jd_guess = jd_from_utc(datetime(year, 5, 16, tzinfo=timezone.utc))
    jd = solar_longitude_crossing(natal_sun, jd_guess)
    utc = utc_from_jd(jd)
    out = {"utc": utc.isoformat(timespec="seconds"), "locations": {}}
    for name, (lat, lon) in places.items():
        a = angles(utc, lat, lon)
        out["locations"][name] = {"asc": a["asc"], "asc_sign": SIGNS[sign_of(a["asc"])],
                                  "mc": a["mc"], "mc_sign": SIGNS[sign_of(a["mc"])]}
    return out
