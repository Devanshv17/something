# Input audit

## Original input

> 23 JUN 2004,  Vashi navi mumbai maharastra, 1PM +-1hr, cureent:- blr. / female, riya

## Normalized

| Field | Value |
|---|---|
| gregorian_date | 2004-06-23 |
| local_time_24h | 13:05:00 |
| local_iso | 2004-06-23T13:05:00+05:30 |
| utc_iso | 2004-06-23T07:35:00+00:00 |
| weekday | Wednesday |
| latitude | 19.0632481 |
| longitude | 72.9987966 |
| elevation_m | 10 |
| coordinate_source | OpenStreetMap Nominatim, way 151768155 'Vashi' (Vashi station area; hospital not given, so a few km of positional uncertainty) |
| iana_zone | Asia/Kolkata |
| tzdata_release | 2026d |
| utc_offset | 5:30:00 |
| dst_in_effect | False |
| julian_day_ut | 2453179.815972222 |
| delta_t_seconds | 64.62460439728584 |
| local_mean_time | 2004-06-23T12:26:59 |
| equation_of_time_minutes | -2.2302447235060754 |
| local_apparent_solar_time | 2004-06-23T12:24:45 |
| historical_time_note | Post-1970 date; Asia/Kolkata has used a fixed +05:30 with no DST since 1945 per IANA. |
| sunrise | SE 2004-06-23T06:02:02+05:30 / JPL 2004-06-23T06:01:51+05:30 (Δ 11 s) |
| sunset | SE 2004-06-23T19:18:24+05:30 / JPL 2004-06-23T19:18:36+05:30 (Δ 12 s) |

Time uncertainty: ASSUMED time chosen by the user (13:05, 'or so'), not a recorded time; modelled as +/-5 min. The underlying record is only 1 PM +/- 1 hour.

## Boundary audit (every crossing inside ±5 min)

| Output | Value at 13:05 | ±5 min | ±5 min | Crossings (minutes from 13:05, from → to) |
|---|---|---|---|---|
| western_asc_sign | Libra | stable | stable | — |
| western_mc_sign | Cancer | stable | stable | — |
| jyotisha_lagna_sign | Virgo | stable | stable | — |
| jyotisha_lagna_d9 | Taurus | sensitive | sensitive | -3.6 min (13:01:24): Aries → Taurus |
| jyotisha_lagna_d10 | Virgo | sensitive | sensitive | +3.4 min (13:08:25): Virgo → Libra |
| jyotisha_lagna_nakshatra_pada | Hasta-2 | sensitive | sensitive | -3.6 min (13:01:24): Hasta-1 → Hasta-2 |
| moon_d9 | Gemini | stable | stable | — |
| moon_d10 | Libra | stable | stable | — |
| moon_nakshatra_pada | Magha-3 | stable | stable | — |
| planet_d9.Sun | Sagittarius | stable | stable | — |
| planet_d9.Mars | Leo | stable | stable | — |
| planet_d9.Mercury | Aquarius | stable | stable | — |
| planet_d9.Jupiter | Virgo | stable | stable | — |
| planet_d9.Venus | Taurus | stable | stable | — |
| planet_d9.Saturn | Aries | stable | stable | — |
| planet_d10.Sun | Leo | stable | stable | — |
| planet_d10.Mars | Aries | stable | stable | — |
| planet_d10.Mercury | Libra | stable | stable | — |
| planet_d10.Jupiter | Aquarius | stable | stable | — |
| planet_d10.Venus | Gemini | stable | stable | — |
| planet_d10.Saturn | Sagittarius | stable | stable | — |
| sect | day | stable | stable | — |
| bazi_hour_civil | 己未 | stable | stable | — |
| bazi_hour_LAT | 戊午 | stable | stable | — |
| ziwei_time_branch_civil | 未 | stable | stable | — |
| ziwei_time_branch_LAT | 午 | stable | stable | — |
| western_lot_fortune_sign | Sagittarius | stable | stable | — |

## Boundary distances

- **Western Ascendant** 08°06'27" Libra: 8.11° into its sign, 21.89° before the next (≈34.2 min since / ≈92.3 min to a cusp at 0.237°/min).
- **Jyotisha Lagna** 14°11'16" Virgo (Lahiri): 14.19° into its sign (≈59.8 min since / ≈66.7 min to a cusp). D9 segment 13.33–16.67°, D10 segment 12–15°.
- **Sect**: 423 min after sunrise, 373 min before sunset → day chart, stable.
- **BaZi / Zi Wei hour**: civil 13:05 is 5.0 min into the 未 double-hour (13:00-15:00), 115.0 min before its end; LAT 12:24 is 84.8 min into the 午 double-hour (11:00-13:00), 35.2 min before its end. Nearest boundary: 5.0 min (civil track, branch start).
- **Day boundary**: 785 min after midnight; late-Zi convention matters only for births between 23:00 and 24:00.
- **Solar terms**: birth 17.97 days after 芒种 and 13.46 days before 小暑 → month 庚午 stable.
- **Zi Wei lunar date**: 甲申年 五月初六 (leap month: False; year's leap month: 2); next new moon 2004-07-17T11:23:46+00:00 (579.8 h after birth).
- **Tibetan Losar**: birth month is after every possible Losar date (late Jan - late Mar).
- **Calendar adoption**: Gregorian civil date; no Julian/Gregorian ambiguity for 2004.
- **Planets within 1° of a sign cusp**: Mars 0.35° (tropical, ≈13 h of motion).
