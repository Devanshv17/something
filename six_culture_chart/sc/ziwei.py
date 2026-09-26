"""Step 4E: Zi Wei Dou Shu via canonical iztro (npm) with py-iztro interface cross-check (same method)."""
import json
import os
import subprocess

from .common import ROOT

MAJOR14 = {"紫微", "天机", "太阳", "武曲", "天同", "廉贞", "天府", "太阴", "贪狼", "巨门",
           "天相", "天梁", "七杀", "破军"}
TIME_INDEX = {"辰": 4, "巳": 5}


def canonical(date_str, time_index, gender_zh, lang="zh-CN", hdates=()):
    out = subprocess.run(["node", os.path.join(ROOT, "js", "ziwei.js"), date_str, str(time_index), gender_zh, lang,
                          *hdates], capture_output=True, text=True, check=True, cwd=os.path.join(ROOT, "js"))
    return json.loads(out.stdout)


def wrapper(date_str, time_index, gender_zh):
    from py_iztro import Astro
    a = Astro().by_solar(date_str, time_index, gender_zh)
    d = a.model_dump()
    return {"soul": d.get("soul"), "body": d.get("body"), "five": d.get("five_elements_class"),
            "palaces": [{"name": p["name"], "branch": p["earthly_branch"],
                         "major": sorted(s["name"] for s in p["major_stars"]),
                         "mutagens": sorted(s["name"] + s["mutagen"] for s in p["major_stars"] + p["minor_stars"]
                                            if s.get("mutagen"))}
                        for p in d["palaces"]]}


def invariants(chart):
    pal = chart["palaces"]
    names = [p["name"] for p in pal]
    branches = [p["earthlyBranch"] for p in pal]
    majors = [s["name"] for p in pal for s in p["majorStars"]]
    mut = [s["name"] + s["mutagen"] for p in pal for s in p["majorStars"] + p["minorStars"] if s.get("mutagen")]
    zw = next(p["earthlyBranch"] for p in pal if any(s["name"] == "紫微" for s in p["majorStars"]))
    tf = next(p["earthlyBranch"] for p in pal if any(s["name"] == "天府" for s in p["majorStars"]))
    order = "子丑寅卯辰巳午未申酉戌亥"
    # Zi Wei and Tian Fu are mirror images about the 寅-申 axis: idx(ZW)+idx(TF) == 4 (mod 12)
    zwtf = (order.index(zw) + order.index(tf)) % 12 == 4
    return [
        {"invariant": "12 unique palace names", "pass": len(set(names)) == 12, "value": len(set(names))},
        {"invariant": "12 unique earthly branches", "pass": len(set(branches)) == 12},
        {"invariant": "14 major stars each placed exactly once", "pass": sorted(majors) == sorted(MAJOR14)},
        {"invariant": "four transformations present (禄权科忌 once each)",
         "pass": sorted(m[-1] for m in mut) == sorted("禄权科忌"), "value": mut},
        {"invariant": "Zi Wei / Tian Fu mirror about Yin-Shen axis", "pass": zwtf, "value": [zw, tf]},
        {"invariant": "decadal ranges contiguous 10-year blocks",
         "pass": sorted(p["decadal"]["range"][0] for p in pal) ==
         list(range(min(p["decadal"]["range"][0] for p in pal), min(p["decadal"]["range"][0] for p in pal) + 120, 10))},
    ]


def compute(date_str, hdates):
    res = {"implementation": "iztro (npm, canonical JS) + py-iztro 0.1.5 wrapper (bundles iztro 2.5.0) -- ONE method",
           "configuration": {"calendar": "solar date input -> iztro lunar conversion", "fixLeap": True,
                             "day_boundary": "iztro default (civil midnight; 23:00-24:00 = late Zi index 12)",
                             "time_index_source": "civil clock hour (IST); LAT variant evaluated in boundary audit",
                             "gender_encoding": "男 (male)", "direction_rule": "iztro default: yang-male forward",
                             "age_convention": "nominal (虚岁) age as used by iztro",
                             "month_note": "Zi Wei uses the lunar month (三月 -> 戊辰 in iztro chineseDate); BaZi uses the solar-term month (己巳). Both are correct within their own convention."},
           "alternatives": {}}
    for br, ti in TIME_INDEX.items():
        zh = canonical(date_str, ti, "男", "zh-CN", hdates)
        en = canonical(date_str, ti, "male", "en-US", hdates)
        wr = wrapper(date_str, ti, "男")
        cmp_ = []
        for p, w in zip(zh["palaces"], wr["palaces"]):
            same = (p["name"] == w["name"] and p["earthlyBranch"] == w["branch"] and
                    sorted(s["name"] for s in p["majorStars"]) == w["major"])
            cmp_.append({"palace": p["name"], "match": same})
        res["alternatives"][br] = {"time_index": ti, "chart_zh": zh, "chart_en": en,
                                   "wrapper_vs_canonical": {"all_match": all(c["match"] for c in cmp_),
                                                            "soul_body_five_match": [zh["soul"], zh["body"], zh["fiveElementsClass"]] ==
                                                            [wr["soul"], wr["body"], wr["five"]],
                                                            "palaces": cmp_},
                                   "invariants": invariants(zh)}
    return res
