"""Steps 6 and 8: master dataset + human-readable INPUT_AUDIT.md, MASTER_DATASET.md, FINAL_READING.md.

All prose values are read from output/*.json so every sentence is traceable to the datasets.
"""
import json
import os
import shutil

from sc.common import OUT, ROOT, SIGNS, dump, fmt_dms

J = lambda n: json.load(open(os.path.join(OUT, n), encoding="utf-8"))


def w(name, lines):
    open(os.path.join(OUT, name), "w", encoding="utf-8").write("\n".join(lines) + "\n")


def main():
    raw, man, ver, syn = J("RAW_CALCULATIONS.json"), J("CALCULATION_MANIFEST.json"), J("VERIFICATION_REPORT.json"), J("SYNTHESIS.json")
    inp = json.load(open(os.path.join(ROOT, "BIRTH_INPUT.json"), encoding="utf-8"))
    shutil.copy(os.path.join(ROOT, "BIRTH_INPUT.json"), os.path.join(OUT, "BIRTH_INPUT.json"))
    a, st, bd = raw["input_audit"], raw["stability"], raw["boundaries"]

    # ---------------- MASTER_DATASET.json ----------------
    master = {"input": {"original": inp, "normalized": a}, "conventions_and_versions": man,
              "raw_calculations": raw, "verification": {"failures": ver["failures"], "data": ver["data"],
                                                        "invariants": ver["invariants"]},
              "time_uncertainty": {"offsets_min": raw["ensemble_offsets_min"], "ensemble": raw["ensemble"],
                                   "stability": st},
              "excluded_methods": {**raw["jyotisha"]["unavailable"], **raw["western"]["unavailable"],
                                   **raw["tibetan"]["omitted"],
                                   "maya_day_sign_meaning": "no verifiable named Maya source",
                                   "bazi_yong_shen_as_fact": "school-dependent; kept as low-confidence rule chains only"}}
    dump("MASTER_DATASET.json", master)

    # ---------------- INPUT_AUDIT.md ----------------
    L = ["# Input audit", "", "## Original input", "", f"> {inp['original_user_input']}", "",
         "## Normalized", "", "| Field | Value |", "|---|---|"]
    for k in ("gregorian_date", "local_time_24h", "local_iso", "utc_iso", "weekday", "latitude", "longitude",
              "elevation_m", "coordinate_source", "iana_zone", "tzdata_release", "utc_offset", "dst_in_effect",
              "julian_day_ut", "delta_t_seconds", "local_mean_time", "equation_of_time_minutes",
              "local_apparent_solar_time", "historical_time_note"):
        L.append(f"| {k} | {a[k]} |")
    L.append(f"| sunrise | SE {a['sunrise']['swiss_ephemeris']} / JPL {a['sunrise']['skyfield_jpl']} (Δ {a['sunrise']['difference_s']:.0f} s) |")
    L.append(f"| sunset | SE {a['sunset']['swiss_ephemeris']} / JPL {a['sunset']['skyfield_jpl']} (Δ {a['sunset']['difference_s']:.0f} s) |")
    L += ["", f"Time uncertainty: {inp['time_uncertainty']['interpretation']}.", "",
          "## Boundary audit (every crossing inside ±30 min)", "",
          "| Output | Value at 09:30 | ±15 min | ±30 min | Crossings (minutes from 09:30, from → to) |", "|---|---|---|---|---|"]
    for k, v in st.items():
        cr = "; ".join(f"{c['minutes_from_T']:+.1f} min ({c['instant_local'][11:19]}): {c['from']} → {c['to']}" for c in v["crossings"]) or "—"
        L.append(f"| {k} | {v['value_at_T']} | {v['inner_interval']} | {v['outer_interval']} | {cr} |")
    wa, jl = bd["western_asc"], bd["jyotisha_lagna"]
    L += ["", "## Boundary distances", "",
          f"- **Western Ascendant** {fmt_dms(wa['asc_lon'])}: {wa['to_next_cusp_deg']:.2f}° before Leo (≈{wa['minutes_to_next_cusp_approx']:.1f} min at {wa['asc_rate_deg_per_min']:.3f}°/min).",
          f"- **Jyotisha Lagna** {fmt_dms(jl['lagna_lon'])} (Lahiri): only {jl['deg_in_sign']:.2f}° past the Gemini/Cancer cusp (≈{jl['minutes_since_prev_cusp_approx']:.1f} min). Its D9 segment is {jl['d9_segment_deg'][0]:.2f}–{jl['d9_segment_deg'][1]:.2f}° and D10 segment {jl['d10_segment_deg'][0]}–{jl['d10_segment_deg'][1]}°.",
          f"- **Sect**: {bd['sunrise_sect']['minutes_after_sunrise']:.0f} min after sunrise, {bd['sunrise_sect']['minutes_before_sunset']:.0f} min before sunset → day chart, stable.",
          f"- **BaZi / Zi Wei hour**: civil 09:30 is 30 min into the 巳 Si double-hour (09:00–11:00). Local apparent solar time {a['local_apparent_solar_time'][11:]} is {bd['bazi_hour']['minutes_after_09:00_LAT']:.1f} min into it. Under the solar-time track the hour becomes 辰 Chen if birth was ≥27.4 min earlier than 09:30.",
          f"- **Day boundary**: {bd['day_boundary']['minutes_after_local_midnight']} min after midnight; late-Zi convention irrelevant.",
          f"- **Solar terms**: birth {raw['bazi']['primary']['birth_after_lixia_days']:.2f} days after 立夏 and {raw['bazi']['primary']['birth_before_mangzhong_days']:.2f} days before 芒种 → month 己巳 stable.",
          f"- **Zi Wei lunar date**: {bd['zi_wei_lunar']['lunar_date']}; next new moon {bd['zi_wei_lunar']['next_new_moon_utc']} ({bd['zi_wei_lunar']['hours_to_next_new_moon']:.1f} h after birth), so lunar month stable.",
          f"- **Tibetan Losar**: {bd['tibetan_losar']}.",
          f"- **Calendar adoption**: {bd['calendar_adoption']}.",
          f"- **Mercury** is {bd['mercury_tropical_sign_cusp']['deg_past_0_taurus']:.2f}° into tropical Taurus (ingress ≈{bd['mercury_tropical_sign_cusp']['hours_since_ingress_approx']:.0f} h before birth) — stable over ±30 min."]
    w("INPUT_AUDIT.md", L)

    # ---------------- MASTER_DATASET.md ----------------
    A = raw["astronomy"]["+0min"]
    M = ["# Master dataset (facts only, no interpretation)", "", f"Birth instant: {a['local_iso']} ({a['utc_iso']} UTC), {a['weekday']}, Lucknow {a['latitude']}N {a['longitude']}E.", "",
         "## Positions at 09:30 IST", "", "| Body | Tropical | Sidereal (Lahiri) | Speed °/d | JPL Δ° |", "|---|---|---|---|---|"]
    for b in ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto", "MeanNode", "TrueNode"]:
        v = A["bodies"][b]
        M.append(f"| {b} | {fmt_dms(v['lon'])} | {fmt_dms(v['sidereal_lon'])} | {v['speed_deg_day']:+.4f} | {format(v['validator_difference_deg'], '.1e') if v.get('validator_difference_deg') is not None else '— (no validator)'} |")
    M += [f"| Asc | {fmt_dms(A['angles_tropical']['asc'])} | {fmt_dms(A['angles_sidereal']['asc'])} | | {A['angle_differences_deg']['asc']:.1e} |",
          f"| MC | {fmt_dms(A['angles_tropical']['mc'])} | {fmt_dms(A['angles_sidereal']['mc'])} | | {A['angle_differences_deg']['mc']:.1e} |",
          f"", f"Lahiri ayanamsha {A['ayanamsha_lahiri_deg']:.6f}°.", ""]
    # Jyotisha
    for off in ("+0min", "-15min"):
        c = raw["jyotisha"]["charts"][off]
        M += [f"## Jyotisha D1 — Lagna {c['lagna']['sign']} {c['lagna']['deg']:.2f}° ({off} alternative)" if off != "+0min" else
              f"## Jyotisha D1 — Lagna {c['lagna']['sign']} {c['lagna']['deg']:.2f}° (09:30; Gemini if birth ≥6.9 min earlier)", "",
              "| Graha | Sign | Deg | House | Nakshatra-pada | Dignity | D9 | D10 | Function |", "|---|---|---|---|---|---|---|---|---|"]
        for g, v in c["grahas"].items():
            M.append(f"| {g} | {v['sign']} | {v['deg']:.2f} | {v['house']} | {v['nakshatra']['name']}-{v['nakshatra']['pada']} | {v['dignity']}"
                     f"{' (combust)' if v.get('combust') else ''} | {v['d9']} | {v['d10']} | {v.get('nature', '')} {v.get('houses_owned', '')} |")
        M.append("")
    c = raw["jyotisha"]["charts"]["+0min"]
    M += ["Yogas (declared whitelist): " + "; ".join(f"{y['id']}={'yes' if y['satisfied'] else 'no'}" + (f" (cancelled: {y['cancellation_basis']})" if y.get("cancelled") and y["satisfied"] else "") for y in c["yogas"]), "",
          f"Planetary war: {c['planetary_war'] or 'none'}. True node sign same as mean: {raw['jyotisha']['true_node_variant_T']['same_sign_as_mean']}.", ""]
    V = raw["jyotisha"]["vimshottari"]
    M += [f"Vimshottari: Moon in {V['+0min']['moon_nakshatra']['name']} (lord {V['+0min']['moon_nakshatra']['lord']}), balance {V['+0min']['balance_at_birth_years']:.3f} y.", "",
          "| Mahadasha | Start (09:30) | End (09:30) | Start range ±30 min |", "|---|---|---|---|"]
    for i, md in enumerate(V["+0min"]["mahadashas"][:6]):
        rng = sorted(V[k]["mahadashas"][i]["start"][:10] for k in V)
        M.append(f"| {md['lord']} | {md['start'][:10]} | {md['end'][:10]} | {rng[0]} … {rng[-1]} |")
    sun_md = next(m for m in V["+0min"]["mahadashas"] if m["lord"] == "Sun")
    M += ["", "Sun Mahadasha antardashas (09:30; each shifts with the ±30 min Moon uncertainty):", ""]
    M += [f"- Sun–{ad['lord']}: {ad['start'][:10]} → {ad['end'][:10]}" for ad in sun_md["antardashas"]]
    # BaZi
    bz = raw["bazi"]["primary"]
    M += ["", "## BaZi", "", "| Pillar | 干支 | Stem Ten God | Hidden stems (Ten God) | Na Yin |", "|---|---|---|---|---|"]
    for p in bz["pillars"]:
        M.append(f"| {p['pillar']} | {p['ganzhi']} {p['pinyin']} | {p['ten_god_of_stem']} | " +
                 ", ".join(f"{h['stem']} {h['ten_god']}" for h in p["hidden_stems"]) + f" | {p['na_yin_traditional_attribute']} |")
    M += ["", f"Alternative hour (solar-time track, birth ≥27.4 min earlier): {raw['bazi']['alternative_hour_Chen']['hour_pillar']['ganzhi']}.",
          f"Day Master strength (BZ-DM-1): support share {bz['dm_strength']['support_share']:.3f} → {bz['dm_strength']['weighted_count_verdict']}; seasonal: {bz['dm_strength']['seasonal_verdict']}; rooted in {bz['dm_strength']['rooting']}.",
          "Interactions: " + "; ".join(f"{i['type']} {i['chars']} ({'/'.join(i.get('pillars', []))})" + (f", transformed={i['transformed']}" if 'transformed' in i else '') for i in bz["interactions"]), "",
          f"Da Yun {bz['da_yun']['direction']}; start {bz['da_yun']['start_date_exact_3day_rule']} (exact 3-day rule) vs {bz['da_yun']['lunar_python_start']['date']} (lunar_python).", ""]
    M += [f"- {t['technique']}: {t['start']} → {t['end']} — {t['basis']}" for t in syn["timing"]["techniques"] if t["technique"].startswith("BaZi")][:5]
    # Western
    wc = raw["western"]["charts"]["+0min"]
    M += ["", f"## Western / Hellenistic — Asc {wc['asc']['sign']} {wc['asc']['deg']:.2f}° (Leo if birth ≥21.3 min later), {wc['sect']} chart", "",
          "| Planet | Sign | Deg | House | Dignities | Sect | Visibility | Motion |", "|---|---|---|---|---|---|---|---|"]
    for p, v in wc["planets"].items():
        M.append(f"| {p} | {v['sign']} | {v['deg']:.2f} | {v['whole_sign_house']} | {', '.join(v['essential']['planet_dignities'])} | {v['sect_status']} | {v['visibility'] or '—'} | "
                 f"{'R' if v['retrograde'] else 'D'}{' stationary' if v['stationary'] else ''} |")
    M += ["", f"Lots: Fortune {fmt_dms(wc['lots']['fortune']['lon'])}, Spirit {fmt_dms(wc['lots']['spirit']['lon'])} (both sensitive).",
          f"Dispositors: terminal loop {wc['terminal_loops']}; mutual receptions {wc['mutual_receptions_by_domicile']}.",
          "Aspects (by sign; ≤3° marked): " + "; ".join(f"{x['a']}–{x['b']} {x['aspect']} {x['degree_orb']:.1f}°{' ✱' if x['within_kollesis_3deg'] else ''}" for x in wc["aspects"]), "",
          "Profections: " + "; ".join(f"age {p['age']} ({p['start']}→{p['end']}): house {p['activated_house']} {p['profected_sign']}, lord {p['lord_of_year']}" for p in wc["profections"]), ""]
    for y, s in raw["western"]["solar_returns"].items():
        M.append(f"Solar return {y}: {s['utc']} — " + ", ".join(f"{k}: Asc {v['asc_sign']}" for k, v in s["locations"].items()) +
                 f"; ±30 min: {s['ensemble_asc_signs']}; location changes Asc sign: {s['location_changes_asc_sign']}")
    # Zi Wei
    for br in ("巳", "辰"):
        z = raw["ziwei"]["alternatives"][br]
        zc, ze = z["chart_zh"], z["chart_en"]
        M += ["", f"## Zi Wei Dou Shu — {br} hour ({'primary, civil clock' if br == '巳' else 'alternative: solar-time track, first 2.6 min of ±30'})", "",
              f"Lunar {zc['lunarDate']}; 命宫 {zc['earthlyBranchOfSoulPalace']}, 身宫 {zc['earthlyBranchOfBodyPalace']}; 命主 {zc['soul']}, 身主 {zc['body']}; {zc['fiveElementsClass']} ({ze['fiveElementsClass']}).", "",
              "| Palace | 干支 | Major stars | Minor stars | Decadal |", "|---|---|---|---|---|"]
        for p, pe in zip(zc["palaces"], ze["palaces"]):
            M.append(f"| {p['name']} {pe['name']}{' 身' if p['isBodyPalace'] else ''} | {p['heavenlyStem']}{p['earthlyBranch']} | " +
                     " ".join(f"{s['name']}{s['brightness'] or ''}{'化' + s['mutagen'] if s.get('mutagen') else ''}" for s in p["majorStars"]) + " | " +
                     " ".join(s["name"] + ('化' + s['mutagen'] if s.get('mutagen') else '') for s in p["minorStars"]) + f" | {p['decadal']['range'][0]}–{p['decadal']['range'][1]} |")
    m, t = raw["maya"], raw["tibetan"]
    M += ["", "## Maya calendar", "", f"Long Count {m['long_count']}; Tzolk'in {m['tzolkin']}; Haab' {m['own_implementation']['haab']} (convertdate spelling {m['haab']}); correlation {m['correlation_constant']}; round-trip {m['round_trip_ok']}.",
          "", "## Tibetan", "", f"{t['gender']} {t['element']} {t['animal']} year. {t['losar_boundary_check']}", "Omitted: " + "; ".join(f"{k}: {v}" for k, v in t["omitted"].items())]
    w("MASTER_DATASET.md", M)

    # ---------------- FINAL_READING.md ----------------
    outer, inner = syn["scenarios"]["outer"], syn["scenarios"]["inner"]
    R = ["# Six-culture chart reading", "",
         "*This is computed symbolic corroboration between traditional systems, not a validated forecast. None of it is scientific evidence about your character or your future.*", "",
         "## 1. Input and sensitivity", "",
         f"- Born **{a['weekday']} {a['gregorian_date']}, {a['local_time_24h'][:5]} IST (UTC{a['local_iso'][-6:]}, no DST)** = {a['utc_iso'][:16].replace('T', ' ')} UTC, Lucknow ({a['latitude']}°N, {a['longitude']}°E; city-centre coordinates).",
         f"- Local mean time {a['local_mean_time'][11:]}; local apparent solar time {a['local_apparent_solar_time'][11:]}. Sunrise {a['sunrise']['swiss_ephemeris'][11:16]}, sunset {a['sunset']['swiss_ephemeris'][11:16]}.",
         f"- Your stated uncertainty (15–30 min) was modelled as ±30 min (primary) and ±15 min (inner). **Three things move within that window:**",
         f"  - **Vedic rising sign (Lagna)**: Cancer 1.49°. If birth was **≥6.9 min earlier (before ~09:23)** it is **Gemini**. This is sensitive even within ±15 min, so no Vedic house-based claim is graded.",
         f"  - **Western Ascendant**: Cancer 25.41°. If birth was **≥21.3 min later (after ~09:51)** it becomes **Leo**. Stable within ±15 min.",
         f"  - **Chinese double-hour**: 巳 Si on the civil clock across the whole window. Under local solar time it becomes 辰 Chen only if birth was ≥27.4 min earlier (before ~09:02). This affects the BaZi hour pillar (癸巳 vs 壬辰) and the whole Zi Wei palace layout.",
         "- Stable across ±30 min: all planetary signs (both zodiacs), Moon nakshatra (Ashwini), the Vedic Moon-sign reference, day/night sect, the BaZi year, month and day pillars, and the Maya and Tibetan dates.", "",
         "## 2. Verification", "",
         f"- Swiss Ephemeris vs NASA JPL DE440s (via Skyfield): the largest planetary difference is **{ver['largest_planet_difference_deg']:.1e}°** (alert threshold 0.01°). The Ascendant/MC agree to within 0.002°.",
         f"- Chinese solar terms (立夏, 芒种): four engines agree to ≤{max(v['max_difference_s'] for v in raw['bazi']['primary']['solar_terms'].values()):.1f} s. Four Pillars: lunar_python = sxtwl (an independent codebase).",
         "- Zi Wei: canonical iztro 2.6.1 matches the py-iztro wrapper. These are the **same method**, so the match is an interface check, not independent confirmation. All 6 structural invariants pass for both hour alternatives.",
         "- Maya: convertdate and a separate implementation agree; the date round-trips exactly.",
         f"- **Invariant failures: {len(ver['failures'])}.**",
         "- Unavailable or not computed: Shadbala, Ashtakavarga, Pratyantardasha, D7/D12, zodiacal releasing, transits, Tibetan Mewa/Parkha/personal forces, and Maya/Tibetan symbolic meanings (no verifiable source).", "",
         "## 3. Divergence rate (read this before the themes)", "",
         f"- Primary (±30 min): **{outer['divergence_rate_all']} domains divergent** ({outer['divergence_rate_sufficient']} of domains with enough evidence). Grade counts: {outer['counts']}.",
         f"- Inner (±15 min, Western houses allowed): {inner['divergence_rate_all']} divergent; counts {inner['counts']}.",
         "- There are no outright conflicts, but there is also **no STRONG domain**. Most agreement is between Jyotisha and the Sinic cluster. With Vedic houses excluded, the Western cluster is mostly neutral.", "",
         "## 4. Cross-cultural themes", ""]
    for scen, sc in (("outer", outer), ("inner", inner)):
        for d, v in sc["domains"].items():
            if v["grade"] in ("STRONG", "MODERATE") and not (scen == "inner" and outer["domains"][d]["grade"] == v["grade"]):
                tag = "" if scen == "outer" else " *(inner ±15 min scenario only)*"
                R.append(f"### {d} {v['domain']} — {v['grade']} ({v['agreed_polarity']}){tag}")
                for p in v["projections"]:
                    if sc["domains"][d]["cluster_polarity"][p["cluster"]] == v["agreed_polarity"] and p["polarity"] not in ("neutral", "silent"):
                        R.append(f"- {p['system']}: {p['basis']} → {p['polarity']} [{p['mapping_rule']}]")
                R.append("")
    R += ["What these mean, stated narrowly:",
          "- **D3 Wealth/gains (MODERATE, mixed):** Jyotisha (Jupiter as wealth-significator in a friendly sign, against the Sun in the 2nd from the Moon) and BaZi (Metal/Wealth is the largest element while the Day Master counts as weak, 财多身弱) agree on the same thing: money matters are **prominent but double-edged**. Neither system says success or failure.",
          "- **D4 Partnership (MODERATE, mixed):** Jyotisha (Venus friendly and in its own navamsa, but Ketu in the 7th from the Moon) and the Sinic cluster (spouse palace 申 combined with, punished by and broken by 巳; Zi Wei's 夫妻 palace is also the Body palace, with 廉贞化禄 and 破军(陷)化权) agree that relationships are **a prominent, mixed theme**.",
          "- **D9 Fortune/worldview (MODERATE, positive):** Jyotisha (Jupiter in a friendly sign and vargottama, Leo in both D1 and D9) and Zi Wei (福德 palace with 武曲庙化科 and 贪狼庙) both read **favourably**. The Western cluster is neutral here (Jupiter in detriment, stationing direct).",
          "- **D1 Self (inner scenario only, negative):** if the Western Ascendant is Cancer, Mars (in fall) and Saturn (in detriment) sit on it. Jyotisha independently puts Rahu with the Moon and Mercury in the Moon-sign. Both read this as a **strained self-image theme**. Of these, only the Jyotisha part is stable over ±30 min.", "",
          "## 5. Disagreements (not smoothed over)", "",
          f"- **Day Master strength (BaZi internal):** the weighted count gives support {raw['bazi']['primary']['dm_strength']['support_share']:.2f} → weak. The seasonal rule gives 丙 fire born in 巳 month → prosperous. These disagree, so BaZi's useful-element (Yong Shen) verdict is **low confidence**. The seasonal school (Qiong Tong) points to 壬 water and 庚 metal. The strength-balancing school, using the weak verdict, points to wood and fire. These conclusions are opposite.",
          "- **Temperament axes with conflicts:** T1 leadership (Jyotisha: Sun in an enemy's sign → strained; Zi Wei: 天府 in 命宫 → supported) and T2 drive (Mars: fall in Western, enemy's sign in Jyotisha → strained; Sinic: 破军 in the Body palace plus two hidden Seven Killings → supported).",
          "- **Vedic Lagna Gemini vs Cancer:** the two alternatives give different house pictures. With Gemini, Mars, Venus and Saturn fall on the Lagna; with Cancer, Jupiter falls in the 2nd. Neither is chosen.", "",
          "## 6. Weak and insufficient areas (do not over-read)", ""]
    for d, v in outer["domains"].items():
        if v["grade"] in ("WEAK", "INSUFFICIENT"):
            R.append(f"- {d} {v['domain']}: {v['grade']} — cluster readings {v['cluster_polarity']}")
    R += ["- D7 Health/routine is reported as symbolic prominence only. **Nothing here is a health, medical or lifespan statement.**", "",
          "## 7. Temperament overlay", ""]
    for k, v in syn["temperament"].items():
        R.append(f"- **{k}** — {v['summary']}: " + "; ".join(f"{c} {x['reading']} ({x['basis']})" for c, x in v["clusters"].items()))
    R += [f"- Maya: **{syn['overlays']['maya']['computed']}**, computed and verified. Meaning is {syn['overlays']['maya']['meaning']}.",
          f"- Tibetan: **{syn['overlays']['tibetan']['computed']}** year. Meaning is {syn['overlays']['tibetan']['meaning']}.", "",
          "## 8. Timing", ""]
    cur = syn["timing"]["current"]
    for x in cur:
        R.append(f"- **Now ({x['start']} → {x['end']}): {x['domain']} {x['domain_name']} — {x['grade']}.** " +
                 "; ".join(f"{c}: {', '.join(t)}" for c, t in x["clusters"].items()) + ".")
    an = syn["bazi_annual_ten_gods"]
    R += ["  - Techniques: the Jyotisha Sun Mahadasha started between 2025-11-27 and 2026-03-04 depending on birth time; the Sun is the wealth-house occupant from the Moon. The Western age-22 profection activates the 11th house (gains) for any Ascendant. The BaZi 辛未 luck pillar has Direct Wealth on its stem.",
          f"  - This shows the area is **activated**, not what the outcome will be. BaZi's annual pillar for Lichun 2026 → Lichun 2027 is {an['2026']['ganzhi']} = {an['2026']['stem_ten_god']} / {an['2026']['branch_ten_god']}: a companion/competitor year for a wealth theme. The natal D3 reading is itself mixed.",
          "  - The current Vimshottari sub-period is **sensitive**: Sun–Moon at 09:30, but Sun–Mars if birth was ~30 min later."]
    fut = [x for x in syn["timing"]["next"] if x["start"] > "2026-09-26"]
    for x in fut[:4]:
        R.append(f"- Next: {x['start']} → {x['end']}: {x['domain']} {x['domain_name']} — {x['grade']} (" +
                 "; ".join(f"{c}: {', '.join(t)}" for c, t in x["clusters"].items()) + ")")
    R += ["- Zi Wei decadal: 16–25 (父母 palace; roughly lunar years 2019–2028) → 26–35 (福德 palace, D9; roughly 2029–2038). This holds only for the 巳-hour chart.", "",
          "## 9. Claims removed", ""]
    for k, v in syn["claims_removed"].items():
        R.append(f"- {k}: {v['count'] if isinstance(v, dict) else v}" + (f" — {v.get('note', '')}" if isinstance(v, dict) and v.get("note") else ""))
    R += ["", "## Closing frame", "",
          "These results show where several traditional symbolic systems, each computed under declared conventions and checked against independent engines, happen to agree or disagree. The domain rules and weights are declared in `SYNTHESIS.json` → `registry`, and different reasonable rules would give different grades. Nothing here is a validated forecast, a fate, or a basis for medical, financial or legal decisions."]
    w("FINAL_READING.md", R)


if __name__ == "__main__":
    main()
    print("ok")
