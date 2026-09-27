# Six-culture chart reading

*This shows where several traditional symbolic systems agree or disagree, not a validated forecast. None of it is scientific evidence about your character or your future.*

## 1. Input and sensitivity

- Born **Wednesday 2004-06-23, 13:00 IST (UTC+05:30, no DST)** = 2004-06-23 07:30 UTC, Vashi, Navi Mumbai, Maharashtra, India (19.0632°N, 72.9988°E; OpenStreetMap Nominatim).
- Local mean time 12:21:59; local apparent solar time 12:19:45. Sunrise 06:02, sunset 19:18.
- Time uncertainty: approximate time, stated as plus or minus one hour; outer envelope +/-60 min is primary, +/-30 min is the inner scenario. Modelled as **±60 min** (inner scenario ±30 min). **Outputs that change inside it:** western_asc_sign (Virgo→Libra at -29.1 min); western_mc_sign (Gemini→Cancer at -29.1 min); jyotisha_lagna_sign (Leo→Virgo at -54.7 min); jyotisha_lagna_d9 (Sagittarius→Capricorn at -54.7 min, Capricorn→Aquarius at -40.7 min, Aquarius→Pisces at -26.7 min, Pisces→Aries at -12.6 min, Aries→Taurus at +1.4 min, Taurus→Gemini at +15.5 min, Gemini→Cancer at +29.6 min, Cancer→Leo at +43.7 min, Leo→Virgo at +57.9 min); jyotisha_lagna_d10 (Taurus→Gemini at -42.1 min, Gemini→Cancer at -29.5 min, Cancer→Leo at -16.9 min, Leo→Virgo at -4.2 min, Virgo→Libra at +8.4 min, Libra→Scorpio at +21.1 min, Scorpio→Sagittarius at +33.8 min, Sagittarius→Capricorn at +46.5 min, Capricorn→Aquarius at +59.3 min); jyotisha_lagna_nakshatra_pada (Uttara Phalguni-1→Uttara Phalguni-2 at -54.7 min, Uttara Phalguni-2→Uttara Phalguni-3 at -40.7 min, Uttara Phalguni-3→Uttara Phalguni-4 at -26.7 min, Uttara Phalguni-4→Hasta-1 at -12.6 min, Hasta-1→Hasta-2 at +1.4 min, Hasta-2→Hasta-3 at +15.5 min, Hasta-3→Hasta-4 at +29.6 min, Hasta-4→Chitra-1 at +43.7 min, Chitra-1→Chitra-2 at +57.9 min); moon_d10 (Libra→Scorpio at +18.1 min); bazi_hour_civil (戊午→己未 at +0.0 min); bazi_hour_LAT (戊午→己未 at +40.2 min); ziwei_time_branch_civil (午→未 at +0.0 min); ziwei_time_branch_LAT (午→未 at +40.2 min); western_lot_fortune_sign (Scorpio→Sagittarius at -30.6 min).
- Nearest boundaries: Vedic Lagna Virgo 13.00° (≈54.8 min after / ≈71.7 min before a cusp); Western Ascendant Libra 6.92° (≈29.2 / ≈97.3 min); Chinese double-hour boundary ≈0.0 min away (civil track).
- Coordinates: OpenStreetMap Nominatim, way 151768155 'Vashi' (Vashi station area; hospital not given, so a few km of positional uncertainty). A different hospital in the same town shifts the Ascendant by roughly 0.1°.
- Houses are counted from the **Moon (Chandra Lagna), because the Lagna sign is not stable** (Jyotisha); Western houses do not vote, because the Ascendant sign is not stable. Zi Wei uses the **未** hour but does not vote (hour uncertain); BaZi hour pillar uncertain, so only hour-independent BaZi facts vote. (Rules JY-REFERENCE, W-HOUSES, HOUR-STABILITY.)

## 2. Verification

- Swiss Ephemeris vs NASA JPL DE440s (via Skyfield): the largest planetary difference is **6.4e-05°** (alert threshold 0.01°). The Ascendant/MC agree to within 0.002°.
- Chinese solar terms (芒种, 小暑): four engines agree to ≤1.6 s. Four Pillars: lunar_python = sxtwl (an independent codebase): **甲申 庚午 癸酉 己未**.
- Zi Wei: canonical iztro 2.6.1 matches the py-iztro wrapper. These are the **same method**, so the match is an interface check only. All structural invariants pass.
- Maya: convertdate and a separate implementation agree; the date round-trips exactly.
- **Invariant failures: 0.**
- Unavailable: shadbala, ashtakavarga, pratyantardasha, D7_D12, zodiacal_releasing, transits. Also unavailable: Tibetan Mewa/Parkha/personal forces, and Maya/Tibetan symbolic meanings (no verifiable source).

## 3. Divergence rate (read this before the themes)

- **1/9 domains divergent** (1/8 of domains with enough evidence). Grade counts: STRONG 0, MODERATE 3, WEAK 4, DIVERGENT 1, INSUFFICIENT 1.

- **D8 Mind/education/craft — DIVERGENT:** jyotisha: Ketu in house 3 from Chandra Lagna (Moon, Leo) → negative; bazi: Output stars: Hurting Officer visible in year, Eating God visible in none, output hidden x1; Resource visible: True → positive

## 4. Cross-cultural themes (STRONG first, then MODERATE)

*No domain reaches STRONG (all three clusters agreeing).*

### D2 Career/status — MODERATE (mixed)
Cluster readings: jyotisha mixed, western neutral, sinic mixed
- jyotisha: Venus in house 10 from Chandra Lagna (Moon, Leo) → positive [HOUSE-OCC]
- jyotisha: karaka Sun: Gemini (neutral sign), navamsa Sagittarius → negative [JY-KARAKA]
- bazi: Officer visible in hour pillar(s); Seven Killings hidden x2; 伤官见官: Hurting Officer visible in year → mixed [BZ-D2]

### D3 Wealth/gains — MODERATE (mixed)
Cluster readings: jyotisha mixed, western neutral, sinic mixed
- jyotisha: Sun, Mercury, Saturn in house 11 from Chandra Lagna (Moon, Leo) → negative [HOUSE-OCC]
- jyotisha: karaka Jupiter: Leo (friend's sign), navamsa Virgo → positive [JY-KARAKA]
- bazi: Wealth (Fire) share 0.24 of weighted tally; weighted-weak DM => 财多身弱 wealth heavy / self light → mixed [BZ-D3]

### D6 Children/creation — MODERATE (positive)
Cluster readings: jyotisha positive, western neutral, sinic positive
- jyotisha: karaka Jupiter: Leo (friend's sign), navamsa Virgo → positive [JY-KARAKA]
- bazi: children palace = hour pillar 己未 with 七杀 Seven Killings on the stem; children star (Eating God/Hurting Officer) visible in year → positive [BZ-D6]

What these mean, stated narrowly:
- **D2 Career/status:** Vedic (Venus in its own sign in the 10th from the Moon, against a weak Sun) and BaZi (伤官见官 under either hour) agree that work is **prominent and comes with friction**, especially around authority.
- **D3 Wealth/gains:** Vedic (Sun, Mercury and Saturn crowd the 11th from the Moon, against a strong Jupiter) and BaZi (财多身弱: weak water Day Master with plenty of Fire wealth) agree that money and gains are **prominent but double-edged**.
- **D6 Children/creation:** Vedic (Jupiter in a friendly sign) and BaZi (the Hurting Officer, a woman's children and creation star, visible under either hour) read children and creation **favourably**. Symbolic only.
- Prominence is not outcome. None of these says anything will succeed or fail.

## 5. Disagreements (not smoothed over)

- **D8 Mind/education/craft:** BaZi reads mind and craft as positive (Hurting Officer and Direct Resource visible). Vedic reads it as negative (Ketu in the 3rd from the Moon). Western is neutral. The systems genuinely disagree.
- **BaZi Day Master strength:** the weighted count gives support 0.33 → weak; the seasonal rule gives weakened (month drains/controls/is controlled) — they agree. Favourable-element (Yong Shen) confidence: **low**. 调候 Seasonal regulation (Qiong Tong Bao Jian): unavailable. 扶抑 Strength-balancing (rule BZ-DM-1): Metal, Water.
- **Temperament conflicts:** .
- **Secondary Vedic view (from the Lagna, non-voting):** D3: Ketu in house 2 from Lagna (Virgo) → negative; D9: Venus in house 9 from Lagna (Virgo) → positive; D2: Sun, Mercury, Saturn in house 10 from Lagna (Virgo) → negative; D3: Mars in house 11 from Lagna (Virgo) → negative.

## 6. Weak areas (do not over-read)

- D1 Self/identity: WEAK — jyotisha mixed, western neutral, sinic negative
- D4 Partnership: WEAK — jyotisha positive, western neutral, sinic silent
- D5 Family/roots/home: WEAK — jyotisha neutral, western neutral, sinic positive
- D7 Health/routine: INSUFFICIENT — jyotisha silent, western neutral, sinic silent
- D9 Fortune/spirituality/worldview: WEAK — jyotisha mixed, western neutral, sinic silent
- D7 Health/routine is symbolic prominence only. **Nothing here is a health, medical or lifespan statement.**

## 7. Temperament overlay

- **T1 Leadership/visibility** — 1 clusters: strained: jyotisha strained (Sun score -1.00 (Gemini, neutral sign, with Mercury/Saturn, navamsa Sagittarius)); western mixed/neutral (Sun score +0.00 (Cancer, peregrine, of the sect)); sinic sensitive (未 hour: mixed/neutral (命宫 major stars ['太阳']; visible Officer: False); 午 hour: supported (命宫 major stars ['武曲', '天府']; visible Officer: True))
- **T2 Drive/initiative** — 2 clusters: strained: jyotisha strained (Mars score -2.00 (Cancer, debilitated, navamsa Leo)); western strained (Mars score -2.25 (Cancer, fall, triplicity (other/participating), contrary to sect)); sinic mixed/neutral (七杀/破军/贪狼 in 命/身: []; Seven Killings hidden x2)
- **T3 Nurturing/service** — 1 clusters: supported: jyotisha mixed/neutral (Moon score +0.00 (Leo, friend's sign, waxing, with Jupiter, navamsa Gemini)); western mixed/neutral (Moon score +0.75 (Virgo, triplicity (other/participating), contrary to sect)); sinic supported (Resource stem visible: ['正印 Direct Resource'])
- **T4 Intellect/craft** — 1 clusters: supported: jyotisha mixed/neutral (Mercury score -0.50 (Gemini, own sign, with Sun/Saturn, navamsa Aquarius)); western mixed/neutral (Mercury score +0.00 (Cancer, peregrine, contrary to sect)); sinic supported (output stem visible ['伤官 Hurting Officer']; 文昌/文曲/天机 in 命/身: ['天机', '文曲'])
- **T5 Adaptability** — 2 clusters: supported: jyotisha supported (3 of 7 grahas in dual signs); western supported (3 of 7 planets in mutable signs); sinic silent (no declared Sinic rule)
- **T6 Discipline/structure** — 2 clusters: strained: jyotisha strained (Saturn score -1.50 (Gemini, friend's sign, with Sun/Mercury, navamsa Aries)); western strained (Saturn score -1.50 (Cancer, detriment, of the sect)); sinic mixed/neutral (Officer star visible but confronted by a visible Hurting Officer (伤官见官))
- Maya: **8 Kab'an 0 Sek / 12.19.11.6.17**, computed and verified. Meaning is omitted — no verifiable named Maya source available in this environment.
- Tibetan: **Male Wood Monkey** year. Meaning is omitted — no validated lineage-specific source; Mewa/Parkha/personal forces not computed.

## 8. Timing

- No moderate or strong convergence is active today.
  - Current Vimshottari: Mahadasha Venus (2006-11-01 → 2026-11-01) / Antardasha Ketu (2025-09-01 → 2026-11-01). Dates move by about ±100 days across ±60 min.
  - BaZi year 丙午 (Lichun 2026 → Lichun 2027): stem 正财 Direct Wealth, branch 偏财 Indirect Wealth. Activation is not outcome.
- Next: 2027-02-08 → 2030-06-19: D2 Career/status — MODERATE (jyotisha: Vimshottari Sun Mahadasha; sinic: BaZi Da Yun 戊辰)
- Next: 2027-02-08 → 2027-06-23: D3 Wealth/gains — MODERATE (jyotisha: Vimshottari Sun Mahadasha; western: annual profection age 22)
- Next: 2028-06-23 → 2029-06-23: D1 Self/identity — MODERATE (jyotisha: Vimshottari Sun Mahadasha; western: annual profection age 24)
- Next: 2030-06-19 → 2032-07-24: D3 Wealth/gains — MODERATE (jyotisha: Vimshottari Sun Mahadasha; sinic: BaZi Da Yun 丁卯)
- Zi Wei decadal (not a convergence by itself): .

## 9. Claims removed

- sensitive_to_birth_time: 38 — projections that change inside the uncertainty interval; displayed, never vote
- secondary_reference_frame_not_voting: 4 — Jyotisha houses from Lagna (JY-REFERENCE)
- neutral_polarity_no_theme: 12
- school_dependent_low_confidence: 1
- no_validated_source: 4
- unavailable_methods: 6
- barnum_screen: every retained projection is tied to a computed datum via a registry rule; no automated Barnum test was run, so generic-sounding prose was avoided by hand in FINAL_READING.md

## Closing frame

These results show where several traditional symbolic systems, each computed under declared conventions and checked against independent engines, happen to agree or disagree. The domain rules and weights are declared in `SYNTHESIS.json` → `registry`, and different reasonable rules would give different grades. Nothing here is a validated forecast, a fate, or a basis for medical, financial or legal decisions.
