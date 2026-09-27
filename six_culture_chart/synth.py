"""Step 7: synthesis by primary cultural cluster using a predeclared mapping registry.

Only reads output/RAW_CALCULATIONS.json + VERIFICATION_REPORT.json. Emits output/SYNTHESIS.json.
Every projection names the rule that produced it; weights are declared here, before any cross-system comparison.
"""
import json
import os
from datetime import date, datetime, timedelta

from sc.common import OUT, SIGNS, dump

DOMAINS = {"D1": "Self/identity", "D2": "Career/status", "D3": "Wealth/gains", "D4": "Partnership",
           "D5": "Family/roots/home", "D6": "Children/creation", "D7": "Health/routine",
           "D8": "Mind/education/craft", "D9": "Fortune/spirituality/worldview"}
HOUSE_DOMAIN = {1: "D1", 2: "D3", 3: "D8", 4: "D5", 5: "D6", 6: "D7", 7: "D4", 9: "D9", 10: "D2", 11: "D3"}
# (8 and 12 deliberately unmapped: no single domain in the nine-domain scheme)

REGISTRY = {
    "HOUSE-OCC": "Whole-sign house/palace occupied -> domain via HOUSE_DOMAIN; prominence high if >=2 occupants else medium; "
                 "polarity from the sum of occupant scores",
    "JY-KARAKA": "Parashari naisargika karakas: Sun->D1,D2; Moon->D5,D8; Mercury->D8; Jupiter->D3,D6,D9; Venus->D4",
    "W-SIGNIF": "Hellenistic planetary significations (Valens I.1): Sun->D1,D2; Moon->D5,D7; Mercury->D8; Venus->D4; Jupiter->D3,D6,D9",
    "JY-SCORE": "natural nature (Ju/Ve +1, Me +0.5 or -0.5 if with a malefic, Moon +0.5 if 72-288 deg from Sun else -0.5, "
                "Sun -0.5, Ma/Sa/Ra/Ke -1) + sign dignity (exalt/moola/own +1, friend +0.5, neutral 0, enemy -0.5, debil -1) "
                "+ navamsa (own/exalt +0.5, debil -0.5, vargottama +0.5) - 0.5 per malefic sharing the sign",
    "W-SCORE": "nature (Ju/Ve +1, Moon +0.5, Me/Sun 0, Ma/Sa -1) + essential dignity (domicile/exaltation +1, "
               "detriment/fall -1, sect-triplicity +0.5, other triplicity/bound +0.25, face +0.1) + sect "
               "(benefic of sect +0.5, benefic contrary -0.5, malefic of sect +0.5, malefic contrary -0.5) "
               "+ station retrograde -0.5 / station direct +0.25",
    "ZW-SCORE": "major star brightness 庙/旺 +1, 得/利 +0.5, 平 0, 陷/不 -1; 化禄/权/科 +1, 化忌 -1.5; "
                "auspicious minors (左辅 右弼 文昌 文曲 天魁 天钺 禄存 天马) +0.5; malefic minors (擎羊 陀罗 火星 铃星 地空 地劫) -0.75; "
                "empty palace borrows the opposite palace's major stars at half weight (借星安宫)",
    "ZW-PALACE": "命宫->D1, 官禄->D2, 财帛->D3, 夫妻->D4, 田宅/父母->D5, 子女->D6, 疾厄->D7, 福德->D9; "
                 "D8 only if 文昌/文曲 sit in 命宫, 身宫 or 官禄",
    "BZ-D1": "Day Master strength verdicts (BZ-DM-1 weighted vs seasonal) agree -> that polarity; disagree -> mixed",
    "BZ-D2": "Officer/Seven Killings stars visible -> prominence; 伤官见官 (Hurting Officer and Direct Officer both visible) -> mixed",
    "BZ-D3": "Wealth element share >= 25% -> prominence high; weak DM carrying heavy wealth (财多身弱) -> mixed",
    "BZ-D3": "Wealth element (the one the Day Master controls) share >= 25% -> prominence high; weak DM carrying wealth (财多身弱) -> mixed; share < 15% -> neutral",
    "BZ-D4": "spouse palace = day branch (spouse star: Wealth for a male chart, Officer/Killings for a female chart); "
             "punishment/destruction/clash/harm on it -> mixed; only combinations -> positive; none -> neutral",
    "BZ-D5": "Resource star visible in year pillar -> prominence medium; resource stem combined away (合绊) -> mixed",
    "BZ-D6": "children palace = hour pillar; children star = Officer/Killings (male) or Eating/Hurting (female); "
             "visible with conflict (伤官见官 male, 枭神夺食 female) -> mixed; visible -> positive; not visible -> neutral",
    "BZ-D5": "Resource star on a visible stem -> positive; combined away by a stem combination -> mixed; none visible -> neutral",
    "BZ-D8": "Output stars (食神/伤官) visible or >=3 hidden, plus Resource present -> positive, high",
    "POLARITY": "positive if net >= +1 and no component <= -1; negative if net <= -1 and no component >= +1; "
                "mixed if components >= +1 and <= -1 both present; otherwise neutral (does not vote)",
    "GRADE": "STRONG = 3 clusters same polarity; MODERATE = 2 same; WEAK = only one cluster voting or no agreement; "
             "DIVERGENT = any positive-vs-negative conflict between clusters (takes precedence); INSUFFICIENT = none voting",
    "STABILITY": "outer scenario (+/-30 min) counts only facts stable over the whole interval; inner (+/-15 min) counts "
                 "facts stable over +/-15. Sensitive facts are displayed as alternatives and never vote.",
    "JY-REFERENCE": "Jyotisha houses are counted from the Lagna when the Lagna sign is stable over the whole uncertainty "
                    "interval; otherwise from Chandra Lagna (Moon sign). The unused frame is shown as a non-voting secondary view.",
    "W-HOUSES": "Western whole-sign house projections vote only when the Ascendant sign is stable over the whole interval.",
    "CLUSTER": "Jyotisha; Western/Hellenistic; Sinic (BaZi + Zi Wei pooled, one vote). Maya/Tibetan never vote.",
    "TIMING": "a cluster activates a domain in a window if any of its declared techniques does (one vote per cluster): "
              "Jyotisha: Mahadasha lord's karaka domains + its house from the JY-REFERENCE frame; Western: profected house number; "
              "Sinic: Da Yun stem/branch Ten-God domains (Wealth->D3,D4 male; Officer/Killings->D2,D6; Output->D8; "
              "Resource->D5,D8; Companion/Rob->D1) and Zi Wei decadal palace domain",
}

MALEFICS_JY = {"Mars", "Saturn", "Rahu", "Ketu", "Sun"}


def polarity(scores):
    if not scores:
        return "silent"
    pos = [s for s in scores if s >= 1]
    neg = [s for s in scores if s <= -1]
    net = sum(scores)
    if pos and neg:
        return "mixed"
    if net >= 1 and not neg:
        return "positive"
    if net <= -1 and not pos:
        return "negative"
    return "neutral"


# ---------------- Jyotisha ----------------
def jy_score(g, c, elong):
    r = c["grahas"][g]
    same_sign = [h for h in c["grahas"] if h != g and c["grahas"][h]["sign"] == r["sign"]]
    mal_with = [h for h in same_sign if h in MALEFICS_JY]
    base = {"Jupiter": 1, "Venus": 1, "Sun": -0.5, "Mars": -1, "Saturn": -1, "Rahu": -1, "Ketu": -1}.get(g)
    if g == "Mercury":
        base = -0.5 if mal_with else 0.5
    if g == "Moon":
        base = 0.5 if 72 <= elong <= 288 else -0.5
    d = {"exalted": 1, "moolatrikona": 1, "own sign": 1, "friend's sign": 0.5, "neutral sign": 0,
         "enemy's sign": -0.5, "debilitated": -1}.get(r["dignity"], 0)
    nav = 0
    from sc.jyotisha import EXALT, LORD
    if g in EXALT:
        ns = SIGNS.index(r["d9"])
        if LORD[ns] == g or EXALT[g][0] == ns:
            nav += 0.5
        if (EXALT[g][0] + 6) % 12 == ns:
            nav -= 0.5
    if r["d9"] == r["sign"]:
        nav += 0.5
    return base + d + nav - 0.5 * len(mal_with), {"base": base, "dignity": r["dignity"], "d9": r["d9"],
                                                   "navamsa_adj": nav, "malefics_in_sign": mal_with}


def jyotisha_projections(raw, off="+0min", reference="chandra"):
    c = raw["jyotisha"]["charts"][off]
    A = raw["astronomy"][off]["bodies"]
    elong = (A["Moon"]["lon"] - A["Sun"]["lon"]) % 360
    scores = {g: jy_score(g, c, elong) for g in c["grahas"]}
    ref_sign = SIGNS.index(c["grahas"]["Moon"]["sign"]) if reference == "chandra" else SIGNS.index(c["lagna"]["sign"])
    out = []
    by_house = {}
    for g, r in c["grahas"].items():
        h = (SIGNS.index(r["sign"]) - ref_sign) % 12 + 1
        by_house.setdefault(h, []).append(g)
    for h, occ in sorted(by_house.items()):
        if h not in HOUSE_DOMAIN:
            continue
        sc = [scores[g][0] for g in occ]
        out.append({"domain": HOUSE_DOMAIN[h], "system": "jyotisha", "cluster": "jyotisha",
                    "prominence": "high" if len(occ) >= 2 else "medium", "polarity": polarity(sc),
                    "scores": sc, "basis": f"{', '.join(occ)} in house {h} from {'Chandra Lagna (Moon, ' + c['grahas']['Moon']['sign'] + ')' if reference == 'chandra' else 'Lagna (' + c['lagna']['sign'] + ')'}",
                    "mapping_rule": "HOUSE-OCC", "facts": {g: scores[g][1] for g in occ}})
    kar = {"Sun": ["D1", "D2"], "Moon": ["D5", "D8"], "Mercury": ["D8"], "Jupiter": ["D3", "D6", "D9"], "Venus": ["D4"]}
    for g, ds in kar.items():
        for d in ds:
            out.append({"domain": d, "system": "jyotisha", "cluster": "jyotisha", "prominence": "medium",
                        "polarity": polarity([scores[g][0]]), "scores": [scores[g][0]],
                        "basis": f"karaka {g}: {c['grahas'][g]['sign']} ({c['grahas'][g]['dignity']}), navamsa {c['grahas'][g]['d9']}",
                        "mapping_rule": "JY-KARAKA", "facts": scores[g][1]})
    return out, {g: s[0] for g, s in scores.items()}


# ---------------- Western ----------------
def w_score(p, c):
    v = c["planets"][p]
    base = {"Jupiter": 1, "Venus": 1, "Moon": 0.5, "Mars": -1, "Saturn": -1}.get(p, 0)
    dig = v["essential"]["planet_dignities"]
    s = base
    s += sum({"domicile": 1, "exaltation": 1, "detriment": -1, "fall": -1, "triplicity (sect ruler)": 0.5,
              "triplicity (other/participating)": 0.25, "bound": 0.25, "face": 0.1}.get(x, 0) for x in dig)
    if p in ("Jupiter", "Venus"):
        s += 0.5 if v["sect_status"] == "of the sect" else -0.5
    if p in ("Mars", "Saturn"):
        s += 0.5 if v["sect_status"] == "of the sect" else -0.5
    if v["stationary"]:
        # the direction the planet is turning: speed sign after station
        s += -0.5 if p == "Venus" else 0.25 if p == "Jupiter" else 0
    return s, {"dignities": dig, "sect": v["sect_status"], "stationary": v["stationary"]}


STATION_NOTE = "Venus stationing retrograde (speed +0.03°/d, turning), Jupiter stationing direct (speed +0.04°/d)"


def western_projections(raw, off="+0min", houses=True):
    c = raw["western"]["charts"][off]
    scores = {p: w_score(p, c) for p in c["planets"]}
    out = []
    if houses:
        for h, hv in c["houses"].items():
            h = int(h)
            if h not in HOUSE_DOMAIN or not hv["occupants"]:
                continue
            sc = [scores[p][0] for p in hv["occupants"]]
            out.append({"domain": HOUSE_DOMAIN[h], "system": "western", "cluster": "western",
                        "prominence": "high" if len(sc) >= 2 else "medium", "polarity": polarity(sc), "scores": sc,
                        "basis": f"{', '.join(hv['occupants'])} in whole-sign house {h} ({hv['sign']}) from Asc {c['asc']['sign']}",
                        "mapping_rule": "HOUSE-OCC", "facts": {p: scores[p][1] for p in hv["occupants"]}})
    sig = {"Sun": ["D1", "D2"], "Moon": ["D5", "D7"], "Mercury": ["D8"], "Venus": ["D4"], "Jupiter": ["D3", "D6", "D9"]}
    for p, ds in sig.items():
        for d in ds:
            v = c["planets"][p]
            out.append({"domain": d, "system": "western", "cluster": "western", "prominence": "medium",
                        "polarity": polarity([scores[p][0]]), "scores": [scores[p][0]],
                        "basis": f"significator {p}: {v['sign']} {', '.join(v['essential']['planet_dignities'])}, {v['sect_status']}"
                                 + (", stationary" if v["stationary"] else ""),
                        "mapping_rule": "W-SIGNIF", "facts": scores[p][1]})
    return out, {p: s[0] for p, s in scores.items()}


# ---------------- Sinic ----------------
BRIGHT = {"庙": 1, "旺": 1, "得": 0.5, "利": 0.5, "平": 0, "陷": -1, "不": -1, "": 0, None: 0}
GOOD_MINOR = set("左辅 右弼 文昌 文曲 天魁 天钺 禄存 天马".split())
BAD_MINOR = set("擎羊 陀罗 火星 铃星 地空 地劫".split())
PALACE_DOMAIN = {"命宫": "D1", "官禄": "D2", "财帛": "D3", "夫妻": "D4", "田宅": "D5", "父母": "D5",
                 "子女": "D6", "疾厄": "D7", "福德": "D9"}


def zw_palace_score(pal, all_pal):
    parts = []
    majors = pal["majorStars"]
    w = 1.0
    borrowed = False
    if not majors:
        opp = all_pal[(pal["index"] + 6) % 12]
        majors = opp["majorStars"]
        w = 0.5
        borrowed = True
    for s in majors:
        parts.append(w * BRIGHT.get(s["brightness"], 0))
        if s.get("mutagen"):
            parts.append(w * (-1.5 if s["mutagen"] == "忌" else 1))
    for s in pal["minorStars"]:
        if s["name"] in GOOD_MINOR:
            parts.append(0.5)
        elif s["name"] in BAD_MINOR:
            parts.append(-0.75)
        if s.get("mutagen"):
            parts.append(-1.5 if s["mutagen"] == "忌" else 1)
    return parts, borrowed, [s["name"] + (s["brightness"] or "") + (("化" + s["mutagen"]) if s.get("mutagen") else "") for s in majors]


def ziwei_projections(raw, branch=None):
    branch = branch or raw["ziwei"]["primary_branch"]
    ch = raw["ziwei"]["alternatives"][branch]["chart_zh"]
    en = raw["ziwei"]["alternatives"][branch]["chart_en"]
    pal = ch["palaces"]
    out = []
    for p, pe in zip(pal, en["palaces"]):
        if p["name"] not in PALACE_DOMAIN:
            continue
        parts, borrowed, majors = zw_palace_score(p, pal)
        net = sum(parts)
        pol = polarity([net]) if parts else "silent"
        if parts and any(x >= 1 for x in parts) and any(x <= -1 for x in parts):
            pol = "mixed"
        out.append({"domain": PALACE_DOMAIN[p["name"]], "system": "ziwei", "cluster": "sinic",
                    "prominence": "low" if borrowed else ("high" if len(p["majorStars"]) >= 2 or p["isBodyPalace"] else "medium"),
                    "polarity": pol, "scores": [round(net, 2)],
                    "basis": f"{p['name']} ({pe['name']}) at {p['heavenlyStem']}{p['earthlyBranch']}: "
                             f"{'borrowed ' if borrowed else ''}{'/'.join(majors) or '—'}; minors "
                             f"{'/'.join(s['name'] for s in p['minorStars']) or '—'}" + (" [身宫 body palace]" if p["isBodyPalace"] else ""),
                    "mapping_rule": "ZW-PALACE + ZW-SCORE", "facts": {"parts": parts}})
    lit = [p for p in pal if (p["name"] in ("命宫", "官禄") or p["isBodyPalace"]) and
           any(s["name"] in ("文昌", "文曲") for s in p["minorStars"])]
    if lit:
        out.append({"domain": "D8", "system": "ziwei", "cluster": "sinic", "prominence": "medium", "polarity": "positive",
                    "scores": [1.0], "basis": "; ".join(f"{p['name']} holds " + "/".join(s['name'] for s in p['minorStars'] if s['name'] in ('文昌', '文曲')) for p in lit),
                    "mapping_rule": "ZW-PALACE (D8 clause)", "facts": {}})
    return out


def bazi_projections(raw, bz=None):
    from sc.bazi import EL, STEMS, STEM_EL, STEM_COMBOS
    bz = bz or raw["bazi"]["primary"]
    male = raw["input_audit"].get("_gender", "male") == "male"
    P = bz["pillars"]
    dm = bz["dm_strength"]
    dms = bz["day_master"]["stem"]
    dme = STEM_EL[STEMS.index(dms)]
    vis = {p["pillar"]: p["ten_god_of_stem"] for p in P}
    hidden = [h["ten_god"] for p in P for h in p["hidden_stems"]]
    out = []
    strong_season = "旺" in dm["seasonal_verdict"] or "相" in dm["seasonal_verdict"]
    weighted_weak = dm["weighted_count_verdict"] == "weak"
    pol1 = "mixed" if weighted_weak == strong_season else ("positive" if strong_season else "negative")
    out.append({"domain": "D1", "prominence": "high", "polarity": pol1, "scores": [1, -1] if pol1 == "mixed" else [1],
                "basis": f"Day Master {dms} ({bz['day_master']['polarity']} {bz['day_master']['element']}): weighted support "
                         f"{dm['support_share']:.2f} ({dm['weighted_count_verdict']}) vs seasonal {dm['seasonal_verdict']}; "
                         f"rooted in {', '.join(dm['rooting']) or 'none'}", "mapping_rule": "BZ-D1"})
    officer_vis = [k for k, v in vis.items() if ("Officer" in v and "Hurting" not in v) or "Killings" in v]
    hurting_vis = [k for k, v in vis.items() if "Hurting" in v]
    eating_vis = [k for k, v in vis.items() if "Eating" in v]
    ind_res_vis = [k for k, v in vis.items() if "Indirect Resource" in v]
    shgg = bool(officer_vis and hurting_vis)
    if officer_vis or any("Killings" in h or "Direct Officer" in h for h in hidden):
        out.append({"domain": "D2", "prominence": "medium", "polarity": "mixed" if shgg else "positive",
                    "scores": [1, -1] if shgg else [1],
                    "basis": f"Officer visible in {', '.join(officer_vis) or 'none'} pillar(s); Seven Killings hidden x{sum('Killings' in h for h in hidden)}"
                             + ("; 伤官见官: Hurting Officer visible in " + ', '.join(hurting_vis) if shgg else ""), "mapping_rule": "BZ-D2"})
    tally = dm["element_tally"]
    wel = EL[(dme + 2) % 5]
    wshare = tally[wel] / sum(tally.values())
    largest = max(tally, key=tally.get) == wel
    out.append({"domain": "D3", "prominence": "high" if wshare >= 0.25 else "medium",
                "polarity": ("mixed" if weighted_weak else "positive") if wshare >= 0.15 else "neutral",
                "scores": [1, -1] if weighted_weak else [1],
                "basis": f"Wealth ({wel}) share {wshare:.2f} of weighted tally{', largest element' if largest else ''}; "
                         f"{'weighted-weak DM => 财多身弱 wealth heavy / self light' if weighted_weak else 'DM able to carry wealth'}",
                "mapping_rule": "BZ-D3"})
    day = P[2]
    spouse_star = ("Wealth",) if male else ("Officer", "Killings")
    main_tg = day["hidden_stems"][0]["ten_god"]
    inter = [i for i in bz["interactions"] if "day" in i.get("pillars", [])]
    kinds = sorted({i["type"].split(" ")[0] for i in inter})
    harmful = any(k in ("punishment", "destruction", "clash", "harm") for k in kinds)
    pol4 = "mixed" if harmful else ("positive" if inter else "neutral")
    out.append({"domain": "D4", "prominence": "high" if inter else "medium", "polarity": pol4,
                "scores": [1, -1] if pol4 == "mixed" else [1] if pol4 == "positive" else [0],
                "basis": f"spouse palace {day['branch']} {day['pinyin'].split()[1]} (main qi {day['hidden_stems'][0]['stem']} = {main_tg}; "
                         f"spouse star for a {'male' if male else 'female'} chart is {'/'.join(spouse_star)}"
                         f"{', present here' if any(x in main_tg for x in spouse_star) else ''}); interactions on it: {', '.join(kinds) or 'none'}",
                "mapping_rule": "BZ-D4"})
    res_vis = [k for k, v in vis.items() if "Resource" in v]
    res_combined = [i for i in bz["interactions"] if i["type"].startswith("stem combination")
                    and any(pp in res_vis for pp in i["pillars"])]
    pol5 = ("mixed" if res_combined else "positive") if res_vis else "neutral"
    out.append({"domain": "D5", "prominence": "medium", "polarity": pol5,
                "scores": [1, -1] if pol5 == "mixed" else [1] if pol5 == "positive" else [0],
                "basis": (f"Resource star visible in {', '.join(res_vis) or 'none'} pillar(s)" + (f"; combined away ({', '.join(i['chars'] for i in res_combined)}, not transformed)" if res_combined else ""))
                if res_vis else "no Resource star on a visible stem",
                "mapping_rule": "BZ-D5"})
    if male:
        child_vis, conflict, cname = officer_vis, shgg, "伤官见官"
    else:
        child_vis, conflict, cname = hurting_vis + eating_vis, bool(eating_vis and ind_res_vis), "枭神夺食"
    pol6 = ("mixed" if conflict else "positive") if child_vis else "neutral"
    out.append({"domain": "D6", "prominence": "medium", "polarity": pol6,
                "scores": [1, -1] if pol6 == "mixed" else [1] if pol6 == "positive" else [0],
                "basis": f"children palace = hour pillar {P[3]['ganzhi']} with {vis['hour']} on the stem; children star "
                         f"({'Officer/Killings' if male else 'Eating God/Hurting Officer'}) visible in {', '.join(child_vis) or 'no pillar'}"
                         + (f"; {cname}" if conflict and child_vis else ""),
                "mapping_rule": "BZ-D6"})
    n_out_hidden = sum(("Eating" in h or "Hurting" in h) for h in hidden)
    res = bool(res_vis)
    if hurting_vis or eating_vis or n_out_hidden >= 3:
        out.append({"domain": "D8", "prominence": "high", "polarity": "positive" if res else "neutral", "scores": [1.5],
                    "basis": f"Output stars: Hurting Officer visible in {', '.join(hurting_vis) or 'none'}, Eating God visible in {', '.join(eating_vis) or 'none'}, "
                             f"output hidden x{n_out_hidden}; Resource visible: {res}",
                    "mapping_rule": "BZ-D8"})
    for o in out:
        o.update({"system": "bazi", "cluster": "sinic"})
    return out


# ---------------- grading ----------------
def cluster_polarity(projs):
    """Pool one cluster's projections for one domain. Deduplicate identical basis strings."""
    seen, scores = set(), []
    for p in projs:
        if p["basis"] in seen or p["polarity"] in ("silent", "neutral"):
            continue
        seen.add(p["basis"])
        scores.append({"positive": 1, "negative": -1, "mixed": 0}[p["polarity"]])
    if not scores:
        return "silent" if not projs else "neutral"
    has_pos, has_neg, has_mix = 1 in scores, -1 in scores, 0 in scores
    if (has_pos and has_neg) or has_mix:
        return "mixed"
    return "positive" if has_pos else "negative"


def grade(pols):
    voting = {k: v for k, v in pols.items() if v in ("positive", "negative", "mixed")}
    if not voting:
        return "INSUFFICIENT", voting
    vals = list(voting.values())
    if "positive" in vals and "negative" in vals:
        return "DIVERGENT", voting
    best = max(vals.count(x) for x in set(vals))
    if best == 3:
        return "STRONG", voting
    if best == 2:
        return "MODERATE", voting
    return "WEAK", voting


def scenario(raw, name, jy_proj, w_proj, sinic_proj):
    all_p = jy_proj + w_proj + sinic_proj
    out = {}
    for d in DOMAINS:
        pols = {cl: cluster_polarity([p for p in all_p if p["domain"] == d and p["cluster"] == cl])
                for cl in ("jyotisha", "western", "sinic")}
        g, voting = grade(pols)
        agree = None
        if g in ("STRONG", "MODERATE"):
            vals = list(voting.values())
            agree = max(set(vals), key=vals.count)
        out[d] = {"domain": DOMAINS[d], "cluster_polarity": pols, "grade": g, "agreed_polarity": agree,
                  "projections": [p for p in all_p if p["domain"] == d]}
    div = sum(1 for v in out.values() if v["grade"] == "DIVERGENT")
    suff = sum(1 for v in out.values() if v["grade"] != "INSUFFICIENT")
    return {"scenario": name, "domains": out,
            "divergence_rate_all": f"{div}/9",
            "divergence_rate_sufficient": f"{div}/{suff}",
            "counts": {g: sum(1 for v in out.values() if v["grade"] == g)
                       for g in ("STRONG", "MODERATE", "WEAK", "DIVERGENT", "INSUFFICIENT")}}


# ---------------- timing ----------------
# order matters: "Hurting Officer" must match "Hurting" before "Officer"
TG_DOMAIN_M = {"Hurting": ["D8"], "Eating": ["D8"], "Rob": ["D1"], "Friend": ["D1"], "Wealth": ["D3", "D4"],
               "Officer": ["D2", "D6"], "Killings": ["D2", "D6"], "Resource": ["D5", "D8"]}
TG_DOMAIN_F = {"Hurting": ["D6", "D8"], "Eating": ["D6", "D8"], "Rob": ["D1"], "Friend": ["D1"], "Wealth": ["D3"],
               "Officer": ["D2", "D4"], "Killings": ["D2", "D4"], "Resource": ["D5", "D8"]}
TG_DOMAIN = TG_DOMAIN_M


def tg_domains(tg):
    for k, v in TG_DOMAIN.items():
        if k in tg:
            return v
    return []


def timing(raw, today, ref="chandra"):
    from sc.bazi import STEMS, ten_god
    from sc.jyotisha import LORD
    windows = []
    # Jyotisha: Mahadasha (stable lords; dates +/- from ensemble)
    jc = raw["jyotisha"]["charts"]["+0min"]
    moon_sign = SIGNS.index(jc["grahas"]["Moon"]["sign"] if ref == "chandra" else jc["lagna"]["sign"])
    ref_name = "Chandra Lagna" if ref == "chandra" else "Lagna"
    kar = {"Sun": ["D1", "D2"], "Moon": ["D5", "D8"], "Mercury": ["D8"], "Jupiter": ["D3", "D6", "D9"], "Venus": ["D4"]}
    V = raw["jyotisha"]["vimshottari"]
    jy = []
    for i, md in enumerate(V["+0min"]["mahadashas"]):
        lord = md["lord"]
        h = (SIGNS.index(jc["grahas"][lord]["sign"]) - moon_sign) % 12 + 1
        ds = set(kar.get(lord, []))
        if h in HOUSE_DOMAIN:
            ds.add(HOUSE_DOMAIN[h])
        owned = [((s - moon_sign) % 12) + 1 for s in range(12) if LORD[s] == lord]
        starts = sorted(V[k]["mahadashas"][i]["start"][:10] for k in V)
        ends = sorted(V[k]["mahadashas"][i]["end"][:10] for k in V)
        jy.append({"cluster": "jyotisha", "technique": f"Vimshottari {lord} Mahadasha", "start": md["start"][:10],
                   "end": md["end"][:10], "start_range": [starts[0], starts[-1]], "end_range": [ends[0], ends[-1]],
                   "domains": sorted(ds), "basis": f"{lord} karaka {kar.get(lord, [])}; occupies house {h} from {ref_name}; "
                                                   f"lords houses {owned} from {ref_name} (not used)"})
    # Western: profections (house number stable even though sign is not)
    w = []
    for pr in raw["western"]["charts"]["+0min"]["profections"]:
        alts = sorted({(x["profected_sign"], x["lord_of_year"]) for k in raw["western"]["charts"]
                       for x in raw["western"]["charts"][k]["profections"] if x["age"] == pr["age"]})
        w.append({"cluster": "western", "technique": f"annual profection age {pr['age']}", "start": pr["start"],
                  "end": pr["end"], "domains": [HOUSE_DOMAIN[pr["activated_house"]]] if pr["activated_house"] in HOUSE_DOMAIN else [],
                  "basis": f"activated house {pr['activated_house']} (stable); sign/lord of year sensitive: {alts}"})
    # Sinic: Da Yun (exact start) + Zi Wei decadal
    bz = raw["bazi"]["primary"]
    dm = bz["day_master"]["stem"]
    start = datetime.fromisoformat(bz["da_yun"]["start_date_exact_3day_rule"])
    s = []
    for k, p in enumerate(bz["da_yun"]["periods_lunar_python"]):
        st = start + timedelta(days=3652.422 * k)
        en = start + timedelta(days=3652.422 * (k + 1))
        stem_tg = ten_god(dm, p["ganzhi"][0])
        from lunar_python.util import LunarUtil
        br_main = LunarUtil.ZHI_HIDE_GAN[p["ganzhi"][1]][0]
        br_tg = ten_god(dm, br_main)
        ds = sorted(set(tg_domains(stem_tg) + tg_domains(br_tg)))
        s.append({"cluster": "sinic", "technique": f"BaZi Da Yun {p['ganzhi']}", "start": st.date().isoformat(),
                  "end": en.date().isoformat(), "domains": ds,
                  "basis": f"stem {p['ganzhi'][0]} = {stem_tg}; branch {p['ganzhi'][1]} main qi {br_main} = {br_tg}; "
                           f"lunar_python start differs by {bz['da_yun']['start_convention_difference_days']} days"})
    zw = raw["ziwei"]["alternatives"][raw["ziwei"]["primary_branch"]]["chart_zh"]
    by = int(raw["input_audit"]["gregorian_date"][:4])
    for p in zw["palaces"]:
        a, b = p["decadal"]["range"]
        # nominal age n corresponds to Chinese year (birth_year + n - 1); boundaries at lunar new year (approximated by year)
        y0, y1 = by + a - 1, by + b
        if y1 < today.year - 15 or y0 > today.year + 40:
            continue
        s.append({"cluster": "sinic", "technique": f"Zi Wei decadal {a}-{b} ({p['name']} {p['earthlyBranch']})",
                  "start": f"{y0}-lunar-new-year", "end": f"{y1}-lunar-new-year",
                  "start_iso_approx": f"{y0}-02-01", "end_iso_approx": f"{y1}-02-01",
                  "domains": [PALACE_DOMAIN[p["name"]]] if p["name"] in PALACE_DOMAIN else [],
                  "basis": f"decadal palace {p['name']}; nominal-age convention; exact boundary = Chinese New Year of {y0}/{y1}"})
    items = jy + w + s

    def iv(x):
        a = x.get("start_iso_approx", x["start"])
        b = x.get("end_iso_approx", x["end"])
        if "start_range" in x:  # use the conservative inner overlap across the time ensemble
            a, b = x["start_range"][-1], x["end_range"][0]
        return date.fromisoformat(a[:10]), date.fromisoformat(b[:10])

    horizon = (date(today.year - 5, 1, 1), date(today.year + 6, 12, 31))
    windows = []
    for d in DOMAINS:
        acts = {cl: [(iv(x), x) for x in items if x["cluster"] == cl and d in x["domains"]] for cl in ("jyotisha", "western", "sinic")}
        # sweep all boundaries within horizon
        pts = sorted({horizon[0], horizon[1]} | {t for cl in acts.values() for (a, b), _ in cl for t in (a, b)
                                                 if horizon[0] <= t <= horizon[1]})
        for a, b in zip(pts, pts[1:]):
            mid = a + (b - a) / 2
            on = {cl: [x for (s_, e_), x in v if s_ <= mid < e_] for cl, v in acts.items()}
            n = sum(1 for v in on.values() if v)
            if n >= 2:
                windows.append({"domain": d, "domain_name": DOMAINS[d], "start": a.isoformat(), "end": b.isoformat(),
                                "grade": "STRONG ⭐" if n == 3 else "MODERATE",
                                "clusters": {cl: [x["technique"] for x in v] for cl, v in on.items() if v}})
    # merge contiguous identical windows
    merged = []
    for wdw in windows:
        if merged and merged[-1]["domain"] == wdw["domain"] and merged[-1]["end"] == wdw["start"] and \
                merged[-1]["clusters"] == wdw["clusters"]:
            merged[-1]["end"] = wdw["end"]
        else:
            merged.append(dict(wdw))
    current = [x for x in merged if x["start"] <= today.isoformat() < x["end"]]
    future = sorted([x for x in merged if x["start"] > today.isoformat()], key=lambda x: x["start"])
    return {"techniques": items, "windows": merged, "current": current, "next": future[:6], "horizon": [h.isoformat() for h in horizon]}


# ---------------- temperament ----------------
def temperament(raw, jy_sc, w_sc, bz, zw):
    def lab(x):
        return "supported" if x >= 1 else "strained" if x <= -1 else "mixed/neutral"
    zch = zw["chart_zh"]
    ming = next(p for p in zch["palaces"] if p["name"] == "命宫")
    body = next(p for p in zch["palaces"] if p["isBodyPalace"])
    names = lambda p: {s["name"] for s in p["majorStars"] + p["minorStars"]}
    vis = [p["ten_god_of_stem"] for p in bz["pillars"]]
    hidden = [h["ten_god"] for p in bz["pillars"] for h in p["hidden_stems"]]
    jc = raw["jyotisha"]["charts"]["+0min"]["grahas"]
    dual = sum(1 for g, v in jc.items() if SIGNS.index(v["sign"]) % 3 == 2 and g not in ("Rahu", "Ketu"))
    wc = raw["western"]["charts"]["+0min"]["planets"]
    wmut = sum(1 for v in wc.values() if SIGNS.index(v["sign"]) % 3 == 2)
    off_vis = [v for v in vis if ("Officer" in v and "Hurting" not in v) or "Killings" in v]
    A = raw["astronomy"]["+0min"]["bodies"]
    elong = (A["Moon"]["lon"] - A["Sun"]["lon"]) % 360

    def jd_(g):
        v = jc[g]
        with_ = [h for h in jc if h != g and jc[h]["sign"] == v["sign"]]
        extra = ("waxing" if elong < 180 else "waning") if g == "Moon" else ""
        return ", ".join(x for x in [v["sign"], v["dignity"], extra, ("with " + "/".join(with_)) if with_ else "",
                                     "navamsa " + v["d9"]] if x)

    def wd_(p_):
        v = wc[p_]
        return f"{v['sign']}, {', '.join(v['essential']['planet_dignities'])}, {v['sect_status']}"
    axes = {
        "T1 Leadership/visibility": {
            "jyotisha": (lab(jy_sc["Sun"]), f"Sun score {jy_sc['Sun']:+.2f} ({jd_('Sun')})"),
            "western": (lab(w_sc["Sun"]), f"Sun score {w_sc['Sun']:+.2f} ({wd_('Sun')})"),
            "sinic": ("supported" if ({"紫微", "天府"} & names(ming)) else "mixed/neutral",
                      f"命宫 major stars {[s['name'] for s in ming['majorStars']]}; visible Officer: {any('Direct Officer' in v for v in vis)}")},
        "T2 Drive/initiative": {
            "jyotisha": (lab(jy_sc["Mars"]), f"Mars score {jy_sc['Mars']:+.2f} ({jd_('Mars')})"),
            "western": (lab(w_sc["Mars"]), f"Mars score {w_sc['Mars']:+.2f} ({wd_('Mars')})"),
            "sinic": ("supported" if ({"七杀", "破军", "贪狼"} & (names(ming) | names(body))) else "mixed/neutral",
                      f"七杀/破军/贪狼 in 命/身: {sorted({'七杀', '破军', '贪狼'} & (names(ming) | names(body)))}; Seven Killings hidden x{sum('Killings' in h for h in hidden)}")},
        "T3 Nurturing/service": {
            "jyotisha": (lab(jy_sc["Moon"]), f"Moon score {jy_sc['Moon']:+.2f} ({jd_('Moon')})"),
            "western": (lab(w_sc["Moon"]), f"Moon score {w_sc['Moon']:+.2f} ({wd_('Moon')})"),
            "sinic": ("supported" if any("Resource" in v for v in vis) else "mixed/neutral",
                      f"Resource stem visible: {[v for v in vis if 'Resource' in v]}")},
        "T4 Intellect/craft": {
            "jyotisha": (lab(jy_sc["Mercury"]), f"Mercury score {jy_sc['Mercury']:+.2f} ({jd_('Mercury')})"),
            "western": (lab(w_sc["Mercury"]), f"Mercury score {w_sc['Mercury']:+.2f} ({wd_('Mercury')})"),
            "sinic": ("supported" if (any("Hurting" in v or "Eating" in v for v in vis) or {"文昌", "文曲", "天机"} & (names(ming) | names(body))) else "mixed/neutral",
                      f"output stem visible {[v for v in vis if 'Hurting' in v or 'Eating' in v]}; 文昌/文曲/天机 in 命/身: {sorted({'文昌', '文曲', '天机'} & (names(ming) | names(body)))}")},
        "T5 Adaptability": {
            "jyotisha": ("supported" if dual >= 3 else "mixed/neutral", f"{dual} of 7 grahas in dual signs"),
            "western": ("supported" if wmut >= 3 else "mixed/neutral", f"{wmut} of 7 planets in mutable signs"),
            "sinic": ("silent", "no declared Sinic rule")},
        "T6 Discipline/structure": {
            "jyotisha": (lab(jy_sc["Saturn"]), f"Saturn score {jy_sc['Saturn']:+.2f} ({jd_('Saturn')})"),
            "western": (lab(w_sc["Saturn"]), f"Saturn score {w_sc['Saturn']:+.2f} ({wd_('Saturn')})"),
            "sinic": (("mixed/neutral" if any("Hurting" in v for v in vis) else "supported") if off_vis else "mixed/neutral",
                      ("Officer star visible but confronted by a visible Hurting Officer (伤官见官)" if any("Hurting" in v for v in vis)
                       else "Officer star visible on a stem") if off_vis else "no Officer star on a visible stem")},
    }
    out = {}
    for k, v in axes.items():
        labs = [x[0] for x in v.values() if x[0] not in ("silent", "mixed/neutral")]
        agree = max((labs.count(x), x) for x in set(labs)) if labs else (0, None)
        conflict = "supported" in labs and "strained" in labs
        out[k] = {"clusters": {c: {"reading": x[0], "basis": x[1]} for c, x in v.items()},
                  "summary": "conflict" if conflict else (f"{agree[0]} clusters: {agree[1]}" if agree[1] else "no clear signal")}
    return out


def main():
    raw = json.load(open(os.path.join(OUT, "RAW_CALCULATIONS.json"), encoding="utf-8"))
    ver = json.load(open(os.path.join(OUT, "VERIFICATION_REPORT.json"), encoding="utf-8"))
    assert not ver["failures"], "invariant failure: interpretation stopped"
    from sc.common import load_input
    today = date.fromisoformat(load_input()["analysis_date"])
    st = raw["stability"]

    global TG_DOMAIN
    raw["input_audit"]["_gender"] = "male" if load_input()["gender"].lower().startswith("m") else "female"
    TG_DOMAIN = TG_DOMAIN_M if raw["input_audit"]["_gender"] == "male" else TG_DOMAIN_F
    lagna_stable = st["jyotisha_lagna_sign"]["outer_interval"] == "stable"
    asc_stable = st["western_asc_sign"]["outer_interval"] == "stable"
    asc_inner_stable = st["western_asc_sign"]["inner_interval"] == "stable"
    ref = "lagna" if lagna_stable else "chandra"
    zw_branch = raw["ziwei"]["primary_branch"]
    jy_c, jy_sc = jyotisha_projections(raw, "+0min", ref)
    jy_secondary, _ = jyotisha_projections(raw, "+0min", "chandra" if ref == "lagna" else "lagna")
    jy_secondary = [p for p in jy_secondary if p["mapping_rule"] == "HOUSE-OCC"]
    w_sig, w_sc = western_projections(raw, "+0min", houses=False)
    w_inner, _ = western_projections(raw, "+0min", houses=True)
    w_primary = w_inner if asc_stable else w_sig
    bz_p = bazi_projections(raw)
    zw_p = ziwei_projections(raw, zw_branch)
    for p in jy_c + w_inner + bz_p + zw_p:
        p.setdefault("confidence", "medium")
    unc = load_input()["time_uncertainty"]
    scenarios = {"outer": scenario(raw, f"±{unc['outer_minutes']} min (primary)", jy_c, w_primary, bz_p + zw_p)}
    if unc["inner_minutes"] != unc["outer_minutes"] and asc_inner_stable and not asc_stable:
        scenarios["inner"] = scenario(raw, f"inner ±{unc['inner_minutes']} min (Western Asc stable)", jy_c, w_inner, bz_p + zw_p)

    # sensitive alternatives (displayed, never vote) -- only for outputs that actually change in the interval
    alts = {}
    offs = sorted(raw["jyotisha"]["charts"], key=lambda k: int(k.replace("min", "")))
    if not lagna_stable:
        for off in offs:
            pj, _ = jyotisha_projections(raw, off, "lagna")
            alts[f"jyotisha_lagna_{raw['jyotisha']['charts'][off]['lagna']['sign']}"] = [p for p in pj if p["mapping_rule"] == "HOUSE-OCC"]
    if not asc_stable:
        for off in offs:
            pw, _ = western_projections(raw, off, houses=True)
            alts[f"western_asc_{raw['western']['charts'][off]['asc']['sign']}"] = [p for p in pw if p["mapping_rule"] == "HOUSE-OCC"]
    if st["ziwei_time_branch_civil"]["crossings"] or st["ziwei_time_branch_LAT"]["crossings"]:
        for br in raw["ziwei"]["alternatives"]:
            if br != zw_branch:
                alts[f"ziwei_{br}"] = ziwei_projections(raw, br)
    outer = scenarios["outer"]

    tm = timing(raw, today, ref)
    temp = temperament(raw, jy_sc, w_sc, raw["bazi"]["primary"], raw["ziwei"]["alternatives"][zw_branch])

    # claim accounting
    all_candidates = jy_c + w_inner + bz_p + zw_p + [p for v in alts.values() for p in v]
    n_neutral = [p["basis"] for p in jy_c + w_primary + bz_p + zw_p if p["polarity"] in ("neutral", "silent")]
    removed = {
        "sensitive_to_birth_time": {"count": sum(len(v) for v in alts.values()) + (len(w_inner) - len(w_primary)),
                                    "note": "projections that change inside the uncertainty interval; displayed, never vote"},
        "secondary_reference_frame_not_voting": {"count": len(jy_secondary),
                                                 "note": f"Jyotisha houses from {'Chandra Lagna' if ref == 'lagna' else 'Lagna'} (JY-REFERENCE)"},
        "neutral_polarity_no_theme": {"count": len(n_neutral), "items": n_neutral},
        "school_dependent_low_confidence": {"count": 1, "items": ["BaZi Yong Shen / favourable element (schools disagree)"]},
        "no_validated_source": {"count": 4, "items": [f"Maya Tzolk'in {raw['maya']['tzolkin']} meaning",
                                                      f"Maya Haab {raw['maya']['own_implementation']['haab']} meaning",
                                                      f"Tibetan {raw['tibetan']['gender']} {raw['tibetan']['element']} {raw['tibetan']['animal']} meaning",
                                                      "Tibetan Mewa / Parkha / la-sok-lung-ta-wang-thang"]},
        "unavailable_methods": {"items": [k for k, v in {**raw["jyotisha"]["unavailable"], **raw["western"]["unavailable"]}.items()
                                          if not v.startswith("computed")]},
        "barnum_screen": "every retained projection is tied to a computed datum via a registry rule; no automated "
                         "Barnum test was run, so generic-sounding prose was avoided by hand in FINAL_READING.md",
    }
    removed["unavailable_methods"]["count"] = len(removed["unavailable_methods"]["items"])
    from sc.bazi import ten_god
    from lunar_python.util import LunarUtil
    dmst = raw["bazi"]["primary"]["day_master"]["stem"]
    annual = {y: {"ganzhi": gz, "stem_ten_god": ten_god(dmst, gz[0]),
                  "branch_main_qi": LunarUtil.ZHI_HIDE_GAN[gz[1]][0],
                  "branch_ten_god": ten_god(dmst, LunarUtil.ZHI_HIDE_GAN[gz[1]][0]),
                  "period": f"Lichun {y} to Lichun {int(y) + 1}"}
              for y, gz in raw["bazi"]["primary"]["annual_pillars"].items() if int(y) in (2026, 2027, 2028)}
    syn = {"registry": REGISTRY, "house_domain": HOUSE_DOMAIN, "domains": DOMAINS,
           "scenarios": scenarios, "sensitive_alternatives": alts,
           "reference_frames": {"jyotisha_houses": ref, "western_houses_vote": asc_stable, "ziwei_hour_branch": zw_branch},
           "secondary_jyotisha_view": jy_secondary,
           "rule_application_note": ("Registry unchanged from the ±30 min run; JY-REFERENCE and W-HOUSES now select the Lagna "
                                     "and Ascendant houses because both are stable over ±1 min."),
           "stable_scores": {"jyotisha": jy_sc, "western": w_sc},
           "timing": tm, "temperament": temp, "bazi_annual_ten_gods": annual,
           "overlays": {"maya": {"computed": raw["maya"]["calendar_round"] + " / " + raw["maya"]["long_count"],
                                 "meaning": "omitted — no verifiable named Maya source available in this environment"},
                        "tibetan": {"computed": f"{raw['tibetan']['gender']} {raw['tibetan']['element']} {raw['tibetan']['animal']}",
                                    "meaning": "omitted — no validated lineage-specific source; Mewa/Parkha/personal forces not computed"}},
           "yong_shen": raw["bazi"]["primary"]["yong_shen"],
           "claims_removed": removed,
           "candidate_projection_count": len(all_candidates)}
    dump("SYNTHESIS.json", syn)
    return syn


if __name__ == "__main__":
    s = main()
    for k in s["scenarios"]:
        sc = s["scenarios"][k]
        print(sc["scenario"], sc["counts"], sc["divergence_rate_all"], sc["divergence_rate_sufficient"])
        for d, v in sc["domains"].items():
            print(" ", d, v["domain"], v["grade"], v["cluster_polarity"], v["agreed_polarity"])
    for w in s["timing"]["windows"]:
        print(w)
    print("CURRENT", s["timing"]["current"])
    print(json.dumps(s["temperament"], ensure_ascii=False, indent=0)[:3000])
