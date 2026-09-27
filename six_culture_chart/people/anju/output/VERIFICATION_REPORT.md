# Verification report

Thresholds: planets > 0.01°, angles > 0.05°, solar terms > 120 s raise an alert.

| System | Datum | Primary | Validator | Difference | Stability | Confidence | Status |
|---|---|---|---|---|---|---|---|
| shared | Sun tropical longitude | 96.92087 | Skyfield + JPL DE440s | 2.54269e-06 | stable (sign) | high | pass |
| shared | Moon tropical longitude | 214.37134 | Skyfield + JPL DE440s | 3.03107e-05 | stable (sign) | high | pass |
| shared | Mercury tropical longitude | 99.72528 | Skyfield + JPL DE440s | 1.0925e-06 | stable (sign) | high | pass |
| shared | Venus tropical longitude | 63.59415 | Skyfield + JPL DE440s | 2.9525e-06 | stable (sign) | high | pass |
| shared | Mars tropical longitude | 132.27004 | Skyfield + JPL DE440s | 1.76501e-06 | stable (sign) | high | pass |
| shared | Jupiter tropical longitude | 347.74651 | Skyfield + JPL DE440s | 5.3728e-07 | stable (sign) | high | pass |
| shared | Saturn tropical longitude | 98.13609 | Skyfield + JPL DE440s | 6.14859e-07 | stable (sign) | high | pass |
| shared | Uranus tropical longitude | 203.66262 | Skyfield + JPL DE440s | 2.7972e-07 | stable (sign) | high | pass |
| shared | Neptune tropical longitude | 247.48035 | Skyfield + JPL DE440s | 2.55299e-07 | stable (sign) | high | pass |
| shared | Pluto tropical longitude | 184.12156 | Skyfield + JPL DE440s | 3.77093e-07 | stable (sign) | high | pass |
| jyotisha | Mean lunar node (Rahu) tropical longitude | 258.44447 | Meeus mean-node polynomial (independent formula) | 0.00479553 | stable | high | pass |
| western | ASC tropical | 107.94964 | Skyfield GAST + IAU2000A true obliquity, textbook formula | 0.000679706 | outer stable, inner stable | high | pass |
| western | MC tropical | 6.39029 | Skyfield GAST + IAU2000A true obliquity, textbook formula | 0.00085923 | outer stable, inner stable | high | pass |
| jyotisha | Lagna (sidereal Ascendant) | 84.44887 | Skyfield Asc minus same Lahiri ayanamsha | 0.000679706 | outer stable, inner stable | medium | pass |
| jyotisha | Lahiri ayanamsha | 23.50077 | — | — | stable | medium | single-engine |
| shared | sunrise | 1974-06-29T05:20:23+05:30 | Skyfield almanac + DE440s | 13.1415 | stable | high | pass |
| shared | sunset | 1974-06-29T19:22:58+05:30 | Skyfield almanac + DE440s | 12.7553 | stable | high | pass |
| bazi | solar term 芒种 instant | 1974-06-06T01:51:39+00:00 | Skyfield/DE440s; lunar_python; sxtwl | 0.511036 | stable | high | pass |
| bazi | solar term 小暑 instant | 1974-07-07T12:11:05+00:00 | Skyfield/DE440s; lunar_python; sxtwl | 0.761138 | stable | high | pass |
| bazi | Four Pillars (civil_clock) | ['甲寅', '庚午', '辛丑', '辛卯'] | sxtwl 2.0.7 (independent C++ calendar) | identical | stable over the interval (辛卯) | high | pass |
| bazi | Four Pillars (local_apparent_solar_time) | ['甲寅', '庚午', '辛丑', '辛卯'] | sxtwl 2.0.7 (independent C++ calendar) | identical | stable over the interval (辛卯) | high | pass |
| bazi | Da Yun start | 1982-02-21 | lunar_python Yun (sect 1 rounding) | 13 days | convention difference ~10 days; time uncertainty shifts start by < 1 day | medium | pass (convention difference disclosed) |
| ziwei | Zi Wei chart (time branch 卯) | {'ming': '卯', 'bureau': '火六局'} | py-iztro 0.1.5 (bundles iztro 2.5.0) -- SAME METHOD, interface check only | — | primary (civil): stable over the interval (卯); LAT: stable over the interval (卯) | medium | pass |
| ziwei | Zi Wei chart (time branch 辰) | {'ming': '寅', 'bureau': '火六局'} | py-iztro 0.1.5 (bundles iztro 2.5.0) -- SAME METHOD, interface check only | — | alternative hour, outside the uncertainty interval | not used | pass |
| maya | Long Count / Tzolkin / Haab | 2 Chikchan 18 Sotz' / 12.18.0.17.5 | own GMT-584283 implementation | identical (Haab month spelled Zip vs Sip = same month) | stable (date-based) | high | pass |
| tibetan | element-animal year | Male Wood Tiger | BaZi year pillar 甲申 (Yang Wood Monkey) + Losar bracket | — | stable | medium | pass (limited overlay) |

## Invariants

| System | Invariant | Pass |
|---|---|---|
| ziwei | 12 unique palace names | ✅ |
| ziwei | 12 unique earthly branches | ✅ |
| ziwei | 14 major stars each placed exactly once | ✅ |
| ziwei | four transformations present (禄权科忌 once each) | ✅ |
| ziwei | Zi Wei / Tian Fu mirror about Yin-Shen axis | ✅ |
| ziwei | decadal ranges contiguous 10-year blocks | ✅ |
| ziwei | 12 unique palace names | ✅ |
| ziwei | 12 unique earthly branches | ✅ |
| ziwei | 14 major stars each placed exactly once | ✅ |
| ziwei | four transformations present (禄权科忌 once each) | ✅ |
| ziwei | Zi Wei / Tian Fu mirror about Yin-Shen axis | ✅ |
| ziwei | decadal ranges contiguous 10-year blocks | ✅ |
| jyotisha | Rahu-Ketu separation 180 (-10min) | ✅ |
| jyotisha | Rahu-Ketu separation 180 (-5min) | ✅ |
| jyotisha | Rahu-Ketu separation 180 (+0min) | ✅ |
| jyotisha | Rahu-Ketu separation 180 (+5min) | ✅ |
| jyotisha | Rahu-Ketu separation 180 (+10min) | ✅ |
| jyotisha | Vimshottari lord years total 120 | ✅ |
| jyotisha | Vimshottari periods continuous, ordered, non-overlapping (-10min) | ✅ |
| jyotisha | Vimshottari periods continuous, ordered, non-overlapping (+0min) | ✅ |
| jyotisha | Vimshottari periods continuous, ordered, non-overlapping (+10min) | ✅ |
| western | Egyptian bounds: every sign ends at 30; planet totals J79 V82 Me76 Ma66 S57 | ✅ |
| bazi | birth after 芒种 and before 小暑 (month 庚午) | ✅ |
| bazi | Da Yun periods contiguous 10-year blocks | ✅ |
| maya | Maya conversion round-trips exactly | ✅ |
| all | No 'independent' validator shares calculation code without disclosure | ✅ |

**Failures:** 0
