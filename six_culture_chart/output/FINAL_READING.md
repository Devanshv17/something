# Six-culture chart reading

*This is computed symbolic corroboration between traditional systems, not a validated forecast. None of it is scientific evidence about your character or your future.*

## 1. Input and sensitivity

- Born **Monday 2004-05-17, 09:30 IST (UTC+05:30, no DST)** = 2004-05-17 04:00 UTC, Lucknow (26.8467°N, 80.9462°E; city-centre coordinates).
- Local mean time 09:23:47; local apparent solar time 09:27:25. Sunrise 05:17, sunset 18:47.
- Your stated uncertainty (15–30 min) was modelled as ±30 min (primary) and ±15 min (inner). **Three things move within that window:**
  - **Vedic rising sign (Lagna)**: Cancer 1.49°. If birth was **≥6.9 min earlier (before ~09:23)** it is **Gemini**. This is sensitive even within ±15 min, so no Vedic house-based claim is graded.
  - **Western Ascendant**: Cancer 25.41°. If birth was **≥21.3 min later (after ~09:51)** it becomes **Leo**. Stable within ±15 min.
  - **Chinese double-hour**: 巳 Si on the civil clock across the whole window. Under local solar time it becomes 辰 Chen only if birth was ≥27.4 min earlier (before ~09:02). This affects the BaZi hour pillar (癸巳 vs 壬辰) and the whole Zi Wei palace layout.
- Stable across ±30 min: all planetary signs (both zodiacs), Moon nakshatra (Ashwini), the Vedic Moon-sign reference, day/night sect, the BaZi year, month and day pillars, and the Maya and Tibetan dates.

## 2. Verification

- Swiss Ephemeris vs NASA JPL DE440s (via Skyfield): the largest planetary difference is **6.1e-05°** (alert threshold 0.01°). The Ascendant/MC agree to within 0.002°.
- Chinese solar terms (立夏, 芒种): four engines agree to ≤1.6 s. Four Pillars: lunar_python = sxtwl (an independent codebase).
- Zi Wei: canonical iztro 2.6.1 matches the py-iztro wrapper. These are the **same method**, so the match is an interface check, not independent confirmation. All 6 structural invariants pass for both hour alternatives.
- Maya: convertdate and a separate implementation agree; the date round-trips exactly.
- **Invariant failures: 0.**
- Unavailable or not computed: Shadbala, Ashtakavarga, Pratyantardasha, D7/D12, zodiacal releasing, transits, Tibetan Mewa/Parkha/personal forces, and Maya/Tibetan symbolic meanings (no verifiable source).

## 3. Divergence rate (read this before the themes)

- Primary (±30 min): **0/9 domains divergent** (0/9 of domains with enough evidence). Grade counts: {'STRONG': 0, 'MODERATE': 3, 'WEAK': 6, 'DIVERGENT': 0, 'INSUFFICIENT': 0}.
- Inner (±15 min, Western houses allowed): 0/9 divergent; counts {'STRONG': 0, 'MODERATE': 4, 'WEAK': 5, 'DIVERGENT': 0, 'INSUFFICIENT': 0}.
- There are no outright conflicts, but there is also **no STRONG domain**. Most agreement is between Jyotisha and the Sinic cluster. With Vedic houses excluded, the Western cluster is mostly neutral.

## 4. Cross-cultural themes

### D3 Wealth/gains — MODERATE (mixed)
- jyotisha: Sun in house 2 from Chandra Lagna (Moon, Aries) → negative [HOUSE-OCC]
- jyotisha: karaka Jupiter: Leo (friend's sign), navamsa Leo → positive [JY-KARAKA]
- bazi: Wealth (Metal) share 0.29 of weighted tally, largest element; weighted-weak DM => 财多身弱 wealth heavy / self light → mixed [BZ-D3]
- ziwei: 财帛 (wealth) at 辛未: borrowed 武曲庙化科/贪狼庙; minors 天钺/火星 → positive [ZW-PALACE + ZW-SCORE]

### D4 Partnership — MODERATE (mixed)
- jyotisha: Ketu in house 7 from Chandra Lagna (Moon, Aries) → negative [HOUSE-OCC]
- jyotisha: karaka Venus: Gemini (friend's sign), navamsa Libra → positive [JY-KARAKA]
- bazi: spouse palace 申 Shen (main qi 庚 Indirect Wealth = spouse star for a male); interactions on it: ['destruction', 'punishment', 'six'] → mixed [BZ-D4]
- ziwei: 夫妻 (spouse) at 癸酉: 廉贞平化禄/破军陷化权; minors 文曲 [身宫 body palace] → mixed [ZW-PALACE + ZW-SCORE]

### D9 Fortune/spirituality/worldview — MODERATE (positive)
- jyotisha: karaka Jupiter: Leo (friend's sign), navamsa Leo → positive [JY-KARAKA]
- ziwei: 福德 (spirit) at 丁丑: 武曲庙化科/贪狼庙; minors 天魁/陀罗 → positive [ZW-PALACE + ZW-SCORE]

### D1 Self/identity — MODERATE (negative) *(inner ±15 min scenario only)*
- jyotisha: Moon, Mercury, Rahu in house 1 from Chandra Lagna (Moon, Aries) → negative [HOUSE-OCC]
- jyotisha: karaka Sun: Taurus (enemy's sign), navamsa Capricorn → negative [JY-KARAKA]
- western: Mars, Saturn in whole-sign house 1 (Cancer) from Asc Cancer → negative [HOUSE-OCC]

What these mean, stated narrowly:
- **D3 Wealth/gains (MODERATE, mixed):** Jyotisha (Jupiter as wealth-significator in a friendly sign, against the Sun in the 2nd from the Moon) and BaZi (Metal/Wealth is the largest element while the Day Master counts as weak, 财多身弱) agree on the same thing: money matters are **prominent but double-edged**. Neither system says success or failure.
- **D4 Partnership (MODERATE, mixed):** Jyotisha (Venus friendly and in its own navamsa, but Ketu in the 7th from the Moon) and the Sinic cluster (spouse palace 申 combined with, punished by and broken by 巳; Zi Wei's 夫妻 palace is also the Body palace, with 廉贞化禄 and 破军(陷)化权) agree that relationships are **a prominent, mixed theme**.
- **D9 Fortune/worldview (MODERATE, positive):** Jyotisha (Jupiter in a friendly sign and vargottama, Leo in both D1 and D9) and Zi Wei (福德 palace with 武曲庙化科 and 贪狼庙) both read **favourably**. The Western cluster is neutral here (Jupiter in detriment, stationing direct).
- **D1 Self (inner scenario only, negative):** if the Western Ascendant is Cancer, Mars (in fall) and Saturn (in detriment) sit on it. Jyotisha independently puts Rahu with the Moon and Mercury in the Moon-sign. Both read this as a **strained self-image theme**. Of these, only the Jyotisha part is stable over ±30 min.

## 5. Disagreements (not smoothed over)

- **Day Master strength (BaZi internal):** the weighted count gives support 0.33 → weak. The seasonal rule gives 丙 fire born in 巳 month → prosperous. These disagree, so BaZi's useful-element (Yong Shen) verdict is **low confidence**. The seasonal school (Qiong Tong) points to 壬 water and 庚 metal. The strength-balancing school, using the weak verdict, points to wood and fire. These conclusions are opposite.
- **Temperament axes with conflicts:** T1 leadership (Jyotisha: Sun in an enemy's sign → strained; Zi Wei: 天府 in 命宫 → supported) and T2 drive (Mars: fall in Western, enemy's sign in Jyotisha → strained; Sinic: 破军 in the Body palace plus two hidden Seven Killings → supported).
- **Vedic Lagna Gemini vs Cancer:** the two alternatives give different house pictures. With Gemini, Mars, Venus and Saturn fall on the Lagna; with Cancer, Jupiter falls in the 2nd. Neither is chosen.

## 6. Weak and insufficient areas (do not over-read)

- D1 Self/identity: WEAK — cluster readings {'jyotisha': 'negative', 'western': 'neutral', 'sinic': 'mixed'}
- D2 Career/status: WEAK — cluster readings {'jyotisha': 'negative', 'western': 'neutral', 'sinic': 'mixed'}
- D5 Family/roots/home: WEAK — cluster readings {'jyotisha': 'neutral', 'western': 'positive', 'sinic': 'mixed'}
- D6 Children/creation: WEAK — cluster readings {'jyotisha': 'positive', 'western': 'neutral', 'sinic': 'mixed'}
- D7 Health/routine: WEAK — cluster readings {'jyotisha': 'silent', 'western': 'positive', 'sinic': 'neutral'}
- D8 Mind/education/craft: WEAK — cluster readings {'jyotisha': 'mixed', 'western': 'neutral', 'sinic': 'positive'}
- D7 Health/routine is reported as symbolic prominence only. **Nothing here is a health, medical or lifespan statement.**

## 7. Temperament overlay

- **T1 Leadership/visibility** — conflict: jyotisha strained (Sun score -1.00 (Taurus, enemy's sign)); western mixed/neutral (Sun score +0.00 (Taurus, peregrine)); sinic supported (命宫 major stars ['天府']; visible Officer: True)
- **T2 Drive/initiative** — conflict: jyotisha strained (Mars score -1.50); western strained (Mars score -2.00 (fall, contrary to sect)); sinic supported (七杀/破军/贪狼 in 命/身: ['破军']; Seven Killings hidden x2)
- **T3 Nurturing/service** — 2 clusters: supported: jyotisha mixed/neutral (Moon score -0.50 (waning, with Rahu)); western supported (Moon score +1.75 (exalted in Taurus)); sinic supported (Resource stem visible: ['偏印 Indirect Resource'])
- **T4 Intellect/craft** — 1 clusters: supported: jyotisha mixed/neutral (Mercury score -0.50 (Aries with Rahu; navamsa Gemini)); western mixed/neutral (Mercury score +0.10 (Taurus, face)); sinic supported (output stem visible ['伤官 Hurting Officer']; 文昌/文曲/天机 in 命/身: ['文曲'])
- **T5 Adaptability** — 1 clusters: supported: jyotisha supported (3 of 7 grahas in dual signs); western mixed/neutral (2 of 7 planets in mutable signs); sinic silent (no declared Sinic rule)
- **T6 Discipline/structure** — 1 clusters: strained: jyotisha mixed/neutral (Saturn score -0.50); western strained (Saturn score -1.50 (detriment, of sect)); sinic mixed/neutral (Direct Officer visible but confronted by visible Hurting Officer (伤官见官))
- Maya: **10 Ajaw 3 Zip / 12.19.11.5.0**, computed and verified. Meaning is omitted — no verifiable named Maya source available in this environment.
- Tibetan: **Male Wood Monkey** year. Meaning is omitted — no validated lineage-specific source; Mewa/Parkha/personal forces not computed.

## 8. Timing

- **Now (2026-05-17 → 2027-05-17): D3 Wealth/gains — STRONG ⭐.** jyotisha: Vimshottari Sun Mahadasha; western: annual profection age 22; sinic: BaZi Da Yun 辛未.
  - Techniques: the Jyotisha Sun Mahadasha started between 2025-11-27 and 2026-03-04 depending on birth time; the Sun is the wealth-house occupant from the Moon. The Western age-22 profection activates the 11th house (gains) for any Ascendant. The BaZi 辛未 luck pillar has Direct Wealth on its stem.
  - This shows the area is **activated**, not what the outcome will be. BaZi's annual pillar for Lichun 2026 → Lichun 2027 is 丙午 = 比肩 Friend / 劫财 Rob Wealth: a companion/competitor year for a wealth theme. The natal D3 reading is itself mixed.
  - The current Vimshottari sub-period is **sensitive**: Sun–Moon at 09:30, but Sun–Mars if birth was ~30 min later.
- Next: 2027-05-17 → 2030-10-06: D3 Wealth/gains — MODERATE (jyotisha: Vimshottari Sun Mahadasha; sinic: BaZi Da Yun 辛未)
- Next: 2028-05-17 → 2029-05-17: D1 Self/identity — MODERATE (jyotisha: Vimshottari Sun Mahadasha; western: annual profection age 24)
- Next: 2030-10-06 → 2031-11-27: D2 Career/status — MODERATE (jyotisha: Vimshottari Sun Mahadasha; sinic: BaZi Da Yun 壬申)
- Next: 2030-10-06 → 2031-11-27: D3 Wealth/gains — MODERATE (jyotisha: Vimshottari Sun Mahadasha; sinic: BaZi Da Yun 壬申)
- Zi Wei decadal: 16–25 (父母 palace; roughly lunar years 2019–2028) → 26–35 (福德 palace, D9; roughly 2029–2038). This holds only for the 巳-hour chart.

## 9. Claims removed

- sensitive_to_birth_time: 27 — Lagna/Asc-house and Zi Wei 辰-hour projections: displayed as alternatives, never vote (Western Asc houses vote only in the inner ±15 scenario)
- neutral_polarity_no_theme: 13
- school_dependent_low_confidence: 1
- no_validated_source: 4
- unavailable_methods: 6
- barnum_screen: every retained projection is tied to a computed datum via a registry rule; no automated Barnum test was run, so generic-sounding prose was avoided by hand in FINAL_READING.md

## Closing frame

These results show where several traditional symbolic systems, each computed under declared conventions and checked against independent engines, happen to agree or disagree. The domain rules and weights are declared in `SYNTHESIS.json` → `registry`, and different reasonable rules would give different grades. Nothing here is a validated forecast, a fate, or a basis for medical, financial or legal decisions.
