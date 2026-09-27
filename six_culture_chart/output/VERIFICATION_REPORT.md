# Verification report

Thresholds: planets > 0.01°, angles > 0.05°, solar terms > 120 s raise an alert.

| System | Datum | Primary | Validator | Difference | Stability | Confidence | Status |
|---|---|---|---|---|---|---|---|
| shared | Sun tropical longitude | 56.58954 | Skyfield + JPL DE440s | 5.25426e-06 | stable (sign) | high | pass |
| shared | Moon tropical longitude | 34.08315 | Skyfield + JPL DE440s | 6.05659e-05 | stable (sign) | high | pass |
| shared | Mercury tropical longitude | 30.93254 | Skyfield + JPL DE440s | 5.9292e-06 | stable (sign) | high | pass |
| shared | Venus tropical longitude | 86.12689 | Skyfield + JPL DE440s | 1.40329e-06 | stable (sign) | high | pass |
| shared | Mars tropical longitude | 96.20887 | Skyfield + JPL DE440s | 3.21452e-06 | stable (sign) | high | pass |
| shared | Jupiter tropical longitude | 159.13310 | Skyfield + JPL DE440s | 2.59242e-07 | stable (sign) | high | pass |
| shared | Saturn tropical longitude | 100.43041 | Skyfield + JPL DE440s | 6.57609e-07 | stable (sign) | high | pass |
| shared | Uranus tropical longitude | 336.55309 | Skyfield + JPL DE440s | 2.22721e-07 | stable (sign) | high | pass |
| shared | Neptune tropical longitude | 315.39350 | Skyfield + JPL DE440s | 3.48082e-08 | stable (sign) | high | pass |
| shared | Pluto tropical longitude | 261.54968 | Skyfield + JPL DE440s | 2.87215e-08 | stable (sign) | high | pass |
| jyotisha | Mean lunar node (Rahu) tropical longitude | 40.43866 | Meeus mean-node polynomial (independent formula) | 0.00335514 | stable | high | pass |
| western | ASC tropical | 115.41304 | Skyfield GAST + IAU2000A true obliquity, textbook formula | 0.00167747 | outer stable, inner stable | high | pass |
| western | MC tropical | 17.50608 | Skyfield GAST + IAU2000A true obliquity, textbook formula | 0.00209394 | outer stable, inner stable | high | pass |
| jyotisha | Lagna (sidereal Ascendant) | 91.49484 | Skyfield Asc minus same Lahiri ayanamsha | 0.00167747 | outer stable, inner stable | medium | pass |
| jyotisha | Lahiri ayanamsha | 23.91820 | — | — | stable | medium | single-engine |
| shared | sunrise | 2004-05-17T05:17:47+05:30 | Skyfield almanac + DE440s | 11.182 | stable | high | pass |
| shared | sunset | 2004-05-17T18:47:40+05:30 | Skyfield almanac + DE440s | 12.1443 | stable | high | pass |
| bazi | solar term 立夏 instant | 2004-05-05T04:02:26+00:00 | Skyfield/DE440s; lunar_python; sxtwl | 1.14513 | stable | high | pass |
| bazi | solar term 芒种 instant | 2004-06-05T08:13:44+00:00 | Skyfield/DE440s; lunar_python; sxtwl | 1.5913 | stable | high | pass |
| bazi | Four Pillars (civil_clock) | ['甲申', '己巳', '丙申', '癸巳'] | sxtwl 2.0.7 (independent C++ calendar) | identical | stable over the interval (癸巳) | high | pass |
| bazi | Four Pillars (local_apparent_solar_time) | ['甲申', '己巳', '丙申', '癸巳'] | sxtwl 2.0.7 (independent C++ calendar) | identical | stable over the interval (癸巳) | high | pass |
| bazi | Da Yun start | 2010-10-07 | lunar_python Yun (sect 1 rounding) | 10 days | convention difference ~10 days; time uncertainty shifts start by < 1 day | medium | pass (convention difference disclosed) |
| ziwei | Zi Wei chart (time branch 辰) | {'ming': '子', 'bureau': '水二局'} | py-iztro 0.1.5 (bundles iztro 2.5.0) -- SAME METHOD, interface check only | — | alternative hour, outside the uncertainty interval | not used | pass |
| ziwei | Zi Wei chart (time branch 巳) | {'ming': '亥', 'bureau': '火六局'} | py-iztro 0.1.5 (bundles iztro 2.5.0) -- SAME METHOD, interface check only | — | primary (civil): stable over the interval (巳); LAT: stable over the interval (巳) | medium | pass |
| maya | Long Count / Tzolkin / Haab | 10 Ajaw 3 Zip / 12.19.11.5.0 | own GMT-584283 implementation | identical (Haab month spelled Zip vs Sip = same month) | stable (date-based) | high | pass |
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
| jyotisha | Rahu-Ketu separation 180 (-1min) | ✅ |
| jyotisha | Rahu-Ketu separation 180 (+0min) | ✅ |
| jyotisha | Rahu-Ketu separation 180 (+1min) | ✅ |
| jyotisha | Vimshottari lord years total 120 | ✅ |
| jyotisha | Vimshottari periods continuous, ordered, non-overlapping (-1min) | ✅ |
| jyotisha | Vimshottari periods continuous, ordered, non-overlapping (+0min) | ✅ |
| jyotisha | Vimshottari periods continuous, ordered, non-overlapping (+1min) | ✅ |
| western | Egyptian bounds: every sign ends at 30; planet totals J79 V82 Me76 Ma66 S57 | ✅ |
| bazi | birth after 立夏 and before 芒种 (month 己巳) | ✅ |
| bazi | Da Yun periods contiguous 10-year blocks | ✅ |
| maya | Maya conversion round-trips exactly | ✅ |
| all | No 'independent' validator shares calculation code without disclosure | ✅ |

**Failures:** 0
