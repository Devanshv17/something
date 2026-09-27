# Input audit

## Original input

> 23 JUN 2004,  Vashi navi mumbai maharastra, 1PM +-1hr, cureent:- blr. / female, riya

## Normalized

| Field | Value |
|---|---|
| gregorian_date | 2004-06-23 |
| local_time_24h | 13:00:00 |
| local_iso | 2004-06-23T13:00:00+05:30 |
| utc_iso | 2004-06-23T07:30:00+00:00 |
| weekday | Wednesday |
| latitude | 19.0632481 |
| longitude | 72.9987966 |
| elevation_m | 10 |
| coordinate_source | OpenStreetMap Nominatim, way 151768155 'Vashi' (Vashi station area; hospital not given, so a few km of positional uncertainty) |
| iana_zone | Asia/Kolkata |
| tzdata_release | 2026d |
| utc_offset | 5:30:00 |
| dst_in_effect | False |
| julian_day_ut | 2453179.8125 |
| delta_t_seconds | 64.62460333120346 |
| local_mean_time | 2004-06-23T12:21:59 |
| equation_of_time_minutes | -2.229494904684543 |
| local_apparent_solar_time | 2004-06-23T12:19:45 |
| historical_time_note | Post-1970 date; Asia/Kolkata has used a fixed +05:30 with no DST since 1945 per IANA. |
| sunrise | SE 2004-06-23T06:02:02+05:30 / JPL 2004-06-23T06:01:51+05:30 (Δ 11 s) |
| sunset | SE 2004-06-23T19:18:24+05:30 / JPL 2004-06-23T19:18:36+05:30 (Δ 12 s) |

Time uncertainty: approximate time, stated as plus or minus one hour; outer envelope +/-60 min is primary, +/-30 min is the inner scenario.

## Boundary audit (every crossing inside ±60 min)

| Output | Value at 13:00 | ±30 min | ±60 min | Crossings (minutes from 13:00, from → to) |
|---|---|---|---|---|
| western_asc_sign | Libra | sensitive | sensitive | -29.1 min (12:30:51): Virgo → Libra |
| western_mc_sign | Cancer | sensitive | sensitive | -29.1 min (12:30:51): Gemini → Cancer |
| jyotisha_lagna_sign | Virgo | stable | sensitive | -54.7 min (12:05:15): Leo → Virgo |
| jyotisha_lagna_d9 | Aries | sensitive | sensitive | -54.7 min (12:05:15): Sagittarius → Capricorn; -40.7 min (12:19:18): Capricorn → Aquarius; -26.7 min (12:33:20): Aquarius → Pisces; -12.6 min (12:47:21): Pisces → Aries; +1.4 min (13:01:24): Aries → Taurus; +15.5 min (13:15:28): Taurus → Gemini; +29.6 min (13:29:33): Gemini → Cancer; +43.7 min (13:43:41): Cancer → Leo; +57.9 min (13:57:52): Leo → Virgo |
| jyotisha_lagna_d10 | Virgo | sensitive | sensitive | -42.1 min (12:17:53): Taurus → Gemini; -29.5 min (12:30:31): Gemini → Cancer; -16.9 min (12:43:08): Cancer → Leo; -4.2 min (12:55:46): Leo → Virgo; +8.4 min (13:08:25): Virgo → Libra; +21.1 min (13:21:05): Libra → Scorpio; +33.8 min (13:33:47): Scorpio → Sagittarius; +46.5 min (13:46:31): Sagittarius → Capricorn; +59.3 min (13:59:17): Capricorn → Aquarius |
| jyotisha_lagna_nakshatra_pada | Hasta-1 | sensitive | sensitive | -54.7 min (12:05:15): Uttara Phalguni-1 → Uttara Phalguni-2; -40.7 min (12:19:18): Uttara Phalguni-2 → Uttara Phalguni-3; -26.7 min (12:33:20): Uttara Phalguni-3 → Uttara Phalguni-4; -12.6 min (12:47:21): Uttara Phalguni-4 → Hasta-1; +1.4 min (13:01:24): Hasta-1 → Hasta-2; +15.5 min (13:15:28): Hasta-2 → Hasta-3; +29.6 min (13:29:33): Hasta-3 → Hasta-4; +43.7 min (13:43:41): Hasta-4 → Chitra-1; +57.9 min (13:57:52): Chitra-1 → Chitra-2 |
| moon_d9 | Gemini | stable | stable | — |
| moon_d10 | Libra | sensitive | sensitive | +18.1 min (13:18:08): Libra → Scorpio |
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
| bazi_hour_civil | 己未 | sensitive | sensitive | +0.0 min (13:00:00): 戊午 → 己未 |
| bazi_hour_LAT | 戊午 | stable | sensitive | +40.2 min (13:40:14): 戊午 → 己未 |
| ziwei_time_branch_civil | 未 | sensitive | sensitive | +0.0 min (13:00:00): 午 → 未 |
| ziwei_time_branch_LAT | 午 | stable | sensitive | +40.2 min (13:40:14): 午 → 未 |
| western_lot_fortune_sign | Sagittarius | stable | sensitive | -30.6 min (12:29:23): Scorpio → Sagittarius |

## Boundary distances

- **Western Ascendant** 06°55'17" Libra: 6.92° into its sign, 23.08° before the next (≈29.2 min since / ≈97.3 min to a cusp at 0.237°/min).
- **Jyotisha Lagna** 13°00'07" Virgo (Lahiri): 13.00° into its sign (≈54.8 min since / ≈71.7 min to a cusp). D9 segment 10.00–13.33°, D10 segment 12–15°.
- **Sect**: 418 min after sunrise, 378 min before sunset → day chart, stable.
- **BaZi / Zi Wei hour**: civil 13:00 is 0.0 min into the 未 double-hour (13:00-15:00), 120.0 min before its end; LAT 12:19 is 79.8 min into the 午 double-hour (11:00-13:00), 40.2 min before its end. Nearest boundary: 0.0 min (civil track, branch start).
- **Day boundary**: 780 min after midnight; late-Zi convention matters only for births between 23:00 and 24:00.
- **Solar terms**: birth 17.97 days after 芒种 and 13.46 days before 小暑 → month 庚午 stable.
- **Zi Wei lunar date**: 甲申年 五月初六 (leap month: False; year's leap month: 2); next new moon 2004-07-17T11:23:46+00:00 (579.9 h after birth).
- **Tibetan Losar**: birth month is after every possible Losar date (late Jan - late Mar).
- **Calendar adoption**: Gregorian civil date; no Julian/Gregorian ambiguity for 2004.
- **Planets within 1° of a sign cusp**: Mars 0.35° (tropical, ≈13 h of motion).
