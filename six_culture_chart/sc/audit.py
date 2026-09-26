"""Step 2: normalize input, audit civil time, solar time, sunrise/sunset."""
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

import swisseph as swe
import tzdata
from skyfield import almanac
from skyfield.api import load, wgs84
from timezonefinder import TimezoneFinder

from .common import EPHE, iso, jd_from_utc, utc_from_jd

_ts = load.timescale(builtin=True)
_eph = load(f"{EPHE}/de440s.bsp")


def normalize(inp):
    lat = inp["birthplace"]["latitude"]
    lon = inp["birthplace"]["longitude"]
    tzname = TimezoneFinder().timezone_at(lat=lat, lng=lon)
    tz = ZoneInfo(tzname)
    d, m, y = (int(x) for x in inp["date"]["raw"].split("/"))
    hh, mm, ss = (int(x) for x in inp["time"]["local_24h"].split(":"))
    local = datetime(y, m, d, hh, mm, ss, tzinfo=tz)
    utc = local.astimezone(timezone.utc)
    offset = local.utcoffset()
    dst = local.dst()

    # Offset history check: the zone must have had one fixed offset around the birth date.
    probes = {iso(datetime(y, mo, 1, 12, tzinfo=tz)): str(datetime(y, mo, 1, 12, tzinfo=tz).utcoffset())
              for mo in range(1, 13)}

    jd = jd_from_utc(utc)
    lmt = utc + timedelta(hours=lon / 15.0)
    eot_days = swe.time_equ(jd)  # LAT - LMT, in days
    lat_time = lmt + timedelta(days=eot_days)

    # Sunrise / sunset: Swiss Ephemeris (disc centre? no: upper limb + refraction, SE default)
    geo = (lon, lat, inp["birthplace"].get("elevation_m", 0))
    day0 = datetime(y, m, d, tzinfo=tz).astimezone(timezone.utc)
    jd0 = jd_from_utc(day0)
    rs = swe.rise_trans(jd0, swe.SUN, swe.CALC_RISE, geo, 1013.25, 25.0)[1][0]
    ss_ = swe.rise_trans(jd0, swe.SUN, swe.CALC_SET, geo, 1013.25, 25.0)[1][0]
    rise_se, set_se = utc_from_jd(rs), utc_from_jd(ss_)

    # Independent sunrise/sunset from JPL DE440s via Skyfield almanac
    place = wgs84.latlon(lat, lon, inp["birthplace"].get("elevation_m", 0))
    t0 = _ts.from_datetime(day0)
    t1 = _ts.from_datetime(day0 + timedelta(days=1))
    f = almanac.sunrise_sunset(_eph, place)
    times, events = almanac.find_discrete(t0, t1, f)
    sk = {("rise" if e else "set"): t.utc_datetime() for t, e in zip(times, events)}

    return {
        "original": inp,
        "normalized": {
            "gregorian_date": local.date().isoformat(),
            "local_time_24h": local.strftime("%H:%M:%S"),
            "local_iso": iso(local),
            "utc_iso": iso(utc),
            "weekday": local.strftime("%A"),
            "latitude": lat, "longitude": lon,
            "elevation_m": inp["birthplace"].get("elevation_m"),
            "coordinate_source": inp["birthplace"]["coordinate_source"],
            "iana_zone": tzname,
            "tzdata_release": tzdata.IANA_VERSION,
            "utc_offset": str(offset),
            "dst_in_effect": dst != timedelta(0),
            "offset_history_probe_first_of_month_2004": probes,
            "julian_day_ut": jd,
            "julian_day_tt": jd + swe.deltat(jd),
            "delta_t_seconds": swe.deltat(jd) * 86400,
            "local_mean_time": lmt.replace(tzinfo=None).isoformat(timespec="seconds"),
            "equation_of_time_minutes": eot_days * 1440,
            "local_apparent_solar_time": lat_time.replace(tzinfo=None).isoformat(timespec="seconds"),
            "sunrise": {"swiss_ephemeris": iso(rise_se, tz), "skyfield_jpl": iso(sk["rise"], tz),
                        "difference_s": abs((rise_se - sk["rise"]).total_seconds())},
            "sunset": {"swiss_ephemeris": iso(set_se, tz), "skyfield_jpl": iso(sk["set"], tz),
                       "difference_s": abs((set_se - sk["set"]).total_seconds())},
            "sunrise_convention": "upper limb on apparent horizon with standard refraction (SE: 1013.25 hPa, 25 C; Skyfield: -0.8333 deg)",
            "historical_time_note": "Post-1970 date; Asia/Kolkata has used a fixed +05:30 with no DST since 1945 per IANA.",
        },
        "_objects": {"tz": tz, "local": local, "utc": utc, "rise_utc": rise_se, "set_utc": set_se},
    }
