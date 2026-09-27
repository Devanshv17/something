# Six-culture chart reading

*This shows where several traditional symbolic systems agree or disagree, not a validated forecast. None of it is scientific evidence about your character or your future.*

## 1. Input and sensitivity

- Born **Saturday 1974-06-29, 06:15 IST (UTC+05:30, no DST)** = 1974-06-29 00:45 UTC, Roorkee, Haridwar district, Uttarakhand, India (Uttar Pradesh in 1974) (29.8693°N, 77.8902°E; OpenStreetMap Nominatim).
- Local mean time 05:56:33; local apparent solar time 05:53:19. Sunrise 05:20, sunset 19:22.
- Time uncertainty: approximate time, stated as within about 5-10 minutes; outer envelope +/-10 min is primary, +/-5 min is the inner scenario. Modelled as **±10 min** (inner scenario ±5 min). **Outputs that change inside it:** jyotisha_lagna_d9 (Aries→Taurus at -5.2 min); jyotisha_lagna_d10 (Capricorn→Aquarius at -2.1 min); jyotisha_lagna_nakshatra_pada (Punarvasu-1→Punarvasu-2 at -5.2 min).
- Nearest boundaries: Vedic Lagna Gemini 24.45° (≈113.3 min after / ≈25.7 min before a cusp); Western Ascendant Cancer 17.95° (≈83.2 / ≈55.9 min); Chinese double-hour boundary ≈45.0 min away (civil track).
- Coordinates: OpenStreetMap Nominatim, node 4373395280 'Roorkee' (city centre; hospital not given, so a few km of positional uncertainty). A different hospital in the same town shifts the Ascendant by roughly 0.1°.
- Houses are counted from the **Lagna** (Jyotisha); Western houses vote. Zi Wei uses the **卯** hour; BaZi hour pillar stable. (Rules JY-REFERENCE, W-HOUSES, HOUR-STABILITY.)

## 2. Verification

- Swiss Ephemeris vs NASA JPL DE440s (via Skyfield): the largest planetary difference is **3.0e-05°** (alert threshold 0.01°). The Ascendant/MC agree to within 0.002°.
- Chinese solar terms (芒种, 小暑): four engines agree to ≤0.8 s. Four Pillars: lunar_python = sxtwl (an independent codebase): **甲寅 庚午 辛丑 辛卯**.
- Zi Wei: canonical iztro 2.6.1 matches the py-iztro wrapper. These are the **same method**, so the match is an interface check only. All structural invariants pass.
- Maya: convertdate and a separate implementation agree; the date round-trips exactly.
- **Invariant failures: 0.**
- Unavailable: shadbala, ashtakavarga, pratyantardasha, D7_D12, zodiacal_releasing, transits. Also unavailable: Tibetan Mewa/Parkha/personal forces, and Maya/Tibetan symbolic meanings (no verifiable source).

## 3. Divergence rate (read this before the themes)

- **1/9 domains divergent** (1/8 of domains with enough evidence). Grade counts: STRONG 4, MODERATE 0, WEAK 3, DIVERGENT 1, INSUFFICIENT 1.

- **D2 Career/status — DIVERGENT:** jyotisha: karaka Sun: Gemini (neutral sign), navamsa Aquarius → negative; bazi: Officer visible in none pillar(s); Seven Killings hidden x1 → positive; ziwei: 官禄 (career) at 辛未: borrowed 武曲庙化科/贪狼庙; minors 文昌/文曲/天钺 → positive

## 4. Cross-cultural themes (STRONG first, then MODERATE)

### D1 Self/identity — STRONG (negative)
Cluster readings: jyotisha negative, western negative, sinic negative
- jyotisha: Sun, Mercury, Saturn in house 1 from Lagna (Gemini) → negative [HOUSE-OCC]
- jyotisha: karaka Sun: Gemini (neutral sign), navamsa Aquarius → negative [JY-KARAKA]
- western: Sun, Mercury, Saturn in whole-sign house 1 (Cancer) from Asc Cancer → negative [HOUSE-OCC]
- bazi: Day Master 辛 (Yin Metal): weighted support 0.43 (weak) vs seasonal weakened (month drains/controls/is controlled); rooted in day → negative [BZ-D1]
- ziwei: 命宫 (soul) at 丁卯: 天相陷; minors 擎羊 → negative [ZW-PALACE + ZW-SCORE]

### D3 Wealth/gains — STRONG (mixed)
Cluster readings: jyotisha mixed, western mixed, sinic mixed
- jyotisha: Mars in house 2 from Lagna (Gemini) → negative [HOUSE-OCC]
- jyotisha: karaka Jupiter: Aquarius (neutral sign), navamsa Taurus → positive [JY-KARAKA]
- western: Mars in whole-sign house 2 (Leo) from Asc Cancer → negative [HOUSE-OCC]
- western: significator Jupiter: Pisces domicile, face, of the sect, stationary → positive [W-SIGNIF]
- bazi: Wealth (Wood) share 0.28 of weighted tally, largest element; weighted-weak DM => 财多身弱 wealth heavy / self light → mixed [BZ-D3]

### D6 Children/creation — STRONG (positive)
Cluster readings: jyotisha positive, western positive, sinic positive
- jyotisha: karaka Jupiter: Aquarius (neutral sign), navamsa Taurus → positive [JY-KARAKA]
- western: significator Jupiter: Pisces domicile, face, of the sect, stationary → positive [W-SIGNIF]
- ziwei: 子女 (children) at 丙子: 天同旺/太阴庙; minors — → positive [ZW-PALACE + ZW-SCORE]

### D9 Fortune/spirituality/worldview — STRONG (positive)
Cluster readings: jyotisha positive, western positive, sinic positive
- jyotisha: Jupiter in house 9 from Lagna (Gemini) → positive [HOUSE-OCC]
- jyotisha: karaka Jupiter: Aquarius (neutral sign), navamsa Taurus → positive [JY-KARAKA]
- western: Jupiter in whole-sign house 9 (Pisces) from Asc Cancer → positive [HOUSE-OCC]
- western: significator Jupiter: Pisces domicile, face, of the sect, stationary → positive [W-SIGNIF]
- ziwei: 福德 (spirit) at 己巳: 紫微旺/七杀平; minors — → positive [ZW-PALACE + ZW-SCORE]

What these mean, stated narrowly:
- **D1 Self/identity:** All three clusters read the self as **carrying weight**: Sun, Mercury and Saturn on the Ascendant in both zodiacs (Saturn in detriment in the Western chart), a weak 辛 Day Master in BaZi, and 天相 in a weak position with 擎羊 in Zi Wei's life palace. The Vedic Bhadra and Budhaditya yogas add a quick, articulate mind.
- **D3 Wealth/gains:** All three read money as **prominent but double-edged**: debilitated Mars in the Vedic 2nd, Mars in the Western 2nd against a dignified Jupiter, and 财多身弱 in BaZi (heavy Wood wealth, weak Day Master).
- **D6 Children/creation:** All three read children and creation **favourably**: Jupiter as significator in both zodiacs (own sign in Pisces in the Western chart) and Zi Wei's children palace with 天同 and 太阴 at full brightness. Symbolic only; nothing about fertility.
- **D9 Fortune/spirituality/worldview:** All three read meaning and fortune **favourably**: Jupiter in the 9th house in both zodiacs (own sign and of the sect in the Western chart) and 紫微 bright in Zi Wei's 福德 palace. This is her clearest supportive signature.
- Prominence is not outcome. None of these says anything will succeed or fail.

## 5. Disagreements (not smoothed over)

- **D2 Career/status:** Zi Wei's career palace is bright (literary stars 文昌/文曲, borrowed 武曲化科) and BaZi has a hidden Seven Killings, both positive under the registry; the Vedic Sun (status significator) reads negative. Western is neutral. The systems genuinely disagree.
- **BaZi Day Master strength:** the weighted count gives support 0.43 → weak; the seasonal rule gives weakened (month drains/controls/is controlled) — they agree. Favourable-element (Yong Shen) confidence: **low**. 调候 Seasonal regulation (Qiong Tong Bao Jian): unavailable. 扶抑 Strength-balancing (rule BZ-DM-1): Earth, Metal.
- **Temperament conflicts:** T2 Drive/initiative (jyotisha strained, western strained, sinic supported).
- **Secondary Vedic view (from the Moon, non-voting):** D1: Moon in house 1 from Chandra Lagna (Moon, Libra) → neutral; D3: Rahu in house 2 from Chandra Lagna (Moon, Libra) → negative; D6: Jupiter in house 5 from Chandra Lagna (Moon, Libra) → positive; D9: Sun, Mercury, Saturn in house 9 from Chandra Lagna (Moon, Libra) → negative; D2: Mars in house 10 from Chandra Lagna (Moon, Libra) → negative.

## 6. Weak areas (do not over-read)

- D4 Partnership: WEAK — jyotisha positive, western neutral, sinic mixed
- D5 Family/roots/home: INSUFFICIENT — jyotisha neutral, western neutral, sinic neutral
- D7 Health/routine: WEAK — jyotisha negative, western neutral, sinic neutral
- D8 Mind/education/craft: WEAK — jyotisha neutral, western neutral, sinic positive
- D7 Health/routine is symbolic prominence only. **Nothing here is a health, medical or lifespan statement.**

## 7. Temperament overlay

- **T1 Leadership/visibility** — 1 clusters: strained: jyotisha strained (Sun score -1.00 (Gemini, neutral sign, with Mercury/Saturn, navamsa Aquarius)); western mixed/neutral (Sun score +0.00 (Cancer, peregrine, of the sect)); sinic mixed/neutral (命宫 major stars ['天相']; visible Officer: False)
- **T2 Drive/initiative** — conflict: jyotisha strained (Mars score -2.00 (Cancer, debilitated, navamsa Sagittarius)); western strained (Mars score -1.50 (Leo, peregrine, contrary to sect)); sinic supported (七杀/破军/贪狼 in 命/身: ['破军']; Seven Killings hidden x1)
- **T3 Nurturing/service** — no clear signal: jyotisha mixed/neutral (Moon score +0.50 (Libra, neutral sign, waxing, navamsa Capricorn)); western mixed/neutral (Moon score -0.25 (Scorpio, fall, triplicity (other/participating), contrary to sect)); sinic mixed/neutral (Resource stem visible: [])
- **T4 Intellect/craft** — no clear signal: jyotisha mixed/neutral (Mercury score -0.50 (Gemini, own sign, with Sun/Saturn, navamsa Aquarius)); western mixed/neutral (Mercury score +0.00 (Cancer, peregrine, contrary to sect)); sinic mixed/neutral (output stem visible []; 文昌/文曲/天机 in 命/身: [])
- **T5 Adaptability** — 1 clusters: supported: jyotisha supported (3 of 7 grahas in dual signs); western mixed/neutral (2 of 7 planets in mutable signs); sinic silent (no declared Sinic rule)
- **T6 Discipline/structure** — 1 clusters: strained: jyotisha mixed/neutral (Saturn score -0.50 (Gemini, friend's sign, with Sun/Mercury, navamsa Aquarius)); western strained (Saturn score -1.50 (Cancer, detriment, of the sect)); sinic mixed/neutral (no Officer star on a visible stem)
- Maya: **2 Chikchan 18 Sotz' / 12.18.0.17.5**, computed and verified. Meaning is omitted — no verifiable named Maya source available in this environment.
- Tibetan: **Male Wood Tiger** year. Meaning is omitted — no validated lineage-specific source; Mewa/Parkha/personal forces not computed.

## 8. Timing

- **Now (2022-02-20 → 2032-02-21): D8 Mind/education/craft — MODERATE.** jyotisha: Vimshottari Mercury Mahadasha; sinic: BaZi Da Yun 乙丑.
  - Current Vimshottari: Mahadasha Mercury (2021-10-25 → 2038-10-25) / Antardasha Venus (2025-03-20 → 2028-01-19). Dates move by about ±44 days across ±10 min.
  - Why D8 is active: the Vedic Mercury Mahadasha (Mercury is the intellect karaka and her Lagna lord, sitting in the 1st) overlaps the BaZi 乙丑 luck pillar, whose branch main qi is Indirect Resource (learning).
  - BaZi year 丙午 (Lichun 2026 → Lichun 2027): stem 正官 Direct Officer, branch 七杀 Seven Killings. Activation is not outcome.
- Next: 2032-02-21 → 2032-12-31: D8 Mind/education/craft — MODERATE (jyotisha: Vimshottari Mercury Mahadasha; sinic: BaZi Da Yun 甲子)
- Zi Wei decadal (not a convergence by itself): 46-55 (财帛 亥) ≈2019–2029; then 56-65 (疾厄 戌) ≈2029–2039.

## 9. Claims removed

- sensitive_to_birth_time: 0 — projections that change inside the uncertainty interval; displayed, never vote
- secondary_reference_frame_not_voting: 5 — Jyotisha houses from Chandra Lagna (JY-REFERENCE)
- neutral_polarity_no_theme: 17
- school_dependent_low_confidence: 1
- no_validated_source: 4
- unavailable_methods: 6
- barnum_screen: every retained projection is tied to a computed datum via a registry rule; no automated Barnum test was run, so generic-sounding prose was avoided by hand in FINAL_READING.md

## Closing frame

These results show where several traditional symbolic systems, each computed under declared conventions and checked against independent engines, happen to agree or disagree. The domain rules and weights are declared in `SYNTHESIS.json` → `registry`, and different reasonable rules would give different grades. Nothing here is a validated forecast, a fate, or a basis for medical, financial or legal decisions.
