# Six-culture chart reading

*This shows where several traditional symbolic systems agree or disagree, not a validated forecast. None of it is scientific evidence about your character or your future.*

## 1. Input and sensitivity

- Born **Monday 2004-05-17, 09:30 IST (UTC+05:30, no DST)** = 2004-05-17 04:00 UTC, Fatima General Hospital, Nishat Ganj / Mahanagar, Lucknow, Uttar Pradesh, India (26.8715°N, 80.9521°E; OpenStreetMap Nominatim).
- Local mean time 09:23:48; local apparent solar time 09:27:26. Sunrise 05:17, sunset 18:47.
- Time uncertainty: user-confirmed exact time, at most 1 minute off; ensemble uses +/-1 min (inner and outer identical). Modelled as **±1 min**. **Every time-dependent output is stable over that interval.**
- Nearest boundaries: Vedic Lagna Cancer 1.51° (≈7.0 min after / ≈132.1 min before a cusp); Western Ascendant Cancer 25.43° (≈117.9 / ≈21.2 min); Chinese double-hour boundary ≈27.4 min away (LAT track).
- Birthplace is a named hospital, so positional uncertainty is under ~100 m, negligible for every output.
- Houses are counted from the **Lagna** (Jyotisha); Western houses vote. Zi Wei uses the **巳** hour; BaZi hour pillar stable. (Rules JY-REFERENCE, W-HOUSES, HOUR-STABILITY.)

## 2. Verification

- Swiss Ephemeris vs NASA JPL DE440s (via Skyfield): the largest planetary difference is **6.1e-05°** (alert threshold 0.01°). The Ascendant/MC agree to within 0.002°.
- Chinese solar terms (立夏, 芒种): four engines agree to ≤1.6 s. Four Pillars: lunar_python = sxtwl (an independent codebase): **甲申 己巳 丙申 癸巳**.
- Zi Wei: canonical iztro 2.6.1 matches the py-iztro wrapper. These are the **same method**, so the match is an interface check only. All structural invariants pass.
- Maya: convertdate and a separate implementation agree; the date round-trips exactly.
- **Invariant failures: 0.**
- Unavailable: shadbala, ashtakavarga, D7_D12, zodiacal_releasing, transits. Also unavailable: Tibetan Mewa/Parkha/personal forces, and Maya/Tibetan symbolic meanings (no verifiable source).

## 3. Divergence rate (read this before the themes)

- **1/9 domains divergent** (1/9 of domains with enough evidence). Grade counts: STRONG 0, MODERATE 3, WEAK 5, DIVERGENT 1, INSUFFICIENT 0.

- **D5 Family/roots/home — DIVERGENT:** jyotisha: Ketu in house 4 from Lagna (Cancer) → negative; western: significator Moon: Taurus exaltation, triplicity (other/participating), contrary to sect → positive; ziwei: 父母 (parents) at 丙子: 天同旺/太阴庙; minors — → positive

## 4. Cross-cultural themes (STRONG first, then MODERATE)

*No domain reaches STRONG (all three clusters agreeing).*

### D1 Self/identity — MODERATE (negative)
Cluster readings: jyotisha negative, western negative, sinic mixed
- jyotisha: karaka Sun: Taurus (enemy's sign), navamsa Capricorn → negative [JY-KARAKA]
- western: Mars, Saturn in whole-sign house 1 (Cancer) from Asc Cancer → negative [HOUSE-OCC]
- bazi: Day Master 丙 (Yang Fire): weighted support 0.33 (weak) vs seasonal prosperous 旺 (month element = DM element); rooted in month, hour → mixed [BZ-D1]

### D3 Wealth/gains — MODERATE (mixed)
Cluster readings: jyotisha mixed, western positive, sinic mixed
- jyotisha: Jupiter in house 2 from Lagna (Cancer) → positive [HOUSE-OCC]
- jyotisha: Sun in house 11 from Lagna (Cancer) → negative [HOUSE-OCC]
- jyotisha: karaka Jupiter: Leo (friend's sign), navamsa Leo → positive [JY-KARAKA]
- western: Sun, Moon, Mercury in whole-sign house 11 (Taurus) from Asc Cancer → positive [HOUSE-OCC]
- bazi: Wealth (Metal) share 0.29 of weighted tally, largest element; weighted-weak DM => 财多身弱 wealth heavy / self light → mixed [BZ-D3]
- ziwei: 财帛 (wealth) at 辛未: borrowed 武曲庙化科/贪狼庙; minors 天钺/火星 → positive [ZW-PALACE + ZW-SCORE]

### D9 Fortune/spirituality/worldview — MODERATE (positive)
Cluster readings: jyotisha positive, western neutral, sinic positive
- jyotisha: karaka Jupiter: Leo (friend's sign), navamsa Leo → positive [JY-KARAKA]
- ziwei: 福德 (spirit) at 丁丑: 武曲庙化科/贪狼庙; minors 天魁/陀罗 → positive [ZW-PALACE + ZW-SCORE]

What these mean, stated narrowly:
- **D1 Self/identity:** Vedic (the Sun, a significator of self, sits in an enemy's sign) and Western (Mars in fall and Saturn in detriment both on the Cancer Ascendant) both read the self/identity area as **strained**: self-assertion and self-image are prominent and carry friction. The Sinic reading is mixed (BaZi's two Day Master strength measures disagree), so it neither confirms nor contradicts this.
- **D3 Wealth/gains:** Vedic (Jupiter strong in the 2nd, against the Sun in the 11th in an enemy's sign) and Sinic (Metal/Wealth is the largest element while the Day Master counts as weak by weight, 财多身弱; Zi Wei's wealth palace borrows 武曲/贪狼 brightly) agree that money and gains are **prominent but double-edged**. Western is plainly positive here (Sun, exalted Moon and Mercury in the 11th house of gains), so it leans the same way without matching exactly.
- **D9 Fortune/spirituality/worldview:** Vedic (Jupiter in a friendly sign and vargottama, Leo in both D1 and D9) and Zi Wei (福德 palace with 武曲庙化科 and 贪狼庙) both read fortune/worldview **favourably**. Western is neutral (Jupiter in detriment, stationing direct).
- Prominence is not outcome. None of these says anything will succeed or fail.

## 5. Disagreements (not smoothed over)

- **D5 Family/roots/home:** Vedic puts Ketu in the 4th house (home), a negative reading. Western uses the Moon (mother/home) exalted in Taurus, a positive reading. Sinic is mixed: BaZi's Resource star is combined away by 甲己合, while Zi Wei has a bright 父母 palace against a 田宅 palace carrying 太阳化忌. The systems genuinely disagree here.
- **BaZi Day Master strength:** the weighted count gives support 0.33 → weak; the seasonal rule gives prosperous 旺 (month element = DM element) — the two disagree. Favourable-element (Yong Shen) confidence: **low**. 调候 Seasonal regulation (Qiong Tong Bao Jian, 丙 born in 巳 month): Water (壬), Metal (庚). 扶抑 Strength-balancing (rule BZ-DM-1): Wood, Fire.
- **Temperament conflicts:** T1 Leadership/visibility (jyotisha strained, western mixed/neutral, sinic supported); T2 Drive/initiative (jyotisha strained, western strained, sinic supported).
- **Secondary Vedic view (from the Moon, non-voting):** D1: Moon, Mercury, Rahu in house 1 from Chandra Lagna (Moon, Aries) → negative; D3: Sun in house 2 from Chandra Lagna (Moon, Aries) → negative; D8: Mars, Venus, Saturn in house 3 from Chandra Lagna (Moon, Aries) → mixed; D6: Jupiter in house 5 from Chandra Lagna (Moon, Aries) → positive; D4: Ketu in house 7 from Chandra Lagna (Moon, Aries) → negative.

## 6. Weak areas (do not over-read)

- D2 Career/status: WEAK — jyotisha negative, western neutral, sinic mixed
- D4 Partnership: WEAK — jyotisha positive, western neutral, sinic mixed
- D6 Children/creation: WEAK — jyotisha positive, western neutral, sinic mixed
- D7 Health/routine: WEAK — jyotisha silent, western positive, sinic neutral
- D8 Mind/education/craft: WEAK — jyotisha neutral, western neutral, sinic positive
- D7 Health/routine is symbolic prominence only. **Nothing here is a health, medical or lifespan statement.**

## 7. Temperament overlay

- **T1 Leadership/visibility** — conflict: jyotisha strained (Sun score -1.00 (Taurus, enemy's sign, navamsa Capricorn)); western mixed/neutral (Sun score +0.00 (Taurus, peregrine, of the sect)); sinic supported (命宫 major stars ['天府']; visible Officer: True)
- **T2 Drive/initiative** — conflict: jyotisha strained (Mars score -1.50 (Gemini, enemy's sign, with Venus/Saturn, navamsa Capricorn)); western strained (Mars score -2.00 (Cancer, fall, triplicity (other/participating), bound, contrary to sect)); sinic supported (七杀/破军/贪狼 in 命/身: ['破军']; Seven Killings hidden x2)
- **T3 Nurturing/service** — 2 clusters: supported: jyotisha mixed/neutral (Moon score -0.50 (Aries, neutral sign, waning, with Mercury/Rahu, navamsa Cancer)); western supported (Moon score +1.75 (Taurus, exaltation, triplicity (other/participating), contrary to sect)); sinic supported (Resource stem visible: ['偏印 Indirect Resource'])
- **T4 Intellect/craft** — 1 clusters: supported: jyotisha mixed/neutral (Mercury score -0.50 (Aries, neutral sign, with Moon/Rahu, navamsa Gemini)); western mixed/neutral (Mercury score +0.10 (Taurus, face, of the sect)); sinic supported (output stem visible ['伤官 Hurting Officer']; 文昌/文曲/天机 in 命/身: ['文曲'])
- **T5 Adaptability** — 1 clusters: supported: jyotisha supported (3 of 7 grahas in dual signs); western mixed/neutral (2 of 7 planets in mutable signs); sinic silent (no declared Sinic rule)
- **T6 Discipline/structure** — 1 clusters: strained: jyotisha mixed/neutral (Saturn score -0.50 (Gemini, friend's sign, with Mars/Venus, navamsa Aquarius)); western strained (Saturn score -1.50 (Cancer, detriment, of the sect)); sinic mixed/neutral (Officer star visible but confronted by a visible Hurting Officer (伤官见官))
- Maya: **10 Ajaw 3 Zip / 12.19.11.5.0**, computed and verified. Meaning is omitted — no verifiable named Maya source available in this environment.
- Tibetan: **Male Wood Monkey** year. Meaning is omitted — no validated lineage-specific source; Mewa/Parkha/personal forces not computed.

## 8. Timing

- **Now (2026-05-17 → 2027-05-17): D3 Wealth/gains — STRONG ⭐.** jyotisha: Vimshottari Sun Mahadasha; western: annual profection age 22; sinic: BaZi Da Yun 辛未.
  - Current Vimshottari: Mahadasha Sun (2026-01-14 → 2032-01-15) / Antardasha Moon (2026-05-04 → 2026-11-02) / Pratyantardasha Venus (2026-09-24 → 2026-10-24). Dates move by about ±2 days across ±1 min.
  - Why D3 is active: the Sun Mahadasha lord sits in the 11th from the Lagna. The Western age-22 profection activates the 11th house. The BaZi 辛未 luck pillar has Direct Wealth (辛) on its stem.
  - BaZi year 丙午 (Lichun 2026 → Lichun 2027): stem 比肩 Friend, branch 劫财 Rob Wealth. Activation is not outcome.
- Next: 2027-05-17 → 2030-10-06: D3 Wealth/gains — MODERATE (jyotisha: Vimshottari Sun Mahadasha; sinic: BaZi Da Yun 辛未)
- Next: 2028-05-17 → 2029-05-17: D1 Self/identity — MODERATE (jyotisha: Vimshottari Sun Mahadasha; western: annual profection age 24)
- Next: 2030-10-06 → 2032-01-13: D2 Career/status — MODERATE (jyotisha: Vimshottari Sun Mahadasha; sinic: BaZi Da Yun 壬申)
- Next: 2030-10-06 → 2032-01-13: D3 Wealth/gains — MODERATE (jyotisha: Vimshottari Sun Mahadasha; sinic: BaZi Da Yun 壬申)
- Zi Wei decadal (not a convergence by itself): 16-25 (父母 子) ≈2019–2029; then 26-35 (福德 丑) ≈2029–2039.

## 9. Claims removed

- sensitive_to_birth_time: 0 — projections that change inside the uncertainty interval; displayed, never vote
- secondary_reference_frame_not_voting: 5 — Jyotisha houses from Chandra Lagna (JY-REFERENCE)
- neutral_polarity_no_theme: 14
- school_dependent_low_confidence: 1
- no_validated_source: 4
- unavailable_methods: 5
- barnum_screen: every retained projection is tied to a computed datum via a registry rule; no automated Barnum test was run, so generic-sounding prose was avoided by hand in FINAL_READING.md

## Closing frame

These results show where several traditional symbolic systems, each computed under declared conventions and checked against independent engines, happen to agree or disagree. The domain rules and weights are declared in `SYNTHESIS.json` → `registry`, and different reasonable rules would give different grades. Nothing here is a validated forecast, a fate, or a basis for medical, financial or legal decisions.
