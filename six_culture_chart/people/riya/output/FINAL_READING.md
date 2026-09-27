# Six-culture chart reading

*This shows where several traditional symbolic systems agree or disagree, not a validated forecast. None of it is scientific evidence about your character or your future.*

## 1. Input and sensitivity

- Born **Wednesday 2004-06-23, 13:05 IST (UTC+05:30, no DST)** = 2004-06-23 07:35 UTC, Vashi, Navi Mumbai, Maharashtra, India (19.0632°N, 72.9988°E; OpenStreetMap Nominatim).
- Local mean time 12:26:59; local apparent solar time 12:24:45. Sunrise 06:02, sunset 19:18.
- Time uncertainty: ASSUMED time chosen by the user (13:05, 'or so'), not a recorded time; modelled as +/-5 min. The underlying record is only 1 PM +/- 1 hour. Modelled as **±5 min**. **Outputs that change inside it:** jyotisha_lagna_d9 (Aries→Taurus at -3.6 min); jyotisha_lagna_d10 (Virgo→Libra at +3.4 min); jyotisha_lagna_nakshatra_pada (Hasta-1→Hasta-2 at -3.6 min).
- Nearest boundaries: Vedic Lagna Virgo 14.19° (≈59.8 min after / ≈66.7 min before a cusp); Western Ascendant Libra 8.11° (≈34.2 / ≈92.3 min); Chinese double-hour boundary ≈5.0 min away (civil track).
- Coordinates: OpenStreetMap Nominatim, way 151768155 'Vashi' (Vashi station area; hospital not given, so a few km of positional uncertainty). A different hospital in the same town shifts the Ascendant by roughly 0.1°.
- Houses are counted from the **Lagna** (Jyotisha); Western houses vote. Zi Wei uses the **未** hour; BaZi hour pillar stable. (Rules JY-REFERENCE, W-HOUSES, HOUR-STABILITY.)

## 2. Verification

- Swiss Ephemeris vs NASA JPL DE440s (via Skyfield): the largest planetary difference is **6.4e-05°** (alert threshold 0.01°). The Ascendant/MC agree to within 0.002°.
- Chinese solar terms (芒种, 小暑): four engines agree to ≤1.6 s. Four Pillars: lunar_python = sxtwl (an independent codebase): **甲申 庚午 癸酉 己未**.
- Zi Wei: canonical iztro 2.6.1 matches the py-iztro wrapper. These are the **same method**, so the match is an interface check only. All structural invariants pass.
- Maya: convertdate and a separate implementation agree; the date round-trips exactly.
- **Invariant failures: 0.**
- Unavailable: shadbala, ashtakavarga, D7_D12, zodiacal_releasing, transits. Also unavailable: Tibetan Mewa/Parkha/personal forces, and Maya/Tibetan symbolic meanings (no verifiable source).

## 3. Divergence rate (read this before the themes)

- **1/9 domains divergent** (1/9 of domains with enough evidence). Grade counts: STRONG 0, MODERATE 4, WEAK 4, DIVERGENT 1, INSUFFICIENT 0.

- **D9 Fortune/spirituality/worldview — DIVERGENT:** jyotisha: Venus in house 9 from Lagna (Virgo) → positive; jyotisha: karaka Jupiter: Leo (friend's sign), navamsa Virgo → positive; ziwei: 福德 (spirit) at 丁丑: 天机陷; minors 天魁/陀罗 [身宫 body palace] → negative

## 4. Cross-cultural themes (STRONG first, then MODERATE)

*No domain reaches STRONG (all three clusters agreeing).*

### D1 Self/identity — MODERATE (negative)
Cluster readings: jyotisha negative, western neutral, sinic negative
- jyotisha: karaka Sun: Gemini (neutral sign), navamsa Sagittarius → negative [JY-KARAKA]
- bazi: Day Master 癸 (Yin Water): weighted support 0.33 (weak) vs seasonal weakened (month drains/controls/is controlled); rooted in year → negative [BZ-D1]
- ziwei: 命宫 (soul) at 乙亥: 太阳陷化忌; minors 文曲 → negative [ZW-PALACE + ZW-SCORE]

### D2 Career/status — MODERATE (negative)
Cluster readings: jyotisha negative, western negative, sinic mixed
- jyotisha: Sun, Mercury, Saturn in house 10 from Lagna (Virgo) → negative [HOUSE-OCC]
- jyotisha: karaka Sun: Gemini (neutral sign), navamsa Sagittarius → negative [JY-KARAKA]
- western: Sun, Mercury, Mars, Saturn in whole-sign house 10 (Cancer) from Asc Libra → negative [HOUSE-OCC]
- bazi: Officer visible in hour pillar(s); Seven Killings hidden x2; 伤官见官: Hurting Officer visible in year → mixed [BZ-D2]
- ziwei: 官禄 (career) at 丁卯: 太阴陷; minors 文昌/擎羊 → negative [ZW-PALACE + ZW-SCORE]

### D3 Wealth/gains — MODERATE (mixed)
Cluster readings: jyotisha mixed, western neutral, sinic mixed
- jyotisha: Ketu in house 2 from Lagna (Virgo) → negative [HOUSE-OCC]
- jyotisha: Mars in house 11 from Lagna (Virgo) → negative [HOUSE-OCC]
- jyotisha: karaka Jupiter: Leo (friend's sign), navamsa Virgo → positive [JY-KARAKA]
- bazi: Wealth (Fire) share 0.24 of weighted tally; weighted-weak DM => 财多身弱 wealth heavy / self light → mixed [BZ-D3]
- ziwei: 财帛 (wealth) at 辛未: 天梁旺; minors 天钺 → positive [ZW-PALACE + ZW-SCORE]

### D6 Children/creation — MODERATE (positive)
Cluster readings: jyotisha positive, western neutral, sinic positive
- jyotisha: karaka Jupiter: Leo (friend's sign), navamsa Virgo → positive [JY-KARAKA]
- bazi: children palace = hour pillar 己未 with 七杀 Seven Killings on the stem; children star (Eating God/Hurting Officer) visible in year → positive [BZ-D6]
- ziwei: 子女 (children) at 壬申: 七杀庙; minors 左辅 → positive [ZW-PALACE + ZW-SCORE]

What these mean, stated narrowly:
- **D1 Self/identity:** Vedic (the Sun, significator of self, weak in Gemini) and Sinic (weak 癸 Day Master; Zi Wei life palace 太阳 dim and turning to 化忌) agree the self reads as **under pressure**: confidence that has to be built.
- **D2 Career/status:** Vedic (Sun, Mercury and Saturn in the 10th) and Western (Sun, Mercury, Mars and Saturn in the 10th) agree that career is **the most prominent and most pressured** area of her chart. The Vedic Bhadra yoga (Mercury in its own sign in the 10th) is the counterweight.
- **D3 Wealth/gains:** Vedic (Ketu in the 2nd, debilitated Mars in the 11th, against a strong Jupiter) and Sinic (财多身弱 in BaZi against a bright 天梁 wealth palace) agree that money is **active but double-edged**.
- **D6 Children/creation:** Vedic (Jupiter in a friendly sign) and Sinic (visible Hurting Officer; Zi Wei children palace 七杀 at full strength) read children and creation **favourably**. Symbolic only.
- Prominence is not outcome. None of these says anything will succeed or fail.

## 5. Disagreements (not smoothed over)

- **D9 Fortune/spirituality/worldview:** Vedic reads meaning and fortune favourably (Venus in its own sign in the 9th, strong Jupiter); Zi Wei reads it unfavourably (dim 天机 in 福德). Western is neutral. The systems genuinely disagree.
- **BaZi Day Master strength:** the weighted count gives support 0.33 → weak; the seasonal rule gives weakened (month drains/controls/is controlled) — they agree. Favourable-element (Yong Shen) confidence: **low**. 调候 Seasonal regulation (Qiong Tong Bao Jian): unavailable. 扶抑 Strength-balancing (rule BZ-DM-1): Metal, Water.
- **Temperament conflicts:** .
- **Secondary Vedic view (from the Moon, non-voting):** D1: Moon, Jupiter in house 1 from Chandra Lagna (Moon, Leo) → positive; D8: Ketu in house 3 from Chandra Lagna (Moon, Leo) → negative; D9: Rahu in house 9 from Chandra Lagna (Moon, Leo) → negative; D2: Venus in house 10 from Chandra Lagna (Moon, Leo) → positive; D3: Sun, Mercury, Saturn in house 11 from Chandra Lagna (Moon, Leo) → negative.

## 6. Weak areas (do not over-read)

- D4 Partnership: WEAK — jyotisha positive, western neutral, sinic neutral
- D5 Family/roots/home: WEAK — jyotisha neutral, western neutral, sinic positive
- D7 Health/routine: WEAK — jyotisha silent, western neutral, sinic positive
- D8 Mind/education/craft: WEAK — jyotisha neutral, western neutral, sinic positive
- D7 Health/routine is symbolic prominence only. **Nothing here is a health, medical or lifespan statement.**

## 7. Temperament overlay

- **T1 Leadership/visibility** — 1 clusters: strained: jyotisha strained (Sun score -1.00 (Gemini, neutral sign, with Mercury/Saturn, navamsa Sagittarius)); western mixed/neutral (Sun score +0.00 (Cancer, peregrine, of the sect)); sinic mixed/neutral (命宫 major stars ['太阳']; visible Officer: False)
- **T2 Drive/initiative** — 2 clusters: strained: jyotisha strained (Mars score -2.00 (Cancer, debilitated, navamsa Leo)); western strained (Mars score -2.25 (Cancer, fall, triplicity (other/participating), contrary to sect)); sinic mixed/neutral (七杀/破军/贪狼 in 命/身: []; Seven Killings hidden x2)
- **T3 Nurturing/service** — 1 clusters: supported: jyotisha mixed/neutral (Moon score +0.00 (Leo, friend's sign, waxing, with Jupiter, navamsa Gemini)); western mixed/neutral (Moon score +0.75 (Virgo, triplicity (other/participating), contrary to sect)); sinic supported (Resource stem visible: ['正印 Direct Resource'])
- **T4 Intellect/craft** — 1 clusters: supported: jyotisha mixed/neutral (Mercury score -0.50 (Gemini, own sign, with Sun/Saturn, navamsa Aquarius)); western mixed/neutral (Mercury score +0.00 (Cancer, peregrine, contrary to sect)); sinic supported (output stem visible ['伤官 Hurting Officer']; 文昌/文曲/天机 in 命/身: ['天机', '文曲'])
- **T5 Adaptability** — 2 clusters: supported: jyotisha supported (3 of 7 grahas in dual signs); western supported (3 of 7 planets in mutable signs); sinic silent (no declared Sinic rule)
- **T6 Discipline/structure** — 2 clusters: strained: jyotisha strained (Saturn score -1.50 (Gemini, friend's sign, with Sun/Mercury, navamsa Aries)); western strained (Saturn score -1.50 (Cancer, detriment, of the sect)); sinic mixed/neutral (Officer star visible but confronted by a visible Hurting Officer (伤官见官))
- Maya: **8 Kab'an 0 Sek / 12.19.11.6.17**, computed and verified. Meaning is omitted — no verifiable named Maya source available in this environment.
- Tibetan: **Male Wood Monkey** year. Meaning is omitted — no validated lineage-specific source; Mewa/Parkha/personal forces not computed.

## 8. Timing

- **Now (2021-01-01 → 2026-10-15): D4 Partnership — MODERATE.** jyotisha: Vimshottari Venus Mahadasha; sinic: BaZi Da Yun 戊辰.
  - Current Vimshottari: Mahadasha Venus (2006-10-24 → 2026-10-24) / Antardasha Ketu (2025-08-23 → 2026-10-24) / Pratyantardasha Mercury (2026-08-24 → 2026-10-24). Dates move by about ±8 days across ±5 min.
  - Why D4 is active: the Vedic Venus period (love significator, in its own sign) overlaps BaZi's 戊辰 pillar, whose Officer stars stand for the partner in a woman's chart. The Venus period ends in October 2026.
  - BaZi year 丙午 (Lichun 2026 → Lichun 2027): stem 正财 Direct Wealth, branch 偏财 Indirect Wealth. Activation is not outcome.
- Next: 2026-11-01 → 2030-06-19: D2 Career/status — MODERATE (jyotisha: Vimshottari Sun Mahadasha; sinic: BaZi Da Yun 戊辰)
- Next: 2028-06-23 → 2029-06-23: D1 Self/identity — MODERATE (jyotisha: Vimshottari Sun Mahadasha; western: annual profection age 24)
- Next: 2032-10-31 → 2032-12-31: D8 Mind/education/craft — MODERATE (jyotisha: Vimshottari Moon Mahadasha; sinic: BaZi Da Yun 丁卯)
- Zi Wei decadal (not a convergence by itself): 16-25 (兄弟 戌) ≈2019–2029; then 26-35 (夫妻 酉) ≈2029–2039.

## 9. Claims removed

- sensitive_to_birth_time: 0 — projections that change inside the uncertainty interval; displayed, never vote
- secondary_reference_frame_not_voting: 5 — Jyotisha houses from Chandra Lagna (JY-REFERENCE)
- neutral_polarity_no_theme: 15
- school_dependent_low_confidence: 1
- no_validated_source: 4
- unavailable_methods: 5
- barnum_screen: every retained projection is tied to a computed datum via a registry rule; no automated Barnum test was run, so generic-sounding prose was avoided by hand in FINAL_READING.md

## Closing frame

These results show where several traditional symbolic systems, each computed under declared conventions and checked against independent engines, happen to agree or disagree. The domain rules and weights are declared in `SYNTHESIS.json` → `registry`, and different reasonable rules would give different grades. Nothing here is a validated forecast, a fate, or a basis for medical, financial or legal decisions.
