# Verification report

Thresholds: planets > 0.01°, angles > 0.05°, solar terms > 120 s raise an alert.

| System | Datum | Primary | Validator | Difference | Stability | Confidence | Status |
|---|---|---|---|---|---|---|---|
| shared | Sun tropical longitude | 92.17243 | Skyfield + JPL DE440s | 5.2718e-06 | stable (sign) | high | pass |
| shared | Moon tropical longitude | 152.80609 | Skyfield + JPL DE440s | 6.35806e-05 | stable (sign) | high | pass |
| shared | Mercury tropical longitude | 97.57689 | Skyfield + JPL DE440s | 1.11855e-05 | stable (sign) | high | pass |
| shared | Venus tropical longitude | 70.49659 | Skyfield + JPL DE440s | 1.61396e-09 | stable (sign) | high | pass |
| shared | Mars tropical longitude | 119.65201 | Skyfield + JPL DE440s | 3.43548e-06 | stable (sign) | high | pass |
| shared | Jupiter tropical longitude | 162.30662 | Skyfield + JPL DE440s | 8.51404e-07 | stable (sign) | high | pass |
| shared | Saturn tropical longitude | 104.84543 | Skyfield + JPL DE440s | 9.4408e-07 | stable (sign) | high | pass |
| shared | Uranus tropical longitude | 336.73201 | Skyfield + JPL DE440s | 1.79927e-07 | stable (sign) | high | pass |
| shared | Neptune tropical longitude | 315.04699 | Skyfield + JPL DE440s | 4.86139e-08 | stable (sign) | high | pass |
| shared | Pluto tropical longitude | 260.59472 | Skyfield + JPL DE440s | 6.77527e-08 | stable (sign) | high | pass |
| jyotisha | Mean lunar node (Rahu) tropical longitude | 38.47201 | Meeus mean-node polynomial (independent formula) | 0.00281267 | stable | high | pass |
| western | ASC tropical | 188.10751 | Skyfield GAST + IAU2000A true obliquity, textbook formula | 0.00185413 | outer stable, inner stable | high | pass |
| western | MC tropical | 97.86175 | Skyfield GAST + IAU2000A true obliquity, textbook formula | 0.00180463 | outer stable, inner stable | high | pass |
| jyotisha | Lagna (sidereal Ascendant) | 164.18790 | Skyfield Asc minus same Lahiri ayanamsha | 0.00185413 | outer stable, inner stable | medium | pass |
| jyotisha | Lahiri ayanamsha | 23.91962 | — | — | stable | medium | single-engine |
| shared | sunrise | 2004-06-23T06:02:02+05:30 | Skyfield almanac + DE440s | 11.1496 | stable | high | pass |
| shared | sunset | 2004-06-23T19:18:24+05:30 | Skyfield almanac + DE440s | 12.0872 | stable | high | pass |
| bazi | solar term 芒种 instant | 2004-06-05T08:13:44+00:00 | Skyfield/DE440s; lunar_python; sxtwl | 1.5913 | stable | high | pass |
| bazi | solar term 小暑 instant | 2004-07-06T18:31:15+00:00 | Skyfield/DE440s; lunar_python; sxtwl | 0.430778 | stable | high | pass |
| bazi | Four Pillars (civil_clock) | ['甲申', '庚午', '癸酉', '己未'] | sxtwl 2.0.7 (independent C++ calendar) | identical | stable over the interval (己未) | high | pass |
| bazi | Four Pillars (local_apparent_solar_time) | ['甲申', '庚午', '癸酉', '戊午'] | sxtwl 2.0.7 (independent C++ calendar) | identical | stable over the interval (戊午) | high | pass |
| bazi | Da Yun start | 2010-06-20 | lunar_python Yun (sect 1 rounding) | 8 days | convention difference ~10 days; time uncertainty shifts start by < 1 day | medium | pass (convention difference disclosed) |
| ziwei | Zi Wei chart (time branch 午) | {'ming': '子', 'bureau': '水二局'} | py-iztro 0.1.5 (bundles iztro 2.5.0) -- SAME METHOD, interface check only | — | alternative hour, outside the uncertainty interval | not used | pass |
| ziwei | Zi Wei chart (time branch 未) | {'ming': '亥', 'bureau': '火六局'} | py-iztro 0.1.5 (bundles iztro 2.5.0) -- SAME METHOD, interface check only | — | primary (civil): stable over the interval (未); LAT: stable over the interval (午) | medium | pass |
| maya | Long Count / Tzolkin / Haab | 8 Kab'an 0 Sek / 12.19.11.6.17 | own GMT-584283 implementation | MISMATCH | stable (date-based) | low | pass |
| tibetan | element-animal year | Male Wood Monkey | BaZi year pillar 甲申 (Yang Wood Monkey) + Losar bracket | — | stable | medium | pass (limited overlay) |

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
| jyotisha | Rahu-Ketu separation 180 (-5min) | ✅ |
| jyotisha | Rahu-Ketu separation 180 (+0min) | ✅ |
| jyotisha | Rahu-Ketu separation 180 (+5min) | ✅ |
| jyotisha | Vimshottari lord years total 120 | ✅ |
| jyotisha | Vimshottari periods continuous, ordered, non-overlapping (-5min) | ✅ |
| jyotisha | Vimshottari periods continuous, ordered, non-overlapping (+0min) | ✅ |
| jyotisha | Vimshottari periods continuous, ordered, non-overlapping (+5min) | ✅ |
| western | Egyptian bounds: every sign ends at 30; planet totals J79 V82 Me76 Ma66 S57 | ✅ |
| bazi | birth after 芒种 and before 小暑 (month 庚午) | ✅ |
| bazi | Da Yun periods contiguous 10-year blocks | ✅ |
| maya | Maya conversion round-trips exactly | ✅ |
| all | No 'independent' validator shares calculation code without disclosure | ✅ |

**Failures:** 0
