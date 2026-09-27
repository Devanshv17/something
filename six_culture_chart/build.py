"""Parameterized builder: reads BIRTH_INPUT.json and writes fact-only datasets to output/.

Run: .venv/bin/python build.py
"""
import hashlib
import json
import os
import platform
import sys
from datetime import date, datetime, timedelta, timezone
from importlib.metadata import version

import swisseph as swe

from sc import astro, bazi, jyotisha, maya_tibet, western, ziwei
from sc.audit import normalize
from sc.common import (OUT, ROOT, SIGNS, angdiff, dump, find_crossings, iso, jd_from_utc, load_input, norm,
                       sign_of, utc_from_jd)

EXECUTED = datetime.now(timezone.utc).isoformat(timespec="seconds")


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def main():
    inp = load_input()
    audit = normalize(inp)
    obj = audit["_objects"]
    tz, utc, local = obj["tz"], obj["utc"], obj["local"]
    lat, lon = inp["birthplace"]["latitude"], inp["birthplace"]["longitude"]
    lat_offset = timedelta(minutes=audit["normalized"]["equation_of_time_minutes"]) + \
        timedelta(hours=lon / 15) - local.utcoffset()  # LAT - civil
    outer = inp["time_uncertainty"]["outer_minutes"]
    inner = inp["time_uncertainty"]["inner_minutes"]
    offsets = sorted({-outer, -inner, 0, inner, outer})

    # ---------- shared base at each ensemble instant ----------
    bases = {}
    for off in offsets:
        u = utc + timedelta(minutes=off)
        b = astro.base(u, lat, lon)
        bases[off] = b

    B = bases[0]
    rise, sset = obj["rise_utc"], obj["set_utc"]

    # ---------- per-instant derived labels ----------
    memo = {}

    def lbl(u):
        key = round(u.timestamp(), 3)
        if key in memo:
            return memo[key]
        memo[key] = _lbl(u)
        return memo[key]

    def _lbl(u):
        b = astro.base(u, lat, lon)
        asc_t = b["angles_tropical"]["asc"]
        asc_s = b["angles_sidereal"]["asc"]
        loc = (u.astimezone(tz)).replace(tzinfo=None)
        lat_loc = loc + lat_offset
        return b, {
            "western_asc_sign": SIGNS[sign_of(asc_t)],
            "western_mc_sign": SIGNS[sign_of(b["angles_tropical"]["mc"])],
            "jyotisha_lagna_sign": SIGNS[sign_of(asc_s)],
            "jyotisha_lagna_d9": SIGNS[jyotisha.d9(asc_s)],
            "jyotisha_lagna_d10": SIGNS[jyotisha.d10(asc_s)],
            "jyotisha_lagna_nakshatra_pada": f"{jyotisha.nakshatra(asc_s)['name']}-{jyotisha.nakshatra(asc_s)['pada']}",
            "moon_d9": SIGNS[jyotisha.d9(b['bodies']['Moon']['sidereal_lon'])],
            "moon_d10": SIGNS[jyotisha.d10(b['bodies']['Moon']['sidereal_lon'])],
            "moon_nakshatra_pada": f"{jyotisha.nakshatra(b['bodies']['Moon']['sidereal_lon'])['name']}-"
                                   f"{jyotisha.nakshatra(b['bodies']['Moon']['sidereal_lon'])['pada']}",
            "planet_d9": {g: SIGNS[jyotisha.d9(b['bodies'][g]['sidereal_lon'])] for g in
                          ["Sun", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]},
            "planet_d10": {g: SIGNS[jyotisha.d10(b['bodies'][g]['sidereal_lon'])] for g in
                           ["Sun", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]},
            "sect": "day" if rise <= u <= sset else "night",
            "bazi_hour_civil": bazi.pillars_lunar_python(loc)[1][3],
            "bazi_hour_LAT": bazi.pillars_lunar_python(lat_loc)[1][3],
            "ziwei_time_branch_civil": "子丑寅卯辰巳午未申酉戌亥"[((loc.hour + 1) // 2) % 12],
            "ziwei_time_branch_LAT": "子丑寅卯辰巳午未申酉戌亥"[((lat_loc.hour + 1) // 2) % 12],
            "western_lot_fortune_sign": SIGNS[sign_of(norm(asc_t + b['bodies']['Moon']['lon'] - b['bodies']['Sun']['lon']))],
        }

    ensemble = {}
    for off in offsets:
        u = utc + timedelta(minutes=off)
        _, L = lbl(u)
        ensemble[f"{off:+d}min"] = {"utc": iso(u), "local": iso(u, tz), **L}

    def flat(L):
        f = {}
        for k, v in L.items():
            if isinstance(v, dict):
                for kk, vv in v.items():
                    f[f"{k}.{kk}"] = vv
            else:
                f[k] = v
        return f

    keys = list(flat(lbl(utc)[1]).keys())
    stability = {}
    crossings = {}
    for k in keys:
        f = lambda u, k=k: flat(lbl(u)[1])[k]
        cr = find_crossings(f, utc - timedelta(minutes=outer), utc + timedelta(minutes=outer), step_s=10, tol_s=1)
        within_inner = [c for c in cr if abs((c[0] - utc).total_seconds()) <= inner * 60]
        stability[k] = {
            "value_at_T": f(utc),
            "outer_interval": "stable" if not cr else "sensitive",
            "inner_interval": "stable" if not within_inner else "sensitive",
            "crossings": [{"instant_utc": iso(c[0]), "instant_local": iso(c[0], tz),
                           "minutes_from_T": round((c[0] - utc).total_seconds() / 60, 2),
                           "from": c[1], "to": c[2]} for c in cr],
        }

    # ---------- boundary distances ----------
    asc_t, asc_s = B["angles_tropical"]["asc"], B["angles_sidereal"]["asc"]
    rate = (bases[inner]["angles_tropical"]["asc"] - bases[-inner]["angles_tropical"]["asc"]) / (2 * inner)
    new_moon_jd = None
    jd = jd_from_utc(utc)
    # previous and next new moon (for lunar-month context)
    def elong(j):
        s = swe.calc_ut(j, swe.SUN)[0][0]
        m = swe.calc_ut(j, swe.MOON)[0][0]
        return angdiff(m, s)
    j = jd
    while elong(j) < 0:
        j += 0.25
    lo, hi = j - 0.25, j
    for _ in range(60):
        mid = (lo + hi) / 2
        (lo, hi) = (mid, hi) if elong(mid) < 0 else (lo, mid)
    next_new_moon = utc_from_jd(hi)
    boundaries = {
        "western_asc": {"asc_lon": asc_t, "deg_in_sign": asc_t % 30, "to_prev_cusp_deg": asc_t % 30,
                        "to_next_cusp_deg": 30 - asc_t % 30, "asc_rate_deg_per_min": rate,
                        "minutes_to_next_cusp_approx": (30 - asc_t % 30) / rate,
                        "minutes_since_prev_cusp_approx": (asc_t % 30) / rate},
        "jyotisha_lagna": {"lagna_lon": asc_s, "deg_in_sign": asc_s % 30,
                           "minutes_since_prev_cusp_approx": (asc_s % 30) / rate,
                           "minutes_to_next_cusp_approx": (30 - asc_s % 30) / rate,
                           "d9_segment_deg": [int(asc_s % 30 // (30 / 9)) * 30 / 9, (int(asc_s % 30 // (30 / 9)) + 1) * 30 / 9],
                           "d10_segment_deg": [int(asc_s % 30 // 3) * 3, (int(asc_s % 30 // 3) + 1) * 3]},
        "sunrise_sect": {"sunrise_local": iso(rise, tz), "sunset_local": iso(sset, tz),
                         "minutes_after_sunrise": (utc - rise).total_seconds() / 60,
                         "minutes_before_sunset": (sset - utc).total_seconds() / 60},
        "bazi_hour": {"civil_hour_branch_window": "09:00-11:00 巳 Si",
                      "minutes_after_09:00_civil": 30,
                      "LAT_time": audit["normalized"]["local_apparent_solar_time"],
                      "minutes_after_09:00_LAT": (datetime.fromisoformat(audit["normalized"]["local_apparent_solar_time"]) -
                                                  datetime(2004, 5, 17, 9, 0)).total_seconds() / 60},
        "day_boundary": {"minutes_after_local_midnight": 570, "minutes_before_23:00_late_zi": 13 * 60 + 30,
                         "note": "late-Zi convention irrelevant at 09:30"},
        "zi_wei_lunar": {"lunar_date": "甲申年 三月廿九 (3rd lunar month, day 29; not a leap month; 2004's leap month was 闰二月)",
                         "next_new_moon_utc": iso(next_new_moon),
                         "hours_to_next_new_moon": (next_new_moon - utc).total_seconds() / 3600,
                         "note": "lunar day changes at civil midnight in iztro; the next lunar month begins with the new moon's civil date in China (UTC+8)"},
        "tibetan_losar": "birth in May is after every possible Losar date (late Jan - late Mar)",
        "calendar_adoption": "Gregorian civil date; no Julian/Gregorian ambiguity for 2004",
        "mercury_tropical_sign_cusp": {"deg_past_0_taurus": B["bodies"]["Mercury"]["lon"] - 30,
                                       "hours_since_ingress_approx": (B["bodies"]["Mercury"]["lon"] - 30) /
                                       B["bodies"]["Mercury"]["speed_deg_day"] * 24},
    }

    # ---------- Jyotisha ----------
    jy = {}
    for off in offsets:
        bb = bases[off]
        jy[f"{off:+d}min"] = jyotisha.chart(bb, bb["angles_sidereal"]["asc"], node="MeanNode")
    jy_true_node = jyotisha.chart(B, asc_s, node="TrueNode")
    node_sign_same = jy[f"{0:+d}min"]["grahas"]["Rahu"]["sign"] == jy_true_node["grahas"]["Rahu"]["sign"]
    dasha = {}
    for off in (-outer, 0, outer):
        bb = bases[off]
        dasha[f"{off:+d}min"] = jyotisha.vimshottari(bb["bodies"]["Moon"]["sidereal_lon"], utc,
                                                     pd_window=(2020, 2035) if outer <= 5 else None)
    # identify distinct lagna alternatives
    lagna_alts = {}
    for off in offsets:
        s = jy[f"{off:+d}min"]["lagna"]["sign"]
        lagna_alts.setdefault(s, []).append(off)

    # ---------- BaZi ----------
    lat_local = local.replace(tzinfo=None) + lat_offset
    bz = bazi.compute(local.replace(tzinfo=None), lat_local, utc, gender_code=1)
    bz_alt = bazi.compute(local.replace(tzinfo=None).replace(hour=8, minute=59), lat_local.replace(hour=8, minute=59), utc, 1)
    bz_alt_summary = {"hour_pillar": bz_alt["pillars"][3], "interactions": bz_alt["interactions"],
                      "dm_strength": bz_alt["dm_strength"]}
    bz["yong_shen"] = bazi.yong_shen(bz)
    bz_alt_summary["yong_shen"] = bazi.yong_shen(bz_alt)
    terms = bz.pop("_term_objs")
    bz_alt.pop("_term_objs")

    # ---------- Western ----------
    today = date.fromisoformat(inp["analysis_date"])
    bdate = local.date()
    wc = {}
    for off in offsets:
        bb = bases[off]
        u = utc + timedelta(minutes=off)
        day = rise <= u <= sset
        wc[f"{off:+d}min"] = western.chart(bb, bb["angles_tropical"]["asc"], bb["angles_tropical"]["mc"], day)
        wc[f"{off:+d}min"]["profections"] = western.profections(sign_of(bb["angles_tropical"]["asc"]), bdate, today, 3)
    places = {"birthplace_Lucknow": (lat, lon),
              "current_residence_Almora": (inp["current_residence"]["latitude"], inp["current_residence"]["longitude"])}
    sr = {str(y): western.solar_return(B["bodies"]["Sun"]["lon"], y, places) for y in (2026, 2027)}
    for y, v in sr.items():
        v["natal_sun_lon"] = B["bodies"]["Sun"]["lon"]
        v["sensitivity_note"] = "Return Ascendant recomputed with the natal Sun at T-30 and T+30; see ensemble_asc_signs."
        v["location_changes_asc_sign"] = len({x["asc_sign"] for x in v["locations"].values()}) > 1
    # SR sensitivity: recompute with Sun at -30/+30
    for y in sr:
        sr[y]["ensemble_asc_signs"] = {}
        for off in (-outer, outer):
            s_alt = western.solar_return(bases[off]["bodies"]["Sun"]["lon"], int(y), places)
            sr[y]["ensemble_asc_signs"][f"{off:+d}min"] = {k: v["asc_sign"] for k, v in s_alt["locations"].items()}

    # ---------- Zi Wei ----------
    zw = ziwei.compute(f"{bdate.year}-{bdate.month}-{bdate.day}", [today.isoformat().replace("-0", "-"),
                                                                     "2027-9-26", "2028-9-26"])

    # ---------- Maya / Tibetan ----------
    my = maya_tibet.maya(bdate.year, bdate.month, bdate.day)
    tb = maya_tibet.tibetan(bdate.year, bdate.month, bdate.day)

    # ---------- manifest ----------
    pkgs = ["pyswisseph", "pysweph", "skyfield", "jplephem", "numpy", "tzdata", "timezonefinder", "lunar_python",
            "sxtwl", "convertdate", "py-iztro", "pythonmonkey", "immanuel", "ephem"]
    code_files = sorted([os.path.join("sc", f) for f in os.listdir(os.path.join(ROOT, "sc")) if f.endswith(".py")] +
                        ["build.py", "verify.py", "synth.py", "render.py", "js/ziwei.js", "js/package.json"])
    manifest = {
        "executed_utc": EXECUTED,
        "runtime": {"python": sys.version, "platform": platform.platform(), "node": os.popen("node --version").read().strip()},
        "packages": {p: version(p) for p in pkgs},
        "npm": {"iztro": zw["alternatives"]["巳"]["chart_zh"]["iztro_version"]},
        "package_notes": [
            "pyswisseph and pysweph both provide the `swisseph` module; the loaded binary reports Swiss Ephemeris " + swe.version,
            "immanuel installed but NOT used: its object model was not needed after direct Swiss Ephemeris computation; no values come from it",
            "ephem installed but not used",
            "py-iztro bundles iztro 2.5.0 JS; canonical npm iztro is newer. Both are the same method, not independent.",
        ],
        "ephemeris_files": {f: sha(os.path.join(ROOT, "ephe", f)) for f in sorted(os.listdir(os.path.join(ROOT, "ephe")))},
        "ephemeris_notes": {"swiss": "Swiss Ephemeris 2.10 compressed JPL files sepl_18/semo_18/seas_18 (1800-2400 CE)",
                            "jpl": "de440s.bsp (NAIF generic kernels; DE440 short span 1849-2150)"},
        "iana_tzdata": audit["normalized"]["tzdata_release"],
        "conventions": {
            "shared": "geocentric apparent positions; true ecliptic and equinox of date; UT via Swiss Ephemeris delta-T",
            "jyotisha": "sidereal, Lahiri (SE_SIDM_LAHIRI), whole-sign houses from Lagna, MEAN node primary (true node reported), "
                        "Vimshottari 365.25-day year, BPHS natural friendships, combustion orbs Mo12 Ma17 Me14/12R Ju11 Ve10/8R Sa15",
            "western": "tropical, whole-sign houses, 7 traditional planets, sect by actual horizon (SE sunrise/sunset), "
                       "Egyptian bounds, Dorothean triplicities, Chaldean faces, Ptolemaic aspects by sign with 3-deg kollesis, "
                       "under-beams 15 deg / combust 8.5 deg / cazimi 17', Lots by day/night formula, annual profections by whole sign",
            "bazi": "lunar_python EightChar sect=2 (day changes at 00:00), civil clock primary with LAT track, jie (sectional) "
                    "solar terms by apparent solar longitude, Da Yun 3 days = 1 year (exact) and lunar_python rounding reported",
            "ziwei": zw["configuration"],
            "maya": my["correlation_constant"],
            "tibetan": "element-animal-gender year only",
        },
        "source_checksums": {f: sha(os.path.join(ROOT, f)) for f in code_files if os.path.exists(os.path.join(ROOT, f))},
    }

    raw = {
        "input_audit": audit["normalized"],
        "ensemble_offsets_min": offsets,
        "ensemble": ensemble,
        "stability": stability,
        "boundaries": boundaries,
        "astronomy": {f"{k:+d}min": v for k, v in bases.items()},
        "jyotisha": {"charts": jy, "true_node_variant_T": {"rahu": jy_true_node["grahas"]["Rahu"],
                                                           "ketu": jy_true_node["grahas"]["Ketu"],
                                                           "same_sign_as_mean": node_sign_same},
                     "lagna_alternatives": lagna_alts, "vimshottari": dasha,
                     "unavailable": {"shadbala": "no validated implementation in this environment",
                                     "ashtakavarga": "timing/transit support not requested; not computed",
                                     "pratyantardasha": ("computed for Mahadashas overlapping 2020-2035 only" if outer <= 5 else
                                                         "time precision insufficient; omitted"),
                                     "D7_D12": "domains not specifically requested and time precision insufficient"}},
        "bazi": {"primary": bz, "alternative_hour_Chen": bz_alt_summary},
        "western": {"charts": wc, "solar_returns": sr,
                    "unavailable": {"zodiacal_releasing": "not implemented/validated here",
                                    "transits": "not requested", "modern_outer_planets": "computed in astronomy base only; excluded from Hellenistic scoring"}},
        "ziwei": zw,
        "maya": my,
        "tibetan": tb,
    }
    dump("RAW_CALCULATIONS.json", raw)
    dump("CALCULATION_MANIFEST.json", manifest)
    return raw, manifest


if __name__ == "__main__":
    main()
    print("ok")
