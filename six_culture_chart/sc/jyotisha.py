"""Step 4B: Jyotisha (Parashari track: sidereal, Lahiri, whole-sign, mean node)."""
from datetime import timedelta

from .common import SIGNS, norm, sign_of, deg_in_sign

LORD = ["Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury", "Venus", "Mars",
        "Jupiter", "Saturn", "Saturn", "Jupiter"]
GRAHAS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]

EXALT = {"Sun": (0, 10), "Moon": (1, 3), "Mars": (9, 28), "Mercury": (5, 15),
         "Jupiter": (3, 5), "Venus": (11, 27), "Saturn": (6, 20)}
MOOLA = {"Sun": (4, 0, 20), "Moon": (1, 3, 30), "Mars": (0, 0, 12), "Mercury": (5, 15, 20),
         "Jupiter": (8, 0, 10), "Venus": (6, 0, 15), "Saturn": (10, 0, 20)}
# Naisargika (natural) relationships, BPHS.
FRIENDS = {
    "Sun": ({"Moon", "Mars", "Jupiter"}, {"Mercury"}, {"Venus", "Saturn"}),
    "Moon": ({"Sun", "Mercury"}, {"Mars", "Jupiter", "Venus", "Saturn"}, set()),
    "Mars": ({"Sun", "Moon", "Jupiter"}, {"Venus", "Saturn"}, {"Mercury"}),
    "Mercury": ({"Sun", "Venus"}, {"Mars", "Jupiter", "Saturn"}, {"Moon"}),
    "Jupiter": ({"Sun", "Moon", "Mars"}, {"Saturn"}, {"Mercury", "Venus"}),
    "Venus": ({"Mercury", "Saturn"}, {"Mars", "Jupiter"}, {"Sun", "Moon"}),
    "Saturn": ({"Mercury", "Venus"}, {"Jupiter"}, {"Sun", "Moon", "Mars"}),
}
COMBUST_ORB = {"Moon": 12, "Mars": 17, "Mercury": (14, 12), "Jupiter": 11, "Venus": (10, 8), "Saturn": 15}
SPECIAL_ASPECTS = {"Mars": [4, 7, 8], "Jupiter": [5, 7, 9], "Saturn": [3, 7, 10]}
NAKSHATRAS = ["Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu",
              "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta",
              "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha",
              "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada",
              "Uttara Bhadrapada", "Revati"]
DASHA_ORDER = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]
DASHA_YEARS = {"Ketu": 7, "Venus": 20, "Sun": 6, "Moon": 10, "Mars": 7, "Rahu": 18,
               "Jupiter": 16, "Saturn": 19, "Mercury": 17}
YEAR_DAYS = 365.25
NAK = 360 / 27


def nakshatra(lon):
    i = int(lon // NAK)
    return {"index": i + 1, "name": NAKSHATRAS[i], "pada": int((lon % NAK) // (NAK / 4)) + 1,
            "lord": DASHA_ORDER[i % 9], "fraction_elapsed": (lon % NAK) / NAK}


def d9(lon):
    s, p = sign_of(lon), int(deg_in_sign(lon) // (30 / 9))
    return (s * 9 + p) % 12


def d10(lon):
    s, p = sign_of(lon), int(deg_in_sign(lon) // 3)
    return (s + p) % 12 if s % 2 == 0 else (s + 8 + p) % 12


def dignity(planet, lon):
    if planet not in EXALT:
        return "n/a (node)"
    s, d = sign_of(lon), deg_in_sign(lon)
    if EXALT[planet][0] == s:
        return "exalted"
    if (EXALT[planet][0] + 6) % 12 == s:
        return "debilitated"
    ms, a, b = MOOLA[planet]
    if ms == s and a <= d < b:
        return "moolatrikona"
    lord = LORD[s]
    if lord == planet:
        return "own sign"
    fr, ne, en = FRIENDS[planet]
    return "friend's sign" if lord in fr else "neutral sign" if lord in ne else "enemy's sign"


def functional_nature(planet, lagna):
    """Declared simple Parashari rule set (rule id JY-FN-1)."""
    owned = [((s - lagna) % 12) + 1 for s in range(12) if LORD[s] == planet]
    if not owned:
        return {"houses_owned": [], "nature": "n/a"}
    tr = {1, 5, 9}
    bad = {3, 6, 11}
    if any(h in tr for h in owned) and not any(h in bad for h in owned):
        nat = "functional benefic"
    elif set(owned) & tr and set(owned) & bad:
        nat = "mixed"
    elif any(h in bad for h in owned):
        nat = "functional malefic"
    elif 8 in owned and planet not in ("Sun", "Moon"):
        nat = "functional malefic (8th lord)"
    else:
        nat = "neutral (kendra/2/12 lordship)"
    return {"houses_owned": owned, "nature": nat}


def chart(base, lagna_lon, node="MeanNode"):
    b = base["bodies"]
    lagna = sign_of(lagna_lon)
    sun = b["Sun"]["sidereal_lon"]
    rows = {}
    for g in GRAHAS:
        if g == "Rahu":
            lon, spd = b[node]["sidereal_lon"], b[node]["speed_deg_day"]
        elif g == "Ketu":
            lon, spd = norm(b[node]["sidereal_lon"] + 180), b[node]["speed_deg_day"]
        else:
            lon, spd = b[g]["sidereal_lon"], b[g]["speed_deg_day"]
        s = sign_of(lon)
        r = {"lon": lon, "sign": SIGNS[s], "deg": deg_in_sign(lon), "house": (s - lagna) % 12 + 1,
             "speed": spd, "retrograde": spd < 0 if g not in ("Rahu", "Ketu") else True,
             "nakshatra": nakshatra(lon), "dignity": dignity(g, lon),
             "d9": SIGNS[d9(lon)], "d10": SIGNS[d10(lon)]}
        if g in COMBUST_ORB:
            orb = COMBUST_ORB[g]
            if isinstance(orb, tuple):
                orb = orb[1] if r["retrograde"] else orb[0]
            sep = abs(((lon - sun + 180) % 360) - 180)
            r["distance_from_sun"] = sep
            r["combust"] = sep <= orb
            r["combust_orb_used"] = orb
        if g in LORD:
            r.update(functional_nature(g, lagna))
        rows[g] = r
    # Planetary war (graha yuddha): Mars..Saturn within 1 degree
    wars = []
    tp = ["Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    for i, x in enumerate(tp):
        for y in tp[i + 1:]:
            if abs(((rows[x]["lon"] - rows[y]["lon"] + 180) % 360) - 180) < 1:
                wars.append([x, y])
    # Graha drishti (sign-based, whole-sign)
    aspects = []
    for g in GRAHAS[:7]:
        for n in SPECIAL_ASPECTS.get(g, [7]):
            tgt = (sign_of(rows[g]["lon"]) + n - 1) % 12
            aspects.append({"from": g, "nth": n, "to_sign": SIGNS[tgt], "to_house": (tgt - lagna) % 12 + 1,
                            "occupants": [h for h in GRAHAS if sign_of(rows[h]["lon"]) == tgt]})
    lag = {"lon": lagna_lon, "sign": SIGNS[lagna], "deg": deg_in_sign(lagna_lon),
           "nakshatra": nakshatra(lagna_lon), "d9": SIGNS[d9(lagna_lon)], "d10": SIGNS[d10(lagna_lon)],
           "lord": LORD[lagna]}
    houses = {h: {"sign": SIGNS[(lagna + h - 1) % 12], "lord": LORD[(lagna + h - 1) % 12],
                  "occupants": [g for g in GRAHAS if rows[g]["house"] == h]} for h in range(1, 13)}
    return {"lagna": lag, "grahas": rows, "houses": houses, "planetary_war": wars, "graha_drishti": aspects,
            "yogas": yogas(rows, lagna)}


def yogas(rows, lagna):
    """Declared whitelist; each entry stores its exact rule."""
    out = []
    moon = sign_of(rows["Moon"]["lon"])
    jup = sign_of(rows["Jupiter"]["lon"])
    kendra_from_moon = (jup - moon) % 12 in (0, 3, 6, 9)
    out.append({"id": "JY-Y-GAJAKESARI", "rule": "Jupiter in a kendra (1/4/7/10) from the Moon",
                "satisfied": kendra_from_moon, "basis": f"Moon {SIGNS[moon]}, Jupiter {SIGNS[jup]}",
                "lagna_dependent": False})
    same = lambda a, b: sign_of(rows[a]["lon"]) == sign_of(rows[b]["lon"])
    out.append({"id": "JY-Y-BUDHADITYA", "rule": "Sun and Mercury in the same sign",
                "satisfied": same("Sun", "Mercury"), "lagna_dependent": False,
                "basis": f"Sun {rows['Sun']['sign']}, Mercury {rows['Mercury']['sign']}"})
    out.append({"id": "JY-Y-CHANDRA-MANGALA", "rule": "Moon and Mars in the same sign",
                "satisfied": same("Moon", "Mars"), "lagna_dependent": False,
                "basis": f"Moon {rows['Moon']['sign']}, Mars {rows['Mars']['sign']}"})
    others = [g for g in ["Mars", "Mercury", "Jupiter", "Venus", "Saturn"]]
    adj = [g for g in others if (sign_of(rows[g]["lon"]) - moon) % 12 in (1, 11)]
    with_moon = [g for g in others if sign_of(rows[g]["lon"]) == moon]
    kendra_moon = [g for g in others if (sign_of(rows[g]["lon"]) - moon) % 12 in (3, 6, 9)]
    out.append({"id": "JY-Y-KEMADRUMA", "rule": "No planet (excluding Sun, Rahu, Ketu) in 2nd or 12th from Moon",
                "satisfied": not adj, "basis": f"planets adjacent to Moon: {adj}", "lagna_dependent": False,
                "cancellation_rule": "cancelled if a planet (excl. Sun/nodes) occupies the Moon's sign or a kendra from the Moon",
                "cancelled": bool(with_moon or kendra_moon),
                "cancellation_basis": f"with Moon: {with_moon}; kendra from Moon: {kendra_moon}"})
    for g in others:
        s = sign_of(rows[g]["lon"])
        ok = rows[g]["dignity"] in ("exalted", "own sign", "moolatrikona") and (s - lagna) % 12 in (0, 3, 6, 9)
        out.append({"id": f"JY-Y-MAHAPURUSHA-{g.upper()}",
                    "rule": f"{g} in own/exaltation/moolatrikona sign AND in a kendra from lagna",
                    "satisfied": ok, "basis": f"{g} {rows[g]['sign']} ({rows[g]['dignity']}), house {rows[g]['house']}",
                    "lagna_dependent": True})
    # Neecha (debilitation) listing as fact, not yoga
    return out


def vimshottari(moon_sid_lon, birth_utc, levels=2):
    nk = nakshatra(moon_sid_lon)
    start_lord = nk["lord"]
    i0 = DASHA_ORDER.index(start_lord)
    elapsed_years = nk["fraction_elapsed"] * DASHA_YEARS[start_lord]
    cycle_start = birth_utc - timedelta(days=elapsed_years * YEAR_DAYS)
    periods = []
    t = cycle_start
    for k in range(9 * 2):
        md = DASHA_ORDER[(i0 + k) % 9]
        md_len = DASHA_YEARS[md]
        md_end = t + timedelta(days=md_len * YEAR_DAYS)
        subs = []
        st = t
        j0 = DASHA_ORDER.index(md)
        for j in range(9):
            ad = DASHA_ORDER[(j0 + j) % 9]
            ln = md_len * DASHA_YEARS[ad] / 120.0
            en = st + timedelta(days=ln * YEAR_DAYS)
            subs.append({"lord": ad, "start": st, "end": en})
            st = en
        periods.append({"lord": md, "start": t, "end": md_end, "antardashas": subs})
        t = md_end
        if t.year > birth_utc.year + 110:
            break
    return {"moon_nakshatra": nk, "balance_at_birth_years": DASHA_YEARS[start_lord] - elapsed_years,
            "year_length_days": YEAR_DAYS, "mahadashas": periods}
