"""Step 4F (Maya calendar, GMT 584283) and 4G (Tibetan element-animal year only)."""
from convertdate import gregorian, mayan

GMT = 584283
TZOLKIN = ["Imix", "Ik'", "Ak'bal", "K'an", "Chikchan", "Kimi", "Manik'", "Lamat", "Muluk", "Ok",
           "Chuwen", "Eb", "Ben", "Ix", "Men", "Kib", "Kaban", "Etz'nab", "Kawak", "Ajaw"]
HAAB = ["Pop", "Wo'", "Sip", "Sotz'", "Sek", "Xul", "Yaxk'in", "Mol", "Ch'en", "Yax", "Sak'", "Keh",
        "Mak", "K'ank'in", "Muwan", "Pax", "K'ayab", "Kumk'u", "Wayeb'"]


def own_maya(jdn):
    days = jdn - GMT
    b, r = divmod(days, 144000)
    k, r = divmod(r, 7200)
    t, r = divmod(r, 360)
    w, ki = divmod(r, 20)
    tz_num = (days + 3) % 13 + 1           # 13.0.0.0.0 = 4 Ajaw
    tz_name = TZOLKIN[(days + 19) % 20]
    hd = (days + 348) % 365                 # 13.0.0.0.0 = 8 Kumk'u
    return {"long_count": [b, k, t, w, ki], "tzolkin": [tz_num, tz_name], "haab": [hd % 20, HAAB[hd // 20]]}


def maya(y, m, d, after_sunrise=True):
    jdn = int(gregorian.to_jd(y, m, d) + 0.5)
    lc = mayan.from_gregorian(y, m, d)
    tz = mayan.to_tzolkin(gregorian.to_jd(y, m, d))
    hb = mayan.to_haab(gregorian.to_jd(y, m, d))
    back = mayan.to_gregorian(*lc)
    own = own_maya(jdn)
    own_back_jdn = GMT + own["long_count"][0] * 144000 + own["long_count"][1] * 7200 + \
        own["long_count"][2] * 360 + own["long_count"][3] * 20 + own["long_count"][4]
    return {
        "correlation_constant": "GMT 584283 (convertdate default; own implementation uses the same constant explicitly)",
        "note": ("Date-based. Maya days traditionally begin at sunrise in some communities; this birth is after sunrise, "
                 "so the civil date and a sunrise-based day agree." if after_sunrise else
                 "Date-based. This birth is before sunrise: a sunrise-based day count would assign the previous day."),
        "julian_day_number": jdn,
        "long_count": ".".join(map(str, lc)),
        "tzolkin": f"{tz[0]} {tz[1]}",
        "haab": f"{hb[0]} {hb[1]}",
        "calendar_round": f"{tz[0]} {tz[1]} {hb[0]} {hb[1]}",
        "own_implementation": {"long_count": ".".join(map(str, own["long_count"])),
                               "tzolkin": f"{own['tzolkin'][0]} {own['tzolkin'][1]}",
                               "haab": f"{own['haab'][0]} {own['haab'][1]}"},
        "round_trip_convertdate": list(back),
        "round_trip_ok": tuple(back) == (y, m, d) and own_back_jdn == jdn,
        "engines_agree": ".".join(map(str, lc)) == ".".join(map(str, own["long_count"])) and
        tz[0] == own["tzolkin"][0] and tz[1] == own["tzolkin"][1] and hb[0] == own["haab"][0] and
        list(mayan.HAAB).index(hb[1]) == HAAB.index(own["haab"][1]),
    }


def tibetan(y, m, d):
    cyc = (y - 4) % 60
    elements = ["Wood", "Fire", "Earth", "Iron", "Water"]
    animals = ["Mouse", "Ox", "Tiger", "Hare", "Dragon", "Snake", "Horse", "Sheep", "Monkey", "Bird", "Dog", "Pig"]
    return {
        "element": elements[(cyc % 10) // 2], "animal": animals[cyc % 12],
        "gender": "Male" if cyc % 2 == 0 else "Female",
        "sexagenary_index_1based": cyc + 1,
        "losar_boundary_check": ("Losar (Phugpa and Tsurphu) always falls between late January and late March. "
                                 f"A birth on {y}-{m:02d}-{d:02d} is after any possible Losar of {y}, so the "
                                 "element-animal year is unambiguous without a lineage-specific calendar engine."),
        "omitted": {
            "mewa": "no validated lineage-specific implementation available",
            "parkha": "no validated implementation available",
            "la_sok_lung_ta_wang_thang": "life/body/power/wind-horse/soul-force anchors not validated -> omitted",
            "tibetan_year_number_and_rabjung": "not computed by a validated engine -> omitted",
        },
        "status": "limited symbolic overlay; contributes no domain votes",
    }
