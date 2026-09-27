# Input audit

## Original input

> ANjU, 29 june 1974, 6:15AM(around 5-10mins), roorkee, female, current:- kohima nagaland

## Normalized

| Field | Value |
|---|---|
| gregorian_date | 1974-06-29 |
| local_time_24h | 06:15:00 |
| local_iso | 1974-06-29T06:15:00+05:30 |
| utc_iso | 1974-06-29T00:45:00+00:00 |
| weekday | Saturday |
| latitude | 29.8693496 |
| longitude | 77.8902124 |
| elevation_m | 268 |
| coordinate_source | OpenStreetMap Nominatim, node 4373395280 'Roorkee' (city centre; hospital not given, so a few km of positional uncertainty) |
| iana_zone | Asia/Kolkata |
| tzdata_release | 2026d |
| utc_offset | 5:30:00 |
| dst_in_effect | False |
| julian_day_ut | 2442227.53125 |
| delta_t_seconds | 44.98232371722816 |
| local_mean_time | 1974-06-29T05:56:33 |
| equation_of_time_minutes | -3.2404819748276172 |
| local_apparent_solar_time | 1974-06-29T05:53:19 |
| historical_time_note | Post-1970 date; Asia/Kolkata has used a fixed +05:30 with no DST since 1945 per IANA. |
| sunrise | SE 1974-06-29T05:20:23+05:30 / JPL 1974-06-29T05:20:10+05:30 (Δ 13 s) |
| sunset | SE 1974-06-29T19:22:58+05:30 / JPL 1974-06-29T19:23:11+05:30 (Δ 13 s) |

Time uncertainty: approximate time, stated as within about 5-10 minutes; outer envelope +/-10 min is primary, +/-5 min is the inner scenario.

## Boundary audit (every crossing inside ±10 min)

| Output | Value at 06:15 | ±5 min | ±10 min | Crossings (minutes from 06:15, from → to) |
|---|---|---|---|---|
| western_asc_sign | Cancer | stable | stable | — |
| western_mc_sign | Aries | stable | stable | — |
| jyotisha_lagna_sign | Gemini | stable | stable | — |
| jyotisha_lagna_d9 | Taurus | stable | sensitive | -5.2 min (06:09:50): Aries → Taurus |
| jyotisha_lagna_d10 | Aquarius | sensitive | sensitive | -2.1 min (06:12:55): Capricorn → Aquarius |
| jyotisha_lagna_nakshatra_pada | Punarvasu-2 | stable | sensitive | -5.2 min (06:09:50): Punarvasu-1 → Punarvasu-2 |
| moon_d9 | Capricorn | stable | stable | — |
| moon_d10 | Capricorn | stable | stable | — |
| moon_nakshatra_pada | Swati-2 | stable | stable | — |
| planet_d9.Sun | Aquarius | stable | stable | — |
| planet_d9.Mars | Sagittarius | stable | stable | — |
| planet_d9.Mercury | Aquarius | stable | stable | — |
| planet_d9.Jupiter | Taurus | stable | stable | — |
| planet_d9.Venus | Aries | stable | stable | — |
| planet_d9.Saturn | Aquarius | stable | stable | — |
| planet_d10.Sun | Libra | stable | stable | — |
| planet_d10.Mars | Virgo | stable | stable | — |
| planet_d10.Mercury | Scorpio | stable | stable | — |
| planet_d10.Jupiter | Libra | stable | stable | — |
| planet_d10.Venus | Aries | stable | stable | — |
| planet_d10.Saturn | Libra | stable | stable | — |
| sect | day | stable | stable | — |
| bazi_hour_civil | 辛卯 | stable | stable | — |
| bazi_hour_LAT | 辛卯 | stable | stable | — |
| ziwei_time_branch_civil | 卯 | stable | stable | — |
| ziwei_time_branch_LAT | 卯 | stable | stable | — |
| western_lot_fortune_sign | Scorpio | stable | stable | — |

## Boundary distances

- **Western Ascendant** 17°56'59" Cancer: 17.95° into its sign, 12.05° before the next (≈83.2 min since / ≈55.9 min to a cusp at 0.216°/min).
- **Jyotisha Lagna** 24°26'56" Gemini (Lahiri): 24.45° into its sign (≈113.3 min since / ≈25.7 min to a cusp). D9 segment 23.33–26.67°, D10 segment 24–27°.
- **Sect**: 55 min after sunrise, 788 min before sunset → day chart, stable.
- **BaZi / Zi Wei hour**: civil 06:15 is 75.0 min into the 卯 double-hour (05:00-07:00), 45.0 min before its end; LAT 05:53 is 53.3 min into the 卯 double-hour (05:00-07:00), 66.7 min before its end. Nearest boundary: 45.0 min (civil track, branch end).
- **Day boundary**: 375 min after midnight; late-Zi convention matters only for births between 23:00 and 24:00.
- **Solar terms**: birth 22.95 days after 芒种 and 8.48 days before 小暑 → month 庚午 stable.
- **Zi Wei lunar date**: 甲寅年 五月初十 (leap month: False; year's leap month: 4); next new moon 1974-07-19T12:06:29+00:00 (491.4 h after birth).
- **Tibetan Losar**: birth month is after every possible Losar date (late Jan - late Mar).
- **Calendar adoption**: Gregorian civil date; no Julian/Gregorian ambiguity for 1974.
- **Planets within 1° of a sign cusp**: Uranus 0.16° (sidereal, ≈1481 h of motion).
