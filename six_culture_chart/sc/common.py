"""Shared helpers: ephemeris setup, sign math, time conversion, boundary search."""
import json
import math
import os
import zoneinfo
from datetime import datetime, timedelta, timezone

import swisseph as swe

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EPHE = os.path.join(ROOT, "ephe")
# One chart per directory: BIRTH_INPUT.json (+ optional NARRATIVE.json) in CHART_DIR, results in CHART_DIR/output.
CHART_DIR = os.path.abspath(os.environ.get("SIX_CHART_DIR", ROOT))
OUT = os.path.join(CHART_DIR, "output")

# Force zoneinfo to use the pinned `tzdata` package, not the OS copy.
zoneinfo.reset_tzpath([])

swe.set_ephe_path(EPHE)

SIGNS = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra",
         "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]

PLANETS = {  # name -> swisseph id
    "Sun": swe.SUN, "Moon": swe.MOON, "Mercury": swe.MERCURY, "Venus": swe.VENUS,
    "Mars": swe.MARS, "Jupiter": swe.JUPITER, "Saturn": swe.SATURN,
    "Uranus": swe.URANUS, "Neptune": swe.NEPTUNE, "Pluto": swe.PLUTO,
}
TRADITIONAL = ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn"]

SWE_FLAGS = swe.FLG_SWIEPH | swe.FLG_SPEED


def norm(x):
    return x % 360.0


def sign_of(lon):
    return int(norm(lon) // 30)


def deg_in_sign(lon):
    return norm(lon) % 30.0


def dist_to_sign_boundary(lon):
    """Degrees to the nearest sign cusp (either side)."""
    d = deg_in_sign(lon)
    return min(d, 30.0 - d)


def angdiff(a, b):
    """Signed smallest difference a-b in (-180, 180]."""
    d = (a - b + 180.0) % 360.0 - 180.0
    return d


def fmt_dms(lon):
    d = deg_in_sign(lon)
    deg = int(d)
    m = (d - deg) * 60
    mi = int(m)
    s = int(round((m - mi) * 60))
    if s == 60:
        s, mi = 0, mi + 1
    if mi == 60:
        mi, deg = 0, deg + 1
    return f"{deg:02d}°{mi:02d}'{s:02d}\" {SIGNS[sign_of(lon)]}"


def jd_from_utc(dt_utc):
    h = dt_utc.hour + dt_utc.minute / 60 + dt_utc.second / 3600 + dt_utc.microsecond / 3.6e9
    return swe.julday(dt_utc.year, dt_utc.month, dt_utc.day, h, swe.GREG_CAL)


def utc_from_jd(jd):
    y, m, d, h = swe.revjul(jd, swe.GREG_CAL)
    base = datetime(y, m, d, tzinfo=timezone.utc)
    return base + timedelta(hours=h)


def iso(dt, tz=None):
    if tz is not None:
        dt = dt.astimezone(tz)
    return dt.isoformat(timespec="seconds")


def find_crossings(func, t0, t1, step_s=30, tol_s=1):
    """Return list of (utc_datetime, before_value, after_value) where func changes value in [t0, t1]."""
    out = []
    t = t0
    prev = func(t)
    while t < t1:
        tn = min(t + timedelta(seconds=step_s), t1)
        v = func(tn)
        if v != prev:
            a, b = t, tn
            while (b - a).total_seconds() > tol_s:
                mid = a + (b - a) / 2
                if func(mid) == prev:
                    a = mid
                else:
                    b = mid
            out.append((b, prev, v))
        t, prev = tn, v
    return out


def dump(name, obj):
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2, default=str)


def load_input():
    with open(os.path.join(CHART_DIR, "BIRTH_INPUT.json"), encoding="utf-8") as f:
        return json.load(f)


def load_narrative():
    p = os.path.join(CHART_DIR, "NARRATIVE.json")
    if not os.path.exists(p):
        return {}
    with open(p, encoding="utf-8") as f:
        return json.load(f)
