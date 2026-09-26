"""Step 4A: shared astronomical base (Swiss Ephemeris primary, JPL DE440s/Skyfield validator)."""
import math

import swisseph as swe
from skyfield.api import load
from skyfield.framelib import ecliptic_frame

from .common import (EPHE, PLANETS, SWE_FLAGS, angdiff, jd_from_utc, norm,
                     sign_of, deg_in_sign, dist_to_sign_boundary, SIGNS)

_ts = load.timescale(builtin=True)
_eph = load(f"{EPHE}/de440s.bsp")
_SK = {"Sun": "sun", "Moon": "moon", "Mercury": "mercury", "Venus": "venus",
       "Mars": "mars barycenter", "Jupiter": "jupiter barycenter", "Saturn": "saturn barycenter",
       "Uranus": "uranus barycenter", "Neptune": "neptune barycenter", "Pluto": "pluto barycenter"}

AYANAMSHA = swe.SIDM_LAHIRI


def tropical_positions(utc):
    jd = jd_from_utc(utc)
    out = {}
    for name, pid in PLANETS.items():
        (lon, lat, dist, slon, slat, sdist), _ = swe.calc_ut(jd, pid, SWE_FLAGS)
        out[name] = {"lon": lon, "lat": lat, "dist_au": dist, "speed_deg_day": slon,
                     "retrograde": slon < 0}
    for name, pid in (("MeanNode", swe.MEAN_NODE), ("TrueNode", swe.TRUE_NODE)):
        (lon, lat, dist, slon, *_), _ = swe.calc_ut(jd, pid, SWE_FLAGS)
        out[name] = {"lon": lon, "speed_deg_day": slon, "retrograde": slon < 0}
    return out


def ayanamsha(utc):
    swe.set_sid_mode(AYANAMSHA)
    return swe.get_ayanamsa_ut(jd_from_utc(utc))


def angles(utc, lat, lon, hsys=b"W"):
    jd = jd_from_utc(utc)
    cusps, ascmc = swe.houses_ex(jd, lat, lon, hsys)
    return {"asc": ascmc[0], "mc": ascmc[1], "armc": ascmc[2], "vertex": ascmc[3], "cusps": list(cusps)}


def skyfield_positions(utc):
    t = _ts.from_datetime(utc)
    earth = _eph["earth"]
    out = {}
    for name, key in _SK.items():
        app = earth.at(t).observe(_eph[key]).apparent()
        lat, lon, dist = app.frame_latlon(ecliptic_frame)
        out[name] = {"lon": lon.degrees % 360.0, "lat": lat.degrees}
    return out


def skyfield_angles(utc, lat, lon):
    """Independent Ascendant/MC from Skyfield GAST and true obliquity (textbook formulas)."""
    t = _ts.from_datetime(utc)
    from skyfield.nutationlib import iau2000a_radians, mean_obliquity
    dpsi, deps = iau2000a_radians(t)
    true_ob = mean_obliquity(t.tdb) / 3600.0 + math.degrees(deps)
    eps = math.radians(true_ob)
    ramc = math.radians((t.gast * 15.0 + lon) % 360.0)
    phi = math.radians(lat)
    mc = math.degrees(math.atan2(math.sin(ramc), math.cos(ramc) * math.cos(eps))) % 360
    asc = math.degrees(math.atan2(math.cos(ramc),
                                  -(math.sin(ramc) * math.cos(eps) + math.tan(phi) * math.sin(eps)))) % 360
    return {"asc": asc, "mc": mc, "true_obliquity": true_ob}


def meeus_mean_node(utc):
    jd = jd_from_utc(utc)
    T = (jd + swe.deltat(jd) - 2451545.0) / 36525.0
    return norm(125.04452 - 1934.136261 * T + 0.0020708 * T * T + T ** 3 / 450000.0)


def solar_longitude_crossing(target, jd_guess):
    """Exact UT instant the apparent tropical Sun reaches `target` degrees (Swiss Ephemeris)."""
    jd = jd_guess
    for _ in range(50):
        lon, _ = swe.calc_ut(jd, swe.SUN, SWE_FLAGS)[0][0], None
        speed = swe.calc_ut(jd, swe.SUN, SWE_FLAGS)[0][3]
        d = angdiff(target, lon)
        jd += d / speed
        if abs(d) < 1e-9:
            break
    return jd


def skyfield_solar_longitude_crossing(target, utc_guess):
    from skyfield.searchlib import find_discrete
    from datetime import timedelta

    def f(t):
        e = _eph["earth"].at(t).observe(_eph["sun"]).apparent()
        lon = e.frame_latlon(ecliptic_frame)[1].degrees
        return ((lon - target + 180.0) % 360.0) > 180.0
    f.step_days = 0.5
    t0 = _ts.from_datetime(utc_guess - timedelta(days=3))
    t1 = _ts.from_datetime(utc_guess + timedelta(days=3))
    times, vals = find_discrete(t0, t1, f)
    for t, v in zip(times, vals):
        if not v:
            return t.utc_datetime()
    return times[0].utc_datetime() if len(times) else None


def base(utc, lat, lon):
    trop = tropical_positions(utc)
    ay = ayanamsha(utc)
    sk = skyfield_positions(utc)
    ang = angles(utc, lat, lon)
    sk_ang = skyfield_angles(utc, lat, lon)
    rows = {}
    for name, p in trop.items():
        r = dict(p)
        r["sidereal_lon"] = norm(p["lon"] - ay)
        r["tropical_sign"] = SIGNS[sign_of(p["lon"])]
        r["sidereal_sign"] = SIGNS[sign_of(r["sidereal_lon"])]
        r["tropical_deg_in_sign"] = deg_in_sign(p["lon"])
        r["sidereal_deg_in_sign"] = deg_in_sign(r["sidereal_lon"])
        r["tropical_boundary_distance_deg"] = dist_to_sign_boundary(p["lon"])
        r["sidereal_boundary_distance_deg"] = dist_to_sign_boundary(r["sidereal_lon"])
        if name in sk:
            r["skyfield_lon"] = sk[name]["lon"]
            r["validator_difference_deg"] = abs(angdiff(p["lon"], sk[name]["lon"]))
        rows[name] = r
    rows["MeanNode"]["meeus_lon"] = meeus_mean_node(utc)
    rows["MeanNode"]["validator_difference_deg"] = abs(angdiff(rows["MeanNode"]["lon"], rows["MeanNode"]["meeus_lon"]))
    for nk in ("MeanNode", "TrueNode"):
        k = norm(rows[nk]["lon"] + 180)
        rows[nk.replace("Node", "Ketu")] = {"lon": k, "sidereal_lon": norm(k - ay),
                                           "sidereal_sign": SIGNS[sign_of(norm(k - ay))]}
    return {
        "utc": utc.isoformat(),
        "ayanamsha_lahiri_deg": ay,
        "bodies": rows,
        "angles_tropical": {"asc": ang["asc"], "mc": ang["mc"], "armc": ang["armc"]},
        "angles_sidereal": {"asc": norm(ang["asc"] - ay), "mc": norm(ang["mc"] - ay)},
        "angles_validator": sk_ang,
        "angle_differences_deg": {"asc": abs(angdiff(ang["asc"], sk_ang["asc"])),
                                  "mc": abs(angdiff(ang["mc"], sk_ang["mc"]))},
    }
