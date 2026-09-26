# Input audit

## Original input

> 17/05/2004, 9:30 AM, 15-30mins ig, Lucknow India, Male, Almora Uttrakhand(only from last 1.5minht a of so but planning to go around and visit the country)

## Normalized

| Field | Value |
|---|---|
| gregorian_date | 2004-05-17 |
| local_time_24h | 09:30:00 |
| local_iso | 2004-05-17T09:30:00+05:30 |
| utc_iso | 2004-05-17T04:00:00+00:00 |
| weekday | Monday |
| latitude | 26.8467 |
| longitude | 80.9462 |
| elevation_m | 123 |
| coordinate_source | city-centre coordinates (GeoNames/Wikipedia consensus for Lucknow); hospital/district not provided, so up to ~10 km positional uncertainty |
| iana_zone | Asia/Kolkata |
| tzdata_release | 2026d |
| utc_offset | 5:30:00 |
| dst_in_effect | False |
| julian_day_ut | 2453142.6666666665 |
| delta_t_seconds | 64.61333124981 |
| local_mean_time | 2004-05-17T09:23:47 |
| equation_of_time_minutes | 3.63461696298873 |
| local_apparent_solar_time | 2004-05-17T09:27:25 |
| historical_time_note | Post-1970 date; Asia/Kolkata has used a fixed +05:30 with no DST since 1945 per IANA. |
| sunrise | SE 2004-05-17T05:17:47+05:30 / JPL 2004-05-17T05:17:35+05:30 (Δ 11 s) |
| sunset | SE 2004-05-17T18:47:40+05:30 / JPL 2004-05-17T18:47:52+05:30 (Δ 12 s) |

Time uncertainty: user-estimated uncertainty of 15 to 30 minutes either side; outer envelope +/-30 min used as primary, +/-15 min reported as inner scenario.

## Boundary audit (every crossing inside ±30 min)

| Output | Value at 09:30 | ±15 min | ±30 min | Crossings (minutes from 09:30, from → to) |
|---|---|---|---|---|
| western_asc_sign | Cancer | stable | sensitive | +21.3 min (09:51:17): Cancer → Leo |
| western_mc_sign | Aries | stable | stable | — |
| jyotisha_lagna_sign | Cancer | sensitive | sensitive | -6.9 min (09:23:04): Gemini → Cancer |
| jyotisha_lagna_d9 | Cancer | sensitive | sensitive | -22.3 min (09:07:41): Taurus → Gemini; -6.9 min (09:23:04): Gemini → Cancer; +8.5 min (09:38:31): Cancer → Leo; +24.0 min (09:54:00): Leo → Virgo |
| jyotisha_lagna_d10 | Pisces | sensitive | sensitive | -20.8 min (09:09:13): Aquarius → Pisces; +7.0 min (09:36:59): Pisces → Aries; +20.9 min (09:50:55): Aries → Taurus |
| jyotisha_lagna_nakshatra_pada | Punarvasu-4 | sensitive | sensitive | -22.3 min (09:07:41): Punarvasu-2 → Punarvasu-3; -6.9 min (09:23:04): Punarvasu-3 → Punarvasu-4; +8.5 min (09:38:31): Punarvasu-4 → Pushya-1; +24.0 min (09:54:00): Pushya-1 → Pushya-2 |
| moon_d9 | Cancer | stable | sensitive | -19.6 min (09:10:27): Gemini → Cancer |
| moon_d10 | Cancer | stable | stable | — |
| moon_nakshatra_pada | Ashwini-4 | stable | sensitive | -19.6 min (09:10:27): Ashwini-3 → Ashwini-4 |
| planet_d9.Sun | Capricorn | stable | stable | — |
| planet_d9.Mars | Capricorn | stable | stable | — |
| planet_d9.Mercury | Gemini | stable | stable | — |
| planet_d9.Jupiter | Leo | stable | stable | — |
| planet_d9.Venus | Libra | stable | stable | — |
| planet_d9.Saturn | Aquarius | stable | stable | — |
| planet_d10.Sun | Capricorn | stable | stable | — |
| planet_d10.Mars | Libra | stable | stable | — |
| planet_d10.Mercury | Gemini | stable | stable | — |
| planet_d10.Jupiter | Capricorn | stable | stable | — |
| planet_d10.Venus | Gemini | stable | stable | — |
| planet_d10.Saturn | Scorpio | stable | stable | — |
| sect | day | stable | stable | — |
| bazi_hour_civil | 癸巳 | stable | stable | — |
| bazi_hour_LAT | 癸巳 | stable | sensitive | -27.4 min (09:02:35): 壬辰 → 癸巳 |
| ziwei_time_branch_civil | 巳 | stable | stable | — |
| ziwei_time_branch_LAT | 巳 | stable | sensitive | -27.4 min (09:02:35): 辰 → 巳 |
| western_lot_fortune_sign | Cancer | sensitive | sensitive | -13.0 min (09:17:00): Gemini → Cancer |

## Boundary distances

- **Western Ascendant** 25°24'47" Cancer: 4.59° before Leo (≈21.3 min at 0.216°/min).
- **Jyotisha Lagna** 01°29'41" Cancer (Lahiri): only 1.49° past the Gemini/Cancer cusp (≈6.9 min). Its D9 segment is 0.00–3.33° and D10 segment 0–3°.
- **Sect**: 252 min after sunrise, 558 min before sunset → day chart, stable.
- **BaZi / Zi Wei hour**: civil 09:30 is 30 min into the 巳 Si double-hour (09:00–11:00). Local apparent solar time 09:27:25 is 27.4 min into it. Under the solar-time track the hour becomes 辰 Chen if birth was ≥27.4 min earlier than 09:30.
- **Day boundary**: 570 min after midnight; late-Zi convention irrelevant.
- **Solar terms**: birth 12.00 days after 立夏 and 19.18 days before 芒种 → month 己巳 stable.
- **Zi Wei lunar date**: 甲申年 三月廿九 (3rd lunar month, day 29; not a leap month; 2004's leap month was 闰二月); next new moon 2004-05-19T04:51:55+00:00 (48.9 h after birth), so lunar month stable.
- **Tibetan Losar**: birth in May is after every possible Losar date (late Jan - late Mar).
- **Calendar adoption**: Gregorian civil date; no Julian/Gregorian ambiguity for 2004.
- **Mercury** is 0.93° into tropical Taurus (ingress ≈21 h before birth) — stable over ±30 min.
