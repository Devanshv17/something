"""Step 4C: BaZi. Primary engine lunar_python; validator sxtwl (independent codebase) + Swiss Ephemeris solar terms."""
from datetime import datetime, timedelta, timezone

import sxtwl
import swisseph as swe
from lunar_python import Solar

from .astro import solar_longitude_crossing, skyfield_solar_longitude_crossing
from .common import jd_from_utc, utc_from_jd

STEMS = "甲乙丙丁戊己庚辛壬癸"
BRANCHES = "子丑寅卯辰巳午未申酉戌亥"
STEM_PY = ["Jia", "Yi", "Bing", "Ding", "Wu", "Ji", "Geng", "Xin", "Ren", "Gui"]
BRANCH_PY = ["Zi", "Chou", "Yin", "Mao", "Chen", "Si", "Wu", "Wei", "Shen", "You", "Xu", "Hai"]
EL = ["Wood", "Fire", "Earth", "Metal", "Water"]
STEM_EL = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4]
BRANCH_EL = [4, 2, 0, 0, 2, 1, 1, 2, 3, 3, 2, 4]
CST = timezone(timedelta(hours=8))

STEM_COMBOS = {frozenset("甲己"): "Earth", frozenset("乙庚"): "Metal", frozenset("丙辛"): "Water",
               frozenset("丁壬"): "Wood", frozenset("戊癸"): "Fire"}
SIX_COMBOS = {frozenset("子丑"): "Earth", frozenset("寅亥"): "Wood", frozenset("卯戌"): "Fire",
              frozenset("辰酉"): "Metal", frozenset("巳申"): "Water", frozenset("午未"): "Fire/Earth"}
CLASHES = [frozenset(x) for x in ("子午", "丑未", "寅申", "卯酉", "辰戌", "巳亥")]
HARMS = [frozenset(x) for x in ("子未", "丑午", "寅巳", "卯辰", "申亥", "酉戌")]
DESTRUCTIONS = [frozenset(x) for x in ("子酉", "午卯", "巳申", "寅亥", "辰丑", "戌未")]
PUNISH_GROUPS = [("寅巳申", "ungrateful punishment 无恩之刑"), ("丑戌未", "bullying punishment 恃势之刑"),
                 ("子卯", "uncivil punishment 无礼之刑")]
SELF_PUNISH = "辰午酉亥"
TRINES = {"申子辰": "Water", "亥卯未": "Wood", "寅午戌": "Fire", "巳酉丑": "Metal"}


def ten_god(dm, stem):
    a, b = STEMS.index(dm), STEMS.index(stem)
    ea, eb = STEM_EL[a], STEM_EL[b]
    same = (a % 2) == (b % 2)
    rel = (eb - ea) % 5
    return {0: ("比肩 Friend", "劫财 Rob Wealth"), 1: ("食神 Eating God", "伤官 Hurting Officer"),
            2: ("偏财 Indirect Wealth", "正财 Direct Wealth"), 3: ("七杀 Seven Killings", "正官 Direct Officer"),
            4: ("偏印 Indirect Resource", "正印 Direct Resource")}[rel][0 if same else 1]


def pillars_lunar_python(local_naive):
    s = Solar.fromYmdHms(local_naive.year, local_naive.month, local_naive.day,
                         local_naive.hour, local_naive.minute, local_naive.second)
    ec = s.getLunar().getEightChar()
    ec.setSect(2)  # day pillar changes at 00:00; 23:00-24:00 is late Zi of the same day
    return ec, [ec.getYear(), ec.getMonth(), ec.getDay(), ec.getTime()]


def pillars_sxtwl(local_naive):
    d = sxtwl.fromSolar(local_naive.year, local_naive.month, local_naive.day)
    gz = lambda g: STEMS[g.tg] + BRANCHES[g.dz]
    return [gz(d.getYearGZ()), gz(d.getMonthGZ()), gz(d.getDayGZ()), gz(d.getHourGZ(local_naive.hour))]


def solar_terms(birth_utc):
    """Sectional terms (jie) bracketing the birth: 立夏 45 deg, 芒种 75 deg."""
    out = {}
    lp_table = Solar.fromYmd(birth_utc.year, 5, 17).getLunar().getJieQiTable()
    sx = {x.jqIndex: x.jd for x in sxtwl.getJieQiByYear(birth_utc.year)}
    for name, py, lon, sx_idx in (("立夏", "Lixia (Start of Summer)", 45.0, 9),
                                  ("芒种", "Mangzhong (Grain in Ear)", 75.0, 11)):
        guess = jd_from_utc(birth_utc) + (lon - 56.6) / 0.97
        jd = solar_longitude_crossing(lon, guess)
        se = utc_from_jd(jd)
        sk = skyfield_solar_longitude_crossing(lon, se)
        lpv = datetime.strptime(lp_table[name].toYmdHms(), "%Y-%m-%d %H:%M:%S").replace(tzinfo=CST)
        sxv = utc_from_jd(sx[sx_idx] - 8 / 24)  # sxtwl JD is in Beijing time
        out[name] = {"pinyin": py, "sun_longitude": lon,
                     "swiss_ephemeris_utc": se.isoformat(timespec="seconds"),
                     "skyfield_jpl_utc": sk.isoformat(timespec="seconds"),
                     "lunar_python_utc": lpv.astimezone(timezone.utc).isoformat(timespec="seconds"),
                     "sxtwl_utc": sxv.isoformat(timespec="seconds"),
                     "max_difference_s": max(abs((a - b).total_seconds()) for a in (se, sk, lpv, sxv)
                                             for b in (se, sk, lpv, sxv)),
                     "_utc": se}
    return out


def interactions(pillars):
    names = ["year", "month", "day", "hour"]
    st = [p[0] for p in pillars]
    br = [p[1] for p in pillars]
    out = []
    for i in range(4):
        for j in range(i + 1, 4):
            ss, bb = frozenset(st[i] + st[j]), frozenset(br[i] + br[j])
            adj = j == i + 1
            if ss in STEM_COMBOS:
                out.append({"type": "stem combination 天干五合", "pillars": [names[i], names[j]],
                            "chars": st[i] + st[j], "potential_element": STEM_COMBOS[ss], "adjacent": adj})
            if len(bb) == 2:
                if bb in SIX_COMBOS:
                    out.append({"type": "six combination 六合", "pillars": [names[i], names[j]],
                                "chars": br[i] + br[j], "potential_element": SIX_COMBOS[bb], "adjacent": adj})
                if bb in CLASHES:
                    out.append({"type": "clash 六冲", "pillars": [names[i], names[j]], "chars": br[i] + br[j]})
                if bb in HARMS:
                    out.append({"type": "harm 六害", "pillars": [names[i], names[j]], "chars": br[i] + br[j]})
                if bb in DESTRUCTIONS:
                    out.append({"type": "destruction 六破", "pillars": [names[i], names[j]], "chars": br[i] + br[j]})
                for grp, label in PUNISH_GROUPS:
                    if bb <= set(grp):
                        out.append({"type": f"punishment (partial, {len(bb)} of {len(grp)}) {label}",
                                    "pillars": [names[i], names[j]], "chars": br[i] + br[j]})
            elif br[i] in SELF_PUNISH:
                out.append({"type": "self-punishment 自刑", "pillars": [names[i], names[j]], "chars": br[i] + br[j]})
    present = set(br)
    for trio, el in TRINES.items():
        have = present & set(trio)
        if len(have) >= 2:
            out.append({"type": "three-harmony (partial)" if len(have) == 2 else "three-harmony",
                        "chars": "".join(sorted(have, key=trio.index)), "element": el,
                        "note": "half-combination requires the middle branch in most schools" if len(have) == 2 else ""})
    # Transformation check (declared rule BZ-TR-1): a combination transforms only if adjacent AND the month
    # branch's element equals the potential element. Otherwise reported as 'combined, not transformed'.
    mel = EL[BRANCH_EL[BRANCHES.index(br[1])]]
    for x in out:
        if "potential_element" in x:
            x["transformed"] = bool(x.get("adjacent")) and x["potential_element"] == mel
            x["transformation_rule"] = f"BZ-TR-1: adjacent and month-branch element == potential element (month element is {mel})"
    return out


def dm_strength(pillars, hidden):
    """Declared rule BZ-DM-1 (weighted count). Visible stems 1.0; hidden main/middle/residual 1.0/0.5/0.3;
    month branch hidden stems x2 (month command). Support = companion + resource elements."""
    dm = pillars[2][0]
    dme = STEM_EL[STEMS.index(dm)]
    support_els = {dme, (dme - 1) % 5}
    tally = {e: 0.0 for e in EL}
    rows = []
    for i, p in enumerate(pillars):
        if i != 2:
            e = STEM_EL[STEMS.index(p[0])]
            tally[EL[e]] += 1.0
            rows.append((p[0], "visible", 1.0))
        for k, h in enumerate(hidden[i]):
            w = [1.0, 0.5, 0.3][k] * (2 if i == 1 else 1)
            tally[EL[STEM_EL[STEMS.index(h)]]] += w
            rows.append((h, f"hidden-{['main', 'middle', 'residual'][k]}-{['year', 'month', 'day', 'hour'][i]}", w))
    total = sum(tally.values())
    support = sum(tally[EL[e]] for e in support_els)
    month_el = BRANCH_EL[BRANCHES.index(pillars[1][1])]
    seasonal = ("prosperous 旺 (month element = DM element)" if month_el == dme else
                "strong 相 (month produces DM)" if month_el == (dme - 1) % 5 else
                "weakened (month drains/controls/is controlled)")
    share = support / total
    return {"rule": "BZ-DM-1", "day_master": dm, "element_tally": tally, "support_share": share,
            "weighted_count_verdict": "strong" if share > 0.55 else "weak" if share < 0.45 else "balanced",
            "seasonal_verdict": seasonal, "rows": rows,
            "rooting": [["year", "month", "day", "hour"][i] for i in range(4)
                        if any(STEM_EL[STEMS.index(h)] == dme for h in hidden[i])]}


def compute(local_civil, local_lat, birth_utc, gender_code=1):
    tracks = {}
    for label, t in (("civil_clock", local_civil), ("local_apparent_solar_time", local_lat)):
        ec, p = pillars_lunar_python(t)
        tracks[label] = {"input_time": t.isoformat(timespec="seconds"), "pillars": p,
                         "sxtwl_pillars": pillars_sxtwl(t)}
    ec, p = pillars_lunar_python(local_civil)
    hidden = [ec.getYearHideGan(), ec.getMonthHideGan(), ec.getDayHideGan(), ec.getTimeHideGan()]
    dm = p[2][0]
    pillars = []
    for i, (name, gz) in enumerate(zip(["year", "month", "day", "hour"], p)):
        s, b = gz[0], gz[1]
        pillars.append({"pillar": name, "ganzhi": gz,
                        "pinyin": f"{STEM_PY[STEMS.index(s)]} {BRANCH_PY[BRANCHES.index(b)]}",
                        "stem": s, "stem_element": EL[STEM_EL[STEMS.index(s)]],
                        "stem_polarity": "Yang" if STEMS.index(s) % 2 == 0 else "Yin",
                        "branch": b, "branch_element": EL[BRANCH_EL[BRANCHES.index(b)]],
                        "hidden_stems": [{"stem": h, "element": EL[STEM_EL[STEMS.index(h)]],
                                          "ten_god": ten_god(dm, h)} for h in hidden[i]],
                        "ten_god_of_stem": "日主 Day Master" if name == "day" else ten_god(dm, s),
                        "na_yin_traditional_attribute": [ec.getYearNaYin(), ec.getMonthNaYin(),
                                                         ec.getDayNaYin(), ec.getTimeNaYin()][i]})
    terms = solar_terms(birth_utc)
    yun = ec.getYun(gender_code)
    dayun = [{"start_year": d.getStartYear(), "end_year": d.getEndYear(), "start_age_virtual": d.getStartAge(),
              "ganzhi": d.getGanZhi()} for d in yun.getDaYun()[:10]]
    # Own Da Yun start: forward (male + yang year stem) => to next jie; 3 days = 1 year
    yang_year = STEMS.index(p[0][0]) % 2 == 0
    forward = (gender_code == 1) == yang_year
    nxt = terms["芒种"]["_utc"] if forward else terms["立夏"]["_utc"]
    days = abs((nxt - birth_utc).total_seconds()) / 86400
    years = days / 3
    own_start = birth_utc + timedelta(days=years * 365.2422)
    return {
        "primary_track": "civil_clock (IST) with lunar_python sect=2; local-apparent-solar-time track retained",
        "tracks": tracks,
        "pillars": pillars,
        "day_master": {"stem": dm, "element": EL[STEM_EL[STEMS.index(dm)]], "polarity": "Yang"},
        "solar_terms": {k: {kk: vv for kk, vv in v.items() if kk != "_utc"} for k, v in terms.items()},
        "birth_after_lixia_days": (birth_utc - terms["立夏"]["_utc"]).total_seconds() / 86400,
        "birth_before_mangzhong_days": (terms["芒种"]["_utc"] - birth_utc).total_seconds() / 86400,
        "interactions": interactions(p),
        "dm_strength": dm_strength(p, hidden),
        "da_yun": {
            "direction": "forward" if forward else "backward",
            "direction_rule": "male + yang year stem => forward",
            "days_to_next_sectional_term": days,
            "start_offset_years_exact_3day_rule": years,
            "start_date_exact_3day_rule": own_start.date().isoformat(),
            "lunar_python_start": {"years": yun.getStartYear(), "months": yun.getStartMonth(),
                                   "days": yun.getStartDay(), "date": yun.getStartSolar().toYmd()},
            "start_convention_difference_days": abs((own_start.date() - datetime.strptime(
                yun.getStartSolar().toYmd(), "%Y-%m-%d").date()).days),
            "periods_lunar_python": [d for d in dayun if d["ganzhi"]],
        },
        "annual_pillars": {str(y): Solar.fromYmd(y, 7, 1).getLunar().getYearInGanZhiExact() for y in range(2024, 2031)},
        "_term_objs": terms,
    }


def yong_shen(bz):
    dm = bz["dm_strength"]
    return {
        "schools": [
            {"school": "调候 Seasonal regulation (Qiong Tong Bao Jian, Bing fire born in Si month)",
             "rule_chain": ["Day Master 丙 Bing, month branch 巳 Si (early summer, fire at peak)",
                            "Qiong Tong Bao Jian for 丙 in 四月: 壬 Ren water as primary, 庚 Geng metal as assistant"],
             "useful": ["Water (壬)", "Metal (庚)"],
             "presence": "壬 appears only as hidden stem in both 申; 庚 is main qi of both 申; visible water stem is 癸 not 壬"},
            {"school": "扶抑 Strength-balancing (rule BZ-DM-1)",
             "rule_chain": [f"weighted support share {dm['support_share']:.3f} -> {dm['weighted_count_verdict']}",
                            f"seasonal status: {dm['seasonal_verdict']}",
                            "the two sub-verdicts disagree" if (dm['weighted_count_verdict'] == 'weak') ==
                            ('旺' in dm['seasonal_verdict'] or '相' in dm['seasonal_verdict']) else "sub-verdicts agree"],
             "useful": (["Wood (resource)", "Fire (companion)"] if dm["weighted_count_verdict"] == "weak"
                        else ["Earth", "Metal", "Water"] if dm["weighted_count_verdict"] == "strong" else ["undetermined"]),
             },
        ],
        "confidence": "low",
        "agreement": "schools disagree unless both point to water/metal; see rule chains",
    }
