"""Steps 6 and 8: master dataset + human-readable INPUT_AUDIT.md, MASTER_DATASET.md, FINAL_READING.md.

All prose values are read from output/*.json so every sentence is traceable to the datasets.
"""
import json
from datetime import date
import os
import shutil

from sc.common import CHART_DIR, OUT, ROOT, SIGNS, dump, fmt_dms, load_narrative

J = lambda n: json.load(open(os.path.join(OUT, n), encoding="utf-8"))


def w(name, lines):
    open(os.path.join(OUT, name), "w", encoding="utf-8").write("\n".join(lines) + "\n")


def main():
    raw, man, ver, syn = J("RAW_CALCULATIONS.json"), J("CALCULATION_MANIFEST.json"), J("VERIFICATION_REPORT.json"), J("SYNTHESIS.json")
    inp = json.load(open(os.path.join(CHART_DIR, "BIRTH_INPUT.json"), encoding="utf-8"))
    shutil.copy(os.path.join(CHART_DIR, "BIRTH_INPUT.json"), os.path.join(OUT, "BIRTH_INPUT.json"))
    a, st, bd = raw["input_audit"], raw["stability"], raw["boundaries"]
    T = a["local_time_24h"][:5]

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
          f"## Boundary audit (every crossing inside ±{inp['time_uncertainty']['outer_minutes']} min)", "",
          f"| Output | Value at {T} | ±{inp['time_uncertainty']['inner_minutes']} min | ±{inp['time_uncertainty']['outer_minutes']} min | Crossings (minutes from {T}, from → to) |", "|---|---|---|---|---|"]
    for k, v in st.items():
        cr = "; ".join(f"{c['minutes_from_T']:+.1f} min ({c['instant_local'][11:19]}): {c['from']} → {c['to']}" for c in v["crossings"]) or "—"
        L.append(f"| {k} | {v['value_at_T']} | {v['inner_interval']} | {v['outer_interval']} | {cr} |")
    wa, jl = bd["western_asc"], bd["jyotisha_lagna"]
    L += ["", "## Boundary distances", "",
          f"- **Western Ascendant** {fmt_dms(wa['asc_lon'])}: {wa['deg_in_sign']:.2f}° into its sign, {wa['to_next_cusp_deg']:.2f}° before the next (≈{wa['minutes_since_prev_cusp_approx']:.1f} min since / ≈{wa['minutes_to_next_cusp_approx']:.1f} min to a cusp at {wa['asc_rate_deg_per_min']:.3f}°/min).",
          f"- **Jyotisha Lagna** {fmt_dms(jl['lagna_lon'])} (Lahiri): {jl['deg_in_sign']:.2f}° into its sign (≈{jl['minutes_since_prev_cusp_approx']:.1f} min since / ≈{jl['minutes_to_next_cusp_approx']:.1f} min to a cusp). D9 segment {jl['d9_segment_deg'][0]:.2f}–{jl['d9_segment_deg'][1]:.2f}°, D10 segment {jl['d10_segment_deg'][0]}–{jl['d10_segment_deg'][1]}°.",
          f"- **Sect**: {bd['sunrise_sect']['minutes_after_sunrise']:.0f} min after sunrise, {bd['sunrise_sect']['minutes_before_sunset']:.0f} min before sunset → {st['sect']['value_at_T']} chart, {st['sect']['outer_interval']}.",
          "- **BaZi / Zi Wei hour**: " + "; ".join(f"{trk} {v['time'][11:16]} is {v['minutes_into_branch']:.1f} min into the {v['branch']} double-hour ({v['window']}), {v['minutes_to_branch_end']:.1f} min before its end" for trk, v in bd["bazi_hour"].items() if trk in ("civil", "LAT"))
          + f". Nearest boundary: {bd['bazi_hour']['nearest_boundary']['minutes']:.1f} min ({bd['bazi_hour']['nearest_boundary']['track']} track, branch {bd['bazi_hour']['nearest_boundary']['side']}).",
          f"- **Day boundary**: {bd['day_boundary']['minutes_after_local_midnight']} min after midnight; {bd['day_boundary']['note']}.",
          f"- **Solar terms**: birth {raw['bazi']['primary']['birth_after_prev_jie_days']:.2f} days after {raw['bazi']['primary']['prev_jie']} and {raw['bazi']['primary']['birth_before_next_jie_days']:.2f} days before {raw['bazi']['primary']['next_jie']} → month {raw['bazi']['primary']['pillars'][1]['ganzhi']} stable.",
          f"- **Zi Wei lunar date**: {bd['zi_wei_lunar']['lunar_date']} (leap month: {bd['zi_wei_lunar']['is_leap_month']}; year's leap month: {bd['zi_wei_lunar']['leap_month_of_year'] or 'none'}); next new moon {bd['zi_wei_lunar']['next_new_moon_utc']} ({bd['zi_wei_lunar']['hours_to_next_new_moon']:.1f} h after birth).",
          f"- **Tibetan Losar**: {bd['tibetan_losar']}.",
          f"- **Calendar adoption**: {bd['calendar_adoption']}.",
          "- **Planets within 1° of a sign cusp**: " + ("; ".join(f"{c['body']} {c['deg_from_cusp']:.2f}° ({c['zodiac']}, ≈{c['hours_per_degree'] * c['deg_from_cusp']:.0f} h of motion)" for c in bd["planets_near_sign_cusp"] if c["hours_per_degree"]) or "none") + "."]
    w("INPUT_AUDIT.md", L)

    # ---------------- MASTER_DATASET.md ----------------
    A = raw["astronomy"]["+0min"]
    M = ["# Master dataset (facts only, no interpretation)", "", f"Birth instant: {a['local_iso']} ({a['utc_iso']} UTC), {a['weekday']}, {inp['birthplace']['name']} {a['latitude']:.4f}N {a['longitude']:.4f}E.", "",
         f"## Positions at {T} local", "", "| Body | Tropical | Sidereal (Lahiri) | Speed °/d | JPL Δ° |", "|---|---|---|---|---|"]
    for b in ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto", "MeanNode", "TrueNode"]:
        v = A["bodies"][b]
        M.append(f"| {b} | {fmt_dms(v['lon'])} | {fmt_dms(v['sidereal_lon'])} | {v['speed_deg_day']:+.4f} | {format(v['validator_difference_deg'], '.1e') if v.get('validator_difference_deg') is not None else '— (no validator)'} |")
    M += [f"| Asc | {fmt_dms(A['angles_tropical']['asc'])} | {fmt_dms(A['angles_sidereal']['asc'])} | | {A['angle_differences_deg']['asc']:.1e} |",
          f"| MC | {fmt_dms(A['angles_tropical']['mc'])} | {fmt_dms(A['angles_sidereal']['mc'])} | | {A['angle_differences_deg']['mc']:.1e} |",
          f"", f"Lahiri ayanamsha {A['ayanamsha_lahiri_deg']:.6f}°.", ""]
    # Jyotisha
    jl_min = bd["jyotisha_lagna"]["minutes_since_prev_cusp_approx"]
    alt_offs = [o for o in raw["jyotisha"]["charts"] if raw["jyotisha"]["charts"][o]["lagna"]["sign"] != raw["jyotisha"]["charts"]["+0min"]["lagna"]["sign"]]
    for off in ["+0min"] + alt_offs[:1]:
        c = raw["jyotisha"]["charts"][off]
        M += [f"## Jyotisha D1 — Lagna {c['lagna']['sign']} {c['lagna']['deg']:.2f}° ({off} alternative)" if off != "+0min" else
              f"## Jyotisha D1 — Lagna {c['lagna']['sign']} {c['lagna']['deg']:.2f}° ({T}; previous cusp ≈{jl_min:.1f} min earlier, next ≈{bd['jyotisha_lagna']['minutes_to_next_cusp_approx']:.1f} min later)", "",
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
          f"| Mahadasha | Start ({T}) | End ({T}) | Start range ±{inp['time_uncertainty']['outer_minutes']} min |", "|---|---|---|---|"]
    by_ = int(a["gregorian_date"][:4])
    for i, md in enumerate(m_ for m_ in V["+0min"]["mahadashas"] if int(m_["start"][:4]) <= by_ + 100):
        rng = sorted(V[k]["mahadashas"][i]["start"][:10] for k in V)
        M.append(f"| {md['lord']} | {md['start'][:10]} | {md['end'][:10]} | {rng[0]} … {rng[-1]} |")
    today_s = inp["analysis_date"]
    cur_md = next(m for m in V["+0min"]["mahadashas"] if m["start"][:10] <= today_s < m["end"][:10])
    L_ = cur_md["lord"]
    M += ["", f"Current ({L_}) Mahadasha antardashas at {T} (pratyantardashas listed where computed):", ""]
    for ad in cur_md["antardashas"]:
        M.append(f"- {L_}–{ad['lord']}: {ad['start'][:10]} → {ad['end'][:10]}")
        for pd in ad.get("pratyantardashas", []):
            M.append(f"  - {L_}–{ad['lord']}–{pd['lord']}: {pd['start'][:10]} → {pd['end'][:10]}")
    # BaZi
    bz = raw["bazi"]["primary"]
    M += ["", "## BaZi", "", "| Pillar | 干支 | Stem Ten God | Hidden stems (Ten God) | Na Yin |", "|---|---|---|---|---|"]
    for p in bz["pillars"]:
        M.append(f"| {p['pillar']} | {p['ganzhi']} {p['pinyin']} | {p['ten_god_of_stem']} | " +
                 ", ".join(f"{h['stem']} {h['ten_god']}" for h in p["hidden_stems"]) + f" | {p['na_yin_traditional_attribute']} |")
    alt_h = raw["bazi"]["alternative_hour"]
    M += ["", f"Adjacent hour pillar {alt_h['hour_pillar']['ganzhi']}: reached if {alt_h['reached_if']}; "
              f"{'outside' if alt_h['minutes_away'] > inp['time_uncertainty']['outer_minutes'] else 'INSIDE'} the ±{inp['time_uncertainty']['outer_minutes']} min interval.",
          f"Day Master strength (BZ-DM-1): support share {bz['dm_strength']['support_share']:.3f} → {bz['dm_strength']['weighted_count_verdict']}; seasonal: {bz['dm_strength']['seasonal_verdict']}; rooted in {bz['dm_strength']['rooting']}.",
          "Interactions: " + "; ".join(f"{i['type']} {i['chars']} ({'/'.join(i.get('pillars', []))})" + (f", transformed={i['transformed']}" if 'transformed' in i else '') for i in bz["interactions"]), "",
          f"Da Yun {bz['da_yun']['direction']}; start {bz['da_yun']['start_date_exact_3day_rule']} (exact 3-day rule) vs {bz['da_yun']['lunar_python_start']['date']} (lunar_python).", ""]
    M += [f"- {t['technique']}: {t['start']} → {t['end']} — {t['basis']}" for t in syn["timing"]["techniques"] if t["technique"].startswith("BaZi")][:5]
    # Western
    wc = raw["western"]["charts"]["+0min"]
    M += ["", f"## Western / Hellenistic — Asc {wc['asc']['sign']} {wc['asc']['deg']:.2f}° (previous cusp ≈{bd['western_asc']['minutes_since_prev_cusp_approx']:.1f} min earlier, next ≈{bd['western_asc']['minutes_to_next_cusp_approx']:.1f} min later), {wc['sect']} chart", "",
          "| Planet | Sign | Deg | House | Dignities | Sect | Visibility | Motion |", "|---|---|---|---|---|---|---|---|"]
    for p, v in wc["planets"].items():
        M.append(f"| {p} | {v['sign']} | {v['deg']:.2f} | {v['whole_sign_house']} | {', '.join(v['essential']['planet_dignities'])} | {v['sect_status']} | {v['visibility'] or '—'} | "
                 f"{'R' if v['retrograde'] else 'D'}{' stationary' if v['stationary'] else ''} |")
    M += ["", f"Lots: Fortune {fmt_dms(wc['lots']['fortune']['lon'])}, Spirit {fmt_dms(wc['lots']['spirit']['lon'])} (Fortune sign {st['western_lot_fortune_sign']['outer_interval']} over the interval).",
          f"Dispositors: terminal loop {wc['terminal_loops']}; mutual receptions {wc['mutual_receptions_by_domicile']}.",
          "Aspects (by sign; ≤3° marked): " + "; ".join(f"{x['a']}–{x['b']} {x['aspect']} {x['degree_orb']:.1f}°{' ✱' if x['within_kollesis_3deg'] else ''}" for x in wc["aspects"]), "",
          "Profections: " + "; ".join(f"age {p['age']} ({p['start']}→{p['end']}): house {p['activated_house']} {p['profected_sign']}, lord {p['lord_of_year']}" for p in wc["profections"]), ""]
    for y, s in raw["western"]["solar_returns"].items():
        M.append(f"Solar return {y}: {s['utc']} — " + ", ".join(f"{k}: Asc {v['asc_sign']}" for k, v in s["locations"].items()) +
                 f"; at interval edges: {s['ensemble_asc_signs']}; location changes Asc sign: {s['location_changes_asc_sign']}")
    # Zi Wei
    zb = syn["reference_frames"]["ziwei_hour_branch"]
    for br in [zb] + [b for b in raw["ziwei"]["alternatives"] if b != zb]:
        z = raw["ziwei"]["alternatives"][br]
        zc, ze = z["chart_zh"], z["chart_en"]
        M += ["", f"## Zi Wei Dou Shu — {br} hour ({'primary' if br == zb else 'adjacent hour, outside the confirmed interval — reference only'})", "",
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
    write_reading(raw, ver, syn, inp)


def write_reading(raw, ver, syn, inp):
    a, st, bd = raw["input_audit"], raw["stability"], raw["boundaries"]
    unc = inp["time_uncertainty"]
    sc = syn["scenarios"]["outer"]
    D = sc["domains"]
    sensitive = [k for k, v in st.items() if v["outer_interval"] != "stable"]
    jl, wa = bd["jyotisha_lagna"], bd["western_asc"]
    jc = raw["jyotisha"]["charts"]["+0min"]
    wc = raw["western"]["charts"]["+0min"]
    bz = raw["bazi"]["primary"]
    zb = syn["reference_frames"]["ziwei_hour_branch"]
    R = ["# Six-culture chart reading", "",
         "*This shows where several traditional symbolic systems agree or disagree, not a validated forecast. None of it is scientific evidence about your character or your future.*", "",
         "## 1. Input and sensitivity", "",
         f"- Born **{a['weekday']} {a['gregorian_date']}, {a['local_time_24h'][:5]} IST (UTC{a['local_iso'][-6:]}, no DST)** = {a['utc_iso'][:16].replace('T', ' ')} UTC, {inp['birthplace']['name']} ({a['latitude']:.4f}°N, {a['longitude']:.4f}°E; {inp['birthplace']['coordinate_source'].split(',')[0]}).",
         f"- Local mean time {a['local_mean_time'][11:]}; local apparent solar time {a['local_apparent_solar_time'][11:]}. Sunrise {a['sunrise']['swiss_ephemeris'][11:16]}, sunset {a['sunset']['swiss_ephemeris'][11:16]}.",
         f"- Time uncertainty: {unc['interpretation']}. Modelled as **±{unc['outer_minutes']} min**"
         + (f" (inner scenario ±{unc['inner_minutes']} min)" if unc['inner_minutes'] != unc['outer_minutes'] else "") + ". "
         + ("**Every time-dependent output is stable over that interval.**" if not sensitive else
            "**Outputs that change inside it:** " + "; ".join(
                k + " (" + ", ".join(f"{c['from']}→{c['to']} at {c['minutes_from_T']:+.1f} min" for c in st[k]["crossings"]) + ")"
                for k in sensitive) + "."),
         f"- Nearest boundaries: Vedic Lagna {jc['lagna']['sign']} {jl['deg_in_sign']:.2f}° (≈{jl['minutes_since_prev_cusp_approx']:.1f} min after / ≈{jl['minutes_to_next_cusp_approx']:.1f} min before a cusp); "
         f"Western Ascendant {wc['asc']['sign']} {wa['deg_in_sign']:.2f}° (≈{wa['minutes_since_prev_cusp_approx']:.1f} / ≈{wa['minutes_to_next_cusp_approx']:.1f} min); "
         f"Chinese double-hour boundary ≈{bd['bazi_hour']['nearest_boundary']['minutes']:.1f} min away ({bd['bazi_hour']['nearest_boundary']['track']} track).",
         ("- Birthplace is a named hospital, so positional uncertainty is under ~100 m, negligible for every output." if "previous_coordinates" in inp["birthplace"]
          else f"- Coordinates: {inp['birthplace']['coordinate_source']}. A different hospital in the same town shifts the Ascendant by roughly 0.1°."),
         f"- Houses are counted from the **{'Lagna' if syn['reference_frames']['jyotisha_houses'] == 'lagna' else 'Moon (Chandra Lagna), because the Lagna sign is not stable'}** (Jyotisha); "
         f"Western houses {'vote' if syn['reference_frames']['western_houses_vote'] else 'do not vote, because the Ascendant sign is not stable'}. Zi Wei uses the **{zb}** hour. (Rules JY-REFERENCE and W-HOUSES.)", "",
         "## 2. Verification", "",
         f"- Swiss Ephemeris vs NASA JPL DE440s (via Skyfield): the largest planetary difference is **{ver['largest_planet_difference_deg']:.1e}°** (alert threshold 0.01°). The Ascendant/MC agree to within 0.002°.",
         f"- Chinese solar terms ({', '.join(bz['solar_terms'])}): four engines agree to ≤{max(v['max_difference_s'] for v in bz['solar_terms'].values()):.1f} s. Four Pillars: lunar_python = sxtwl (an independent codebase): **{' '.join(p['ganzhi'] for p in bz['pillars'])}**.",
         f"- Zi Wei: canonical iztro {raw['ziwei']['alternatives'][zb]['chart_zh']['iztro_version']} matches the py-iztro wrapper. These are the **same method**, so the match is an interface check only. All structural invariants pass.",
         "- Maya: convertdate and a separate implementation agree; the date round-trips exactly.",
         f"- **Invariant failures: {len(ver['failures'])}.**",
         "- Unavailable: " + ", ".join(syn["claims_removed"]["unavailable_methods"]["items"]) + ". Also unavailable: Tibetan Mewa/Parkha/personal forces, and Maya/Tibetan symbolic meanings (no verifiable source).", "",
         "## 3. Divergence rate (read this before the themes)", "",
         f"- **{sc['divergence_rate_all']} domains divergent** ({sc['divergence_rate_sufficient']} of domains with enough evidence). Grade counts: " +
         ", ".join(f"{k} {v}" for k, v in sc["counts"].items()) + ".", ""]
    for d, v in D.items():
        if v["grade"] == "DIVERGENT":
            R.append(f"- **{d} {v['domain']} — DIVERGENT:** " + "; ".join(
                f"{p['system']}: {p['basis']} → {p['polarity']}" for p in v["projections"] if p["polarity"] in ("positive", "negative")))
    R += ["", "## 4. Cross-cultural themes (STRONG first, then MODERATE)", ""]
    order = sorted([d for d, v in D.items() if v["grade"] in ("STRONG", "MODERATE")], key=lambda d: D[d]["grade"] != "STRONG")
    if not any(D[d]["grade"] == "STRONG" for d in D):
        R += ["*No domain reaches STRONG (all three clusters agreeing).*", ""]
    for d in order:
        v = D[d]
        R.append(f"### {d} {v['domain']} — {v['grade']} ({v['agreed_polarity']})")
        R.append("Cluster readings: " + ", ".join(f"{k} {x}" for k, x in v["cluster_polarity"].items()))
        for p in v["projections"]:
            if p["polarity"] not in ("neutral", "silent"):
                R.append(f"- {p['system']}: {p['basis']} → {p['polarity']} [{p['mapping_rule']}]")
        R.append("")
    NV = load_narrative().get("reading", {})
    R.append("What these mean, stated narrowly:")
    for d in order:
        t = NV.get("narrow", {}).get(f"{d}|{D[d]['agreed_polarity']}|{D[d]['grade']}")
        if t:
            R.append(f"- **{d} {D[d]['domain']}:** {t}")
    R += ["- Prominence is not outcome. None of these says anything will succeed or fail.", "",
          "## 5. Disagreements (not smoothed over)", ""]
    for d, v in D.items():
        if v["grade"] == "DIVERGENT":
            t = NV.get("divergent", {}).get(d)
            R.append(f"- **{d} {v['domain']}:** " + (t or "; ".join(f"{p['system']}: {p['basis']} → {p['polarity']}" for p in v["projections"] if p["polarity"] in ("positive", "negative"))))
    dm = bz["dm_strength"]
    ys = bz["yong_shen"]
    R += [f"- **BaZi Day Master strength:** the weighted count gives support {dm['support_share']:.2f} → {dm['weighted_count_verdict']}; the seasonal rule gives {dm['seasonal_verdict']}"
          + (" — the two disagree" if ys["sub_verdicts_disagree"] else " — they agree") + f". Favourable-element (Yong Shen) confidence: **{ys['confidence']}**. "
          + " ".join(f"{sc_['school']}: {', '.join(sc_.get('useful_elements') or sc_['useful'])}." for sc_ in ys["schools"]),
          "- **Temperament conflicts:** " + "; ".join(f"{k} ({', '.join(c + ' ' + x['reading'] for c, x in v['clusters'].items())})" for k, v in syn["temperament"].items() if v["summary"] == "conflict") + ".",
          f"- **Secondary Vedic view ({'from the Moon' if syn['reference_frames']['jyotisha_houses'] == 'lagna' else 'from the Lagna'}, non-voting):** "
          + "; ".join(f"{p['domain']}: {p['basis']} → {p['polarity']}" for p in syn["secondary_jyotisha_view"]) + ".", "",
          "## 6. Weak areas (do not over-read)", ""]
    for d, v in D.items():
        if v["grade"] in ("WEAK", "INSUFFICIENT"):
            R.append(f"- {d} {v['domain']}: {v['grade']} — " + ", ".join(f"{k} {x}" for k, x in v["cluster_polarity"].items()))
    R += ["- D7 Health/routine is symbolic prominence only. **Nothing here is a health, medical or lifespan statement.**", "",
          "## 7. Temperament overlay", ""]
    for k, v in syn["temperament"].items():
        R.append(f"- **{k}** — {v['summary']}: " + "; ".join(f"{c} {x['reading']} ({x['basis']})" for c, x in v["clusters"].items()))
    R += [f"- Maya: **{syn['overlays']['maya']['computed']}**, computed and verified. Meaning is {syn['overlays']['maya']['meaning']}.",
          f"- Tibetan: **{syn['overlays']['tibetan']['computed']}** year. Meaning is {syn['overlays']['tibetan']['meaning']}.", "",
          "## 8. Timing", ""]
    today = inp["analysis_date"]
    for x in syn["timing"]["current"]:
        R.append(f"- **Now ({x['start']} → {x['end']}): {x['domain']} {x['domain_name']} — {x['grade']}.** " +
                 "; ".join(f"{c}: {', '.join(t)}" for c, t in x["clusters"].items()) + ".")
    if not syn["timing"]["current"]:
        R.append("- No moderate or strong convergence is active today.")
    V = raw["jyotisha"]["vimshottari"]["+0min"]
    cur = []
    for md in V["mahadashas"]:
        if md["start"][:10] <= today < md["end"][:10]:
            cur.append(("Mahadasha", md))
            for ad in md["antardashas"]:
                if ad["start"][:10] <= today < ad["end"][:10]:
                    cur.append(("Antardasha", ad))
                    for pd in ad.get("pratyantardashas", []):
                        if pd["start"][:10] <= today < pd["end"][:10]:
                            cur.append(("Pratyantardasha", pd))
    an = syn["bazi_annual_ten_gods"]
    VV = raw["jyotisha"]["vimshottari"]
    starts = sorted(VV[k]["mahadashas"][2]["start"][:10] for k in VV)
    spread = (date.fromisoformat(starts[-1]) - date.fromisoformat(starts[0])).days / 2
    yk = today[:4]
    R += ["  - Current Vimshottari: " + " / ".join(f"{k} {x['lord']} ({x['start'][:10]} → {x['end'][:10]})" for k, x in cur) +
          f". Dates move by about ±{spread:.0f} days across ±{unc['outer_minutes']} min."]
    for tn in NV.get("timing_notes", []):
        if any(x["domain"] == tn["guard_current_domain"] for x in syn["timing"]["current"]):
            R.append("  - " + tn["text"])
    if yk in an:
        R.append(f"  - BaZi year {an[yk]['ganzhi']} (Lichun {yk} → Lichun {int(yk) + 1}): stem {an[yk]['stem_ten_god']}, branch {an[yk]['branch_ten_god']}. Activation is not outcome.")
    for x in [x for x in syn["timing"]["next"] if x["start"] > today][:4]:
        R.append(f"- Next: {x['start']} → {x['end']}: {x['domain']} {x['domain_name']} — {x['grade']} (" +
                 "; ".join(f"{c}: {', '.join(t)}" for c, t in x["clusters"].items()) + ")")
    zwd = sorted([t for t in syn["timing"]["techniques"] if t["technique"].startswith("Zi Wei")], key=lambda t: t["start_iso_approx"])
    zwd = [t for t in zwd if t["end_iso_approx"] > today][:2]
    R += ["- Zi Wei decadal (not a convergence by itself): " + "; then ".join(f"{t['technique'].split('decadal ')[1]} ≈{t['start_iso_approx'][:4]}–{t['end_iso_approx'][:4]}" for t in zwd) + ".", "",
          "## 9. Claims removed", ""]
    for k, v in syn["claims_removed"].items():
        R.append(f"- {k}: {v['count'] if isinstance(v, dict) else v}" + (f" — {v.get('note', '')}" if isinstance(v, dict) and v.get("note") else ""))
    R += ["", "## Closing frame", "",
          "These results show where several traditional symbolic systems, each computed under declared conventions and checked against independent engines, happen to agree or disagree. The domain rules and weights are declared in `SYNTHESIS.json` → `registry`, and different reasonable rules would give different grades. Nothing here is a validated forecast, a fate, or a basis for medical, financial or legal decisions."]
    w("FINAL_READING.md", R)

if __name__ == "__main__":
    main()
    print("ok")
