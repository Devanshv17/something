"""Life Map: a readable HTML reading built from output/*.json.

Every interpretive block is keyed to a domain and guarded by the grade/polarity it was written for; if the data
changes, the prose is withheld instead of going stale. Every claim links to the JSON path it came from.
Run after render.py:  .venv/bin/python render_html.py
"""
import html
import json
import math
import os
from datetime import date

from sc.common import OUT, ROOT, SIGNS

J = lambda n: json.load(open(os.path.join(OUT, n), encoding="utf-8"))
E = html.escape
GH = "https://github.com/devanshv17/something/blob/claude/six-culture-verified-chart-j5znid/six_culture_chart/output/"

SYS_LABEL = {"jyotisha": "Vedic", "western": "Western", "bazi": "BaZi", "ziwei": "Zi Wei", "sinic": "Chinese"}
POL_LABEL = {"positive": "supportive", "negative": "strained", "mixed": "double-edged", "neutral": "neutral",
             "silent": "silent"}
GRADE_LABEL = {"STRONG": "All three agree", "MODERATE": "Two agree", "WEAK": "One voice", "DIVERGENT": "Systems disagree",
               "INSUFFICIENT": "No basis"}
DOMAIN_TITLE = {"D1": "Who you are", "D2": "Work & public life", "D3": "Money & gains", "D4": "Partnership",
                "D5": "Home & roots", "D6": "Children & creation", "D7": "Daily rhythm", "D8": "Mind & craft",
                "D9": "Meaning & luck"}

# Interpretive text. Each entry states the grade and cluster polarities it was written against.
NARRATIVE = {
    "D1": {
        "expect": ("MODERATE", {"jyotisha": "negative", "western": "negative", "sinic": "mixed"}),
        "headline": "A protective, sensitive front, with confidence you build rather than inherit.",
        "traditions": [
            ("jyotisha", "Both zodiacs put Cancer on your eastern horizon, a sign ruled by the Moon. The Sun, the classical marker of confidence and authority, sits in Taurus, a sign ruled by its enemy Venus. Vedic texts read this as self-assurance that has to be earned."),
            ("western", "Mars (in its fall) and Saturn (in its detriment) both sit in your first house, the house of body and self-presentation. Hellenistic authors read two planets in poor condition here as friction in how drive and discipline come out."),
            ("sinic", "Your BaZi Day Master is 丙, Yang Fire, the image of the sun. It is born in its own season and rooted twice, yet the rest of the chart outweighs it by count. The two measures disagree, so the Chinese systems stay neutral here."),
        ],
        "practice": [
            "Traditional readers would expect a guarded, caring first impression, with force showing up later.",
            "Mars in Cancer is classically read as indirect drive: holding back, then acting all at once.",
            "Saturn rising is traditionally read as early seriousness and self-criticism that matures into staying power.",
        ],
        "reflect": ["Where do you hold back first and push later?", "Which kinds of confidence have you had to build on purpose?"],
    },
    "D2": {
        "expect": ("WEAK", {"jyotisha": "negative", "western": "neutral", "sinic": "mixed"}),
        "headline": "Work is a loud theme in the Vedic chart and a conflicted one in the Chinese charts.",
        "traditions": [
            ("jyotisha", "The Moon, Mercury and Rahu all sit in the 10th house from your Lagna, the career house. Three planets there make work very prominent. The registry scores it negative because Rahu counts as a malefic and the Moon is waning. Many Vedic astrologers instead read Rahu in the 10th as hungry, unconventional ambition. Both readings agree it is prominent."),
            ("sinic", "BaZi has a Direct Officer (structure, authority) on the hour stem facing a Hurting Officer (talent that questions rules) on the month stem. The classical name is 伤官见官. Zi Wei's career palace holds 天相 in a weak position with 擎羊 and 铃星."),
            ("western", "The Sun is peregrine (no dignity) in Taurus, so the Western signal is neutral."),
        ],
        "practice": [
            "Tradition would expect work to matter a great deal to you, and rigid hierarchies to chafe.",
            "The BaZi picture fits skill-led, independent roles better than rank-led ones.",
        ],
        "reflect": ["When have rules helped your work, and when have they blocked it?"],
    },
    "D3": {
        "expect": ("MODERATE", {"jyotisha": "mixed", "western": "positive", "sinic": "mixed"}),
        "headline": "Money is one of the loudest themes in your chart, and it cuts both ways.",
        "traditions": [
            ("jyotisha", "Jupiter, the great benefic, sits strong in your 2nd house (savings, family wealth), in a friendly sign and in the same sign in the D9 chart. The Sun sits weak in the 11th house of income."),
            ("western", "The Sun, the exalted Moon and Mercury sit together in the 11th house, which Hellenistic authors called the Good Spirit: gains, friends and allies. It is the most positive single factor in your Western chart."),
            ("sinic", "Metal, your Wealth element, is the heaviest element in your BaZi, while the Day Master counts as weak by weight. The classical phrase is 财多身弱, more wealth around you than you can easily hold. Zi Wei's wealth palace borrows 武曲 (the wealth star, bright) and 贪狼."),
        ],
        "practice": [
            "In the Western picture, gains come through people, networks and groups.",
            "The Chinese reading adds a caution: opportunities can outgrow your capacity to hold them. The strength-balancing school's traditional answer is support from peers and from learning or mentors.",
            "None of this is financial advice or a forecast of gain or loss.",
        ],
        "reflect": ["Which of your openings came through other people?", "Where have you taken on more than you could carry?"],
    },
    "D4": {
        "expect": ("WEAK", {"jyotisha": "positive", "western": "neutral", "sinic": "mixed"}),
        "headline": "Relationships run deep and shape you, but the systems disagree on their tone.",
        "traditions": [
            ("jyotisha", "Venus, the marker of love and marriage, is in a friendly sign and in its own sign, Libra, in the D9 chart, which Vedic astrologers use for marriage. A supportive picture."),
            ("sinic", "Your BaZi spouse palace (day branch 申) is combined with, punished by and broken by the 巳 branches around it: attraction mixed with friction. In Zi Wei, the spouse palace is also your Body palace, with 廉贞 turning to 化禄 (fortune) and 破军 turning to 化权 (power). Partnership becomes part of who you are."),
            ("western", "Venus was stationing to turn retrograde when you were born. Tradition reads this as love that gets revisited and reconsidered. The registry scores it neutral."),
        ],
        "practice": ["Tradition expects relationships to be formative for you, with some push and pull. Only the Vedic chart gives a clear signal, so hold this loosely."],
        "reflect": ["Which relationships changed how you see yourself?"],
    },
    "D5": {
        "expect": ("DIVERGENT", {"jyotisha": "negative", "western": "positive", "sinic": "mixed"}),
        "headline": "Home and roots: the systems disagree.",
        "traditions": [
            ("jyotisha", "Ketu, the node of detachment, sits in your 4th house of home and roots. The classical reading is a loose tie to one fixed home."),
            ("western", "The Moon, significator of mother and home, is exalted in Taurus, its best placement. A strong, nourishing home signature."),
            ("sinic", "BaZi's Resource star (the mother) 甲 is tied up by the combination 甲己合. Zi Wei's parents palace is bright (天同, 太阴), but the property palace carries 太阳化忌."),
        ],
        "practice": ["This one is unresolved. The traditions contradict each other, so no verdict comes out of it."],
        "reflect": [],
    },
    "D6": {
        "expect": ("WEAK", {"jyotisha": "positive", "western": "neutral", "sinic": "mixed"}),
        "headline": "One clear voice, and a supportive one.",
        "traditions": [
            ("jyotisha", "Jupiter, the significator of children and creative legacy, is strong (friendly sign, same sign in D1 and D9)."),
            ("sinic", "Your BaZi hour pillar (the children palace) repeats the 伤官见官 friction. Zi Wei's children palace is empty and borrows 太阳化忌 and 巨门 from the opposite palace."),
        ],
        "practice": ["This is symbolic only. It says nothing about fertility or family planning."],
        "reflect": [],
    },
    "D7": {
        "expect": ("WEAK", {"jyotisha": "silent", "western": "positive", "sinic": "neutral"}),
        "headline": "Symbolic only. No health information.",
        "traditions": [("western", "The Moon, the classical significator of the body, is exalted in Taurus.")],
        "practice": ["Nothing in this page is a health, medical or lifespan statement."],
        "reflect": [],
    },
    "D8": {
        "expect": ("WEAK", {"jyotisha": "neutral", "western": "neutral", "sinic": "positive"}),
        "headline": "The Chinese charts show strong creative output; the others stay neutral.",
        "traditions": [
            ("sinic", "The Hurting Officer is visible on your month stem and Eating God appears in four hidden stems. These are BaZi's output stars: expression, performance, making things, critique. Zi Wei's 文曲 (literary talent) sits in your Body palace."),
            ("jyotisha", "Mercury sits with the Moon and Rahu in Aries, neutral. In the D9 chart it is in Gemini, its own sign."),
            ("western", "Mercury is peregrine in Taurus: neutral."),
        ],
        "practice": ["BaZi would point you toward making and expressing rather than following a script. Only one system says so."],
        "reflect": ["What do you make or say that nobody asked you to?"],
    },
    "D9": {
        "expect": ("MODERATE", {"jyotisha": "positive", "western": "neutral", "sinic": "positive"}),
        "headline": "Your steadiest signature: a good relationship with meaning, learning and luck.",
        "traditions": [
            ("jyotisha", "Jupiter (guru, dharma, wisdom) is in Leo in both the D1 and D9 charts. That is called vargottama, a mark of consistent strength."),
            ("sinic", "Zi Wei's 福德 palace (inner contentment, spirit) holds 武曲, bright and turning to 化科 (recognition), with 贪狼 bright and 天魁 (helpful people). A well-starred palace."),
            ("western", "Jupiter is in Virgo, its detriment, and stationing direct. Neutral."),
        ],
        "practice": [
            "Tradition would expect beliefs, study and mentors to steady you.",
            "Zi Wei's ten-year period in this palace runs roughly 2029 to 2038.",
        ],
        "reflect": ["Which ideas or teachers have steadied you when things wobbled?"],
    },
}

CHAPTERS = [
    {"start": "2026-05-17", "end": "2027-05-17", "title": "Money & gains switch on", "tag": "STRONG",
     "text": "The only window where all three clusters point at the same area. Vedic: Sun period, with the Sun in your 11th house of income. Western: the age-22 year activates the 11th house (gains, allies), with Venus as lord of the year. BaZi: the 辛未 luck pillar has Direct Wealth on its stem, and the 2026 year 丙午 adds peers and competitors (Friend / Rob Wealth). The area is active; the natal reading stays double-edged, so this says nothing about gain or loss.",
     "refs": ["SYNTHESIS.json → timing.current[0]", "SYNTHESIS.json → bazi_annual_ten_gods.2026"]},
    {"start": "2027-05-17", "end": "2028-05-17", "title": "Behind-the-scenes year", "tag": "MODERATE",
     "text": "Money stays moderately active (Vedic Sun period + BaZi 辛未). The Western profection moves to the 12th house, traditionally a quieter, withdrawn year, with Mercury as lord. Vedic sub-periods run Mars (to 10 Mar 2027), Rahu (to 2 Feb 2028) and Jupiter. BaZi's 2027 year 丁未 brings Rob Wealth and Hurting Officer.",
     "refs": ["RAW_CALCULATIONS.json → western.charts.+0min.profections[1]", "RAW_CALCULATIONS.json → jyotisha.vimshottari.+0min"]},
    {"start": "2028-05-17", "end": "2029-05-17", "title": "A year about you", "tag": "MODERATE",
     "text": "Vedic Sun period and the Western age-24 profection (1st house, Moon as lord) both activate the self. Given the strained natal reading of the self, tradition would frame this as a year of re-examining how you present and assert yourself.",
     "refs": ["SYNTHESIS.json → timing.windows (D1)"]},
    {"start": "2029-02-01", "end": "2039-02-01", "title": "Zi Wei decade in the palace of meaning", "tag": "WEAK",
     "text": "Zi Wei's ten-year period moves into the 福德 palace, your best-starred palace. One system only, so it isn't a convergence. It lines up in theme with the favourable Vedic Jupiter reading of meaning and luck.",
     "refs": ["SYNTHESIS.json → timing.techniques (Zi Wei decadal 26-35)"]},
    {"start": "2030-10-06", "end": "2032-01-13", "title": "Career pressure and structure", "tag": "MODERATE",
     "text": "BaZi's luck pillar changes to 壬申 on about 6 Oct 2030. Its stem is Seven Killings: pressure, challenge, authority. The Vedic Sun period (the Sun signifies status) is still running, so both activate work and money.",
     "refs": ["SYNTHESIS.json → timing.windows (D2)"]},
    {"start": "2032-01-15", "end": "2042-01-14", "title": "Vedic Moon period begins", "tag": "MODERATE",
     "text": "A ten-year Moon period. The Moon sits in your 10th house of career, so work stays prominent; together with 壬申 it gives another two-system career window in 2032. The computed convergence horizon ends at 2032.",
     "refs": ["RAW_CALCULATIONS.json → jyotisha.vimshottari.+0min.mahadashas[3]"]},
]

CSS = r"""
:root{--bg:#F2F3F6;--surface:#FFFFFF;--surface2:#E8EBF2;--ink:#1A2032;--muted:#586178;--line:#D4D8E2;
--accent:#B3620A;--lapis:#2D4A8E;--pos:#2B7757;--mix:#9C6810;--neg:#A93A53;--neu:#7F8699;
--wood:#3F8A4E;--fire:#C2452D;--earth:#A77B2E;--metal:#7C8394;--water:#2F63A8;
--f-display:"Marcellus","Cormorant Garamond",Georgia,serif;--f-body:"Source Serif 4","Iowan Old Style",Georgia,serif;
--f-mono:"IBM Plex Mono",ui-monospace,Menlo,Consolas,monospace}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){color-scheme:dark;--bg:#0F131D;--surface:#161B28;--surface2:#1E2436;
--ink:#E7E9F0;--muted:#9CA4B8;--line:#2B3246;--accent:#E3A23F;--lapis:#93ABE9;--pos:#5DC49B;--mix:#E4B24D;--neg:#F07D95;--neu:#7E879B;
--wood:#6DBA7B;--fire:#EE7A5F;--earth:#D3A657;--metal:#A9B0C0;--water:#77A6E6}}
:root[data-theme="dark"]{color-scheme:dark;--bg:#0F131D;--surface:#161B28;--surface2:#1E2436;
--ink:#E7E9F0;--muted:#9CA4B8;--line:#2B3246;--accent:#E3A23F;--lapis:#93ABE9;--pos:#5DC49B;--mix:#E4B24D;--neg:#F07D95;--neu:#7E879B;
--wood:#6DBA7B;--fire:#EE7A5F;--earth:#D3A657;--metal:#A9B0C0;--water:#77A6E6}
*{box-sizing:border-box}
body{background:var(--bg);color:var(--ink);font-family:var(--f-body);font-size:17px;line-height:1.6;margin:0}
.wrap{max-width:1100px;margin:0 auto;padding-inline:20px;padding-block:28px 64px}
h1,h2,h3{font-family:var(--f-display);font-weight:400;text-wrap:balance;margin:0;letter-spacing:.01em}
h1{font-size:clamp(2.1rem,5vw,3.3rem);line-height:1.08}
h2{font-size:clamp(1.6rem,3.2vw,2.2rem);line-height:1.15}
h3{font-size:1.35rem;line-height:1.25}
p{margin:0}
a{color:var(--lapis)}
a:focus-visible,summary:focus-visible,button:focus-visible{outline:2px solid var(--accent);outline-offset:2px;border-radius:4px}
.eyebrow{font-family:var(--f-mono);font-size:.72rem;letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}
.mono{font-family:var(--f-mono);font-size:.86em;font-variant-numeric:tabular-nums}
.muted{color:var(--muted)}
nav.toc{position:sticky;top:env(safe-area-inset-top,0px);z-index:5;background:var(--bg);border-bottom:1px solid var(--line);
display:flex;gap:4px 18px;flex-wrap:wrap;padding-block:10px;margin-bottom:28px}
nav.toc a{font-family:var(--f-mono);font-size:.76rem;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);text-decoration:none}
nav.toc a:hover{color:var(--ink)}
.hero{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,.9fr);gap:36px;align-items:center}
.hero .lede{font-size:1.2rem;color:var(--muted);max-width:40ch;margin-top:14px}
.facts{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,150px),1fr));gap:10px;margin-top:22px}
.fact{border-top:1px solid var(--line);padding-top:8px}
.fact b{display:block;font-family:var(--f-display);font-weight:400;font-size:1.15rem}
.wheel{width:100%;max-width:440px;justify-self:center}
.wheel text{fill:var(--ink);font-family:var(--f-mono)}
.frame{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:18px 20px}
.note{border-left:3px solid var(--accent);padding:10px 14px;background:var(--surface);border-radius:0 8px 8px 0;margin-top:22px;font-size:.95rem}
section{margin-top:64px;display:flex;flex-direction:column;gap:18px}
.sec-head{display:flex;flex-direction:column;gap:6px;max-width:70ch}
.sec-head p{color:var(--muted)}
.big3{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,260px),1fr));gap:14px}
.big3 .frame{display:flex;flex-direction:column;gap:8px}
.big3 .num{font-family:var(--f-display);font-size:2.4rem;line-height:1}
.legend{display:flex;flex-wrap:wrap;gap:8px 16px;font-size:.9rem}
.chip{display:inline-flex;align-items:center;gap:6px;font-family:var(--f-mono);font-size:.72rem;letter-spacing:.06em;
text-transform:uppercase;padding:3px 9px;border-radius:999px;border:1px solid currentColor;white-space:nowrap}
.chip::before{content:"";width:7px;height:7px;border-radius:50%;background:currentColor}
.c-positive{color:var(--pos)}.c-negative{color:var(--neg)}.c-mixed{color:var(--mix)}.c-neutral,.c-silent{color:var(--neu)}
.g-STRONG{color:var(--accent)}.g-MODERATE{color:var(--lapis)}.g-WEAK{color:var(--neu)}.g-DIVERGENT{color:var(--neg)}.g-INSUFFICIENT{color:var(--neu)}
.domain{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:22px 22px 16px;display:flex;flex-direction:column;gap:14px}
.domain.hi{border-color:var(--lapis)}
.dhead{display:flex;flex-wrap:wrap;justify-content:space-between;gap:10px;align-items:baseline}
.dhead h3 small{font-family:var(--f-mono);font-size:.72rem;color:var(--muted);letter-spacing:.1em;margin-right:8px}
.headline{font-size:1.18rem;font-style:italic}
.votes{display:flex;flex-wrap:wrap;gap:8px}
.cols{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,1fr);gap:22px}
.trad{display:flex;flex-direction:column;gap:10px}
.trad p{padding-left:12px;border-left:2px solid var(--line)}
.trad p b{font-family:var(--f-mono);font-size:.72rem;letter-spacing:.1em;text-transform:uppercase;font-weight:500;color:var(--muted);display:block}
.practice{background:var(--surface2);border-radius:10px;padding:14px 16px;display:flex;flex-direction:column;gap:8px}
.practice ul{margin:0;padding-left:18px;display:flex;flex-direction:column;gap:6px}
.reflect{font-style:italic;color:var(--muted)}
details.ev{border-top:1px dashed var(--line);padding-top:8px}
details.ev summary{cursor:pointer;font-family:var(--f-mono);font-size:.76rem;letter-spacing:.08em;text-transform:uppercase;color:var(--lapis)}
.evtable{overflow-x:auto;margin-top:10px}
table{border-collapse:collapse;width:100%;font-size:.88rem}
th,td{text-align:left;padding:7px 8px;border-bottom:1px solid var(--line);vertical-align:top}
th{font-family:var(--f-mono);font-size:.7rem;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);font-weight:500}
td code{font-family:var(--f-mono);font-size:.78rem;color:var(--muted);word-break:break-word}
.grid2{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr));gap:16px}
.grid2.wide{grid-template-columns:repeat(auto-fit,minmax(min(100%,460px),1fr))}
.tempo{display:grid;grid-template-columns:minmax(140px,1.2fr) repeat(3,minmax(0,1fr));gap:0;font-size:.92rem}
.tempo>div{padding:9px 8px;border-bottom:1px solid var(--line)}
.tempo .h{font-family:var(--f-mono);font-size:.7rem;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
.dot{display:inline-block;width:10px;height:10px;border-radius:50%;background:currentColor;margin-right:6px;vertical-align:middle}
.timeline{overflow-x:auto;background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:12px}
.timeline svg{display:block;min-width:760px;width:100%}
.timeline text{font-family:var(--f-mono);fill:var(--ink)}
.chapters{display:flex;flex-direction:column;gap:12px}
.chapter{display:grid;grid-template-columns:170px minmax(0,1fr);gap:18px;padding:16px 0;border-top:1px solid var(--line)}
.chapter.now{background:var(--surface);border:1px solid var(--accent);border-radius:12px;padding:16px}
.chapter .when{font-family:var(--f-mono);font-size:.8rem;color:var(--muted);display:flex;flex-direction:column;gap:6px}
.chapter h3{margin-bottom:6px}
.refs{font-family:var(--f-mono);font-size:.72rem;color:var(--muted);margin-top:8px}
.pillars{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px;text-align:center}
.pillar{border:1px solid var(--line);border-radius:10px;padding:10px 4px;background:var(--surface)}
.pillar .zh{font-size:2rem;line-height:1.2;font-family:"Noto Serif SC","Songti SC",serif}
.pillar .lab{font-family:var(--f-mono);font-size:.68rem;letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}
.el{font-family:var(--f-mono);font-size:.7rem}
.el-Wood{color:var(--wood)}.el-Fire{color:var(--fire)}.el-Earth{color:var(--earth)}.el-Metal{color:var(--metal)}.el-Water{color:var(--water)}
.zw{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:4px;font-size:.78rem}
.zw>div{border:1px solid var(--line);border-radius:6px;padding:6px;background:var(--surface);min-height:74px}
.zw .pn{font-family:var(--f-mono);font-size:.64rem;letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}
.zw .ming{border-color:var(--accent)}
.zw .center{grid-column:2/4;grid-row:2/4;display:flex;flex-direction:column;justify-content:center;gap:4px;text-align:center;background:var(--surface2)}
.sources{columns:2 260px;gap:24px}
.sources li{break-inside:avoid;margin-bottom:6px}
footer{margin-top:64px;border-top:1px solid var(--line);padding-top:18px;color:var(--muted);font-size:.9rem}
@media (max-width:760px){.hero,.cols{grid-template-columns:1fr}.chapter{grid-template-columns:1fr}.tempo{grid-template-columns:minmax(110px,1fr) repeat(3,minmax(0,1fr));font-size:.82rem}}
@media (prefers-reduced-motion:no-preference){.domain,.frame{transition:border-color .2s}}
"""


def chip(cls, text):
    return f'<span class="chip {cls}">{E(text)}</span>'


def wheel(raw):
    A = raw["astronomy"]["+0min"]
    asc = A["angles_tropical"]["asc"]
    mc = A["angles_tropical"]["mc"]
    ay = A["ayanamsha_lahiri_deg"]
    cx = cy = 220
    pt = lambda lon, r: (cx + r * math.cos(math.pi + math.radians(lon - asc)),
                         cy - r * math.sin(math.pi + math.radians(lon - asc)))
    s = [f'<svg class="wheel" viewBox="0 0 440 440" role="img" aria-label="Birth chart wheel: outer ring tropical zodiac, inner ring sidereal (Lahiri) zodiac, Ascendant at left">']
    ab = ["Ari", "Tau", "Gem", "Can", "Leo", "Vir", "Lib", "Sco", "Sag", "Cap", "Aqu", "Pis"]

    def band(r1, r2, offset, rising, label_r, cls):
        for k in range(12):
            a0 = k * 30 + offset
            x1, y1 = pt(a0, r1)
            x2, y2 = pt(a0, r2)
            s.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="var(--line)" stroke-width="1"/>')
            if k == rising:
                # shade the rising sign
                pts = [pt(a0 + t, r1) for t in range(0, 31, 3)] + [pt(a0 + 30 - t, r2) for t in range(0, 31, 3)]
                s.append('<polygon points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in pts) +
                         '" fill="var(--accent)" fill-opacity=".16" stroke="none"/>')
            lx, ly = pt(a0 + 15, label_r)
            s.append(f'<text x="{lx:.1f}" y="{ly:.1f}" font-size="10.5" text-anchor="middle" dominant-baseline="middle" '
                     f'fill="{"var(--accent)" if k == rising else "var(--muted)"}" style="fill:{"var(--accent)" if k == rising else "var(--muted)"}">{ab[k]}</text>')
        s.append(f'<circle cx="{cx}" cy="{cy}" r="{r1}" fill="none" stroke="var(--line)"/>')
        s.append(f'<circle cx="{cx}" cy="{cy}" r="{r2}" fill="none" stroke="var(--line)"/>')

    s.append(f'<circle cx="{cx}" cy="{cy}" r="214" fill="var(--surface)" stroke="var(--line)"/>')
    band(214, 188, 0, int(asc // 30), 201, "trop")
    band(96, 76, ay, int(((asc - ay) % 360) // 30), 86, "sid")
    # axes
    for lon, lab in ((asc, "ASC"), (mc, "MC")):
        x1, y1 = pt(lon, 188)
        x2, y2 = pt(lon + 180, 188)
        s.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="var(--lapis)" stroke-width="1" stroke-dasharray="3 4" opacity=".7"/>')
        tx, ty = pt(lon, 176)
        s.append(f'<text x="{tx:.1f}" y="{ty:.1f}" font-size="9.5" text-anchor="middle" dominant-baseline="middle" style="fill:var(--lapis)">{lab}</text>')
    glyph = {"Sun": "Su", "Moon": "Mo", "Mercury": "Me", "Venus": "Ve", "Mars": "Ma", "Jupiter": "Ju", "Saturn": "Sa",
             "MeanNode": "Ra", "MeanKetu": "Ke"}
    bodies = sorted(((A["bodies"][k]["lon"], v) for k, v in glyph.items()), key=lambda x: x[0])
    placed = []
    for lon, g in bodies:
        r = 158
        for plon, pr in placed:
            if abs(((lon - plon + 180) % 360) - 180) < 9 and pr == r:
                r -= 26
        placed.append((lon, r))
        mx, my = pt(lon, 186)
        nx, ny = pt(lon, 176)
        s.append(f'<line x1="{mx:.1f}" y1="{my:.1f}" x2="{nx:.1f}" y2="{ny:.1f}" stroke="var(--ink)" stroke-width="1.4"/>')
        x, y = pt(lon, r)
        s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="12" fill="var(--surface2)" stroke="var(--line)"/>')
        s.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="10" text-anchor="middle" dominant-baseline="central">{g}</text>')
    s.append("</svg>")
    return ('<figure style="margin:0;display:flex;flex-direction:column;align-items:center;gap:6px">' + "".join(s) +
            '<figcaption class="mono muted" style="font-size:.74rem;text-align:center">Same sky, two zodiacs. Outer ring: Western (tropical). '
            'Inner ring: Vedic (sidereal, Lahiri). Rising sign shaded; Ascendant at left.</figcaption></figure>')


def timeline_svg(raw, syn, today):
    y0, y1 = 2024, 2034
    W, left, top = 1000, 190, 26
    x = lambda d: left + (W - left - 10) * ((d.year + (d.timetuple().tm_yday - 1) / 365.25) - y0) / (y1 - y0)
    D = lambda s: date.fromisoformat(s[:10])
    rows = []
    V = raw["jyotisha"]["vimshottari"]["+0min"]["mahadashas"]
    rows.append(("Vedic major", [(m["start"], m["end"], m["lord"]) for m in V]))
    ads = [ad for m in V for ad in m["antardashas"]]
    rows.append(("Vedic sub", [(a["start"], a["end"], a["lord"][:2]) for a in ads]))
    rows.append(("Western year", [(p["start"], p["end"], f"H{p['activated_house']}") for p in raw["western"]["charts"]["+0min"]["profections"]]))
    bz = [t for t in syn["timing"]["techniques"] if t["technique"].startswith("BaZi")]
    rows.append(("BaZi luck", [(t["start"], t["end"], t["technique"].split()[-1]) for t in bz]))
    rows.append(("BaZi year", [(f"{y}-02-04", f"{int(y) + 1}-02-04", g) for y, g in raw["bazi"]["primary"]["annual_pillars"].items()]))
    zw = [t for t in syn["timing"]["techniques"] if t["technique"].startswith("Zi Wei")]
    rows.append(("Zi Wei decade", [(t["start_iso_approx"], t["end_iso_approx"], t["technique"].split("(")[1].split()[0]) for t in zw]))
    rh = 30
    lo, hi = date(y0, 1, 1), date(y1, 1, 1)
    ndom = len({w_["domain"] for w_ in syn["timing"]["windows"] if D(w_["end"]) > lo and D(w_["start"]) < hi})
    H = top + rh * (len(rows) + ndom) + 30
    s = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Timeline 2024 to 2034 of all timing techniques and convergence windows">']
    for yr in range(y0, y1 + 1):
        xx = x(date(yr, 1, 1))
        s.append(f'<line x1="{xx:.1f}" y1="{top - 6}" x2="{xx:.1f}" y2="{H - 24}" stroke="var(--line)"/>')
        s.append(f'<text x="{xx:.1f}" y="{top - 12}" font-size="11" text-anchor="middle" style="fill:var(--muted)">{yr}</text>')
    lo, hi = date(y0, 1, 1), date(y1, 1, 1)
    for i, (name, segs) in enumerate(rows):
        yy = top + i * rh
        s.append(f'<text x="8" y="{yy + rh / 2 + 4:.1f}" font-size="11" style="fill:var(--muted)">{E(name)}</text>')
        for a, b, lab in segs:
            da, db = max(D(a), lo), min(D(b), hi)
            if da >= db:
                continue
            xa, xb = x(da), x(db)
            s.append(f'<rect x="{xa + 1:.1f}" y="{yy + 4}" width="{max(xb - xa - 2, 1):.1f}" height="{rh - 8}" rx="4" fill="var(--surface2)" stroke="var(--line)"/>')
            if xb - xa > 26:
                s.append(f'<text x="{(xa + xb) / 2:.1f}" y="{yy + rh / 2 + 4:.1f}" font-size="10.5" text-anchor="middle">{E(lab)}</text>')
    # convergence rows, one per domain so overlapping windows never overprint
    doms = sorted({w_["domain"] for w_ in syn["timing"]["windows"] if D(w_["end"]) > lo and D(w_["start"]) < hi})
    for j, dm in enumerate(doms):
        yy = top + (len(rows) + j) * rh
        s.append(f'<text x="8" y="{yy + rh / 2 + 4:.1f}" font-size="11" style="fill:var(--accent)">Agree · {E(DOMAIN_TITLE[dm])}</text>')
        for w_ in [w_ for w_ in syn["timing"]["windows"] if w_["domain"] == dm]:
            da, db = max(D(w_["start"]), lo), min(D(w_["end"]), hi)
            if da >= db:
                continue
            strong = w_["grade"].startswith("STRONG")
            xa, xb = x(da), x(db)
            s.append(f'<rect x="{xa + 1:.1f}" y="{yy + 4}" width="{max(xb - xa - 2, 1):.1f}" height="{rh - 8}" rx="4" '
                     f'fill="{"var(--accent)" if strong else "var(--lapis)"}" fill-opacity="{0.85 if strong else 0.35}"/>')
            if xb - xa > 40:
                s.append(f'<text x="{(xa + xb) / 2:.1f}" y="{yy + rh / 2 + 4:.1f}" font-size="10.5" text-anchor="middle">{"3 agree" if strong else "2 agree"}</text>')
    tx = x(today)
    s.append(f'<line x1="{tx:.1f}" y1="{top - 4}" x2="{tx:.1f}" y2="{H - 20}" stroke="var(--accent)" stroke-width="2"/>')
    s.append(f'<text x="{tx + 4:.1f}" y="{H - 8}" font-size="11" style="fill:var(--accent)">today {today.isoformat()}</text>')
    s.append("</svg>")
    return "".join(s)


def pillars_html(raw):
    out = ['<div class="pillars">']
    for p in raw["bazi"]["primary"]["pillars"]:
        out.append(f'<div class="pillar"><div class="lab">{p["pillar"]}</div><div class="zh">{p["stem"]}<br>{p["branch"]}</div>'
                   f'<div class="el el-{p["stem_element"]}">{p["stem_polarity"]} {p["stem_element"]}</div>'
                   f'<div class="el el-{p["branch_element"]}">{p["branch_element"]}</div>'
                   f'<div class="lab" style="margin-top:4px">{E(p["ten_god_of_stem"].split(" ", 1)[-1])}</div></div>')
    out.append("</div>")
    return "".join(out)


def ziwei_html(raw, syn):
    zb = syn["reference_frames"]["ziwei_hour_branch"]
    zc = raw["ziwei"]["alternatives"][zb]["chart_zh"]
    ze = raw["ziwei"]["alternatives"][zb]["chart_en"]
    by = {p["earthlyBranch"]: (p, pe) for p, pe in zip(zc["palaces"], ze["palaces"])}
    layout = [["巳", "午", "未", "申"], ["辰", None, None, "酉"], ["卯", None, None, "戌"], ["寅", "丑", "子", "亥"]]
    out = ['<div class="zw" aria-label="Zi Wei Dou Shu palace chart">']
    centre_done = False
    for row in layout:
        for br in row:
            if br is None:
                if not centre_done:
                    out.append(f'<div class="center"><b style="font-family:var(--f-display);font-size:1.1rem">{E(zc["fiveElementsClass"])}</b>'
                               f'<span class="mono">命 {zc["earthlyBranchOfSoulPalace"]} · 身 {zc["earthlyBranchOfBodyPalace"]}</span>'
                               f'<span class="mono muted">{E(zc["lunarDate"])} · {E(zc["time"])}</span></div>')
                    centre_done = True
                continue
            p, pe = by[br]
            majors = " ".join(s["name"] + ("<sup>" + s["mutagen"] + "</sup>" if s.get("mutagen") else "") for s in p["majorStars"]) or '<span class="muted">—</span>'
            out.append(f'<div class="{"ming" if p["name"] == "命宫" else ""}"><div class="pn">{p["heavenlyStem"]}{br} · {E(pe["name"])}{" · body" if p["isBodyPalace"] else ""}</div>'
                       f'<div>{p["name"]}</div><div>{majors}</div></div>')
    out.append("</div>")
    return "".join(out)


def main():
    raw, syn, ver = J("RAW_CALCULATIONS.json"), J("SYNTHESIS.json"), J("VERIFICATION_REPORT.json")
    inp = json.load(open(os.path.join(ROOT, "BIRTH_INPUT.json"), encoding="utf-8"))
    today = date.fromisoformat(inp["analysis_date"])
    sc = syn["scenarios"]["outer"]
    Dm = sc["domains"]
    A = raw["astronomy"]["+0min"]
    jc = raw["jyotisha"]["charts"]["+0min"]
    wc = raw["western"]["charts"]["+0min"]
    a = raw["input_audit"]
    bz = raw["bazi"]["primary"]
    m = raw["maya"]
    t = raw["tibetan"]

    h = [f"<title>Six Traditions Life Map</title>",
         '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Marcellus&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&family=IBM+Plex+Mono:wght@400;500&display=swap">',
         f"<style>{CSS}</style>", '<div class="wrap">',
         '<nav class="toc" aria-label="Sections"><a href="#top">Overview</a><a href="#themes">Life themes</a><a href="#temperament">Temperament</a>'
         '<a href="#chapters">Timeline</a><a href="#tension">Where systems disagree</a><a href="#charts">Your charts</a><a href="#method">How this was made</a></nav>']

    # ---------- hero ----------
    lag, asc = jc["lagna"], wc["asc"]
    h.append('<header class="hero" id="top"><div>')
    h.append('<div class="eyebrow">Six traditions · one sky</div>')
    h.append('<h1>Your life map, read across six traditions</h1>')
    h.append(f'<p class="lede">Born {a["weekday"]} 17 May 2004 at 09:30 IST in Lucknow (Fatima Hospital). '
             'Vedic, Western, BaZi and Zi Wei were each computed separately and checked against independent engines, then compared. '
             'This page explains what they would say about your life, and shows exactly where each statement comes from.</p>')
    h.append('<div class="facts">')
    for lab, val, sub in [
        ("Rising sign", "Cancer", f"Vedic {lag['deg']:.1f}° · Western {asc['deg']:.1f}°"),
        ("Moon", f"{jc['grahas']['Moon']['sign']} / Taurus", f"Vedic / Western · {jc['grahas']['Moon']['nakshatra']['name']}"),
        ("Day Master", "丙 Yang Fire", "BaZi · born in its own season"),
        ("Zi Wei life palace", "天府 in 亥", syn["reference_frames"]["ziwei_hour_branch"] + " hour · " + raw["ziwei"]["alternatives"][syn["reference_frames"]["ziwei_hour_branch"]]["chart_en"]["fiveElementsClass"]),
        ("Maya day", m["tzolkin"], m["long_count"]),
        ("Tibetan year", f"{t['element']} {t['animal']}", t["gender"]),
    ]:
        h.append(f'<div class="fact"><span class="eyebrow">{E(lab)}</span><b>{E(val)}</b><span class="mono muted">{E(sub)}</span></div>')
    h.append('</div></div>')
    h.append(wheel(raw))
    h.append('</header>')
    h.append('<div class="note"><b>Read this first.</b> Astrology is not a validated way to predict anything. What follows is what these traditions say, translated into plain language, with the agreement between them measured. '
             '"Tradition would expect" means exactly that: it describes a symbol system, not your fate. Nothing here is medical, financial or legal advice.</div>')

    # ---------- big three ----------
    top3 = [d for d in Dm if Dm[d]["grade"] in ("STRONG", "MODERATE")]
    div = [d for d in Dm if Dm[d]["grade"] == "DIVERGENT"]
    cur = syn["timing"]["current"]
    h.append('<section id="summary"><div class="sec-head"><div class="eyebrow">In one glance</div><h2>What stands out</h2></div><div class="big3">')
    h.append(f'<div class="frame"><span class="eyebrow">Where systems agree</span><span class="num">{len(top3)} of 9</span>'
             f'<p>{", ".join(DOMAIN_TITLE[d] for d in top3)}. No area reaches agreement from all three clusters.</p></div>' if not any(Dm[d]["grade"] == "STRONG" for d in Dm) else "")
    h.append(f'<div class="frame"><span class="eyebrow">Where they clash</span><span class="num">{len(div)} of 9</span>'
             f'<p>{", ".join(DOMAIN_TITLE[d] for d in div) or "None"}. Shown in full below, not smoothed over.</p></div>')
    if cur:
        c0 = cur[0]
        h.append(f'<div class="frame" style="border-color:var(--accent)"><span class="eyebrow">Right now</span><span class="num" style="color:var(--accent)">{E(DOMAIN_TITLE[c0["domain"]])}</span>'
                 f'<p>All three clusters activate this area from {c0["start"]} to {c0["end"]}. That is the only three-way timing window found.</p></div>')
    h.append('</div><div class="legend">'
             + chip("g-STRONG", "All three agree") + chip("g-MODERATE", "Two agree") + chip("g-WEAK", "One voice") + chip("g-DIVERGENT", "Disagree")
             + '<span class="muted">·</span>' + chip("c-positive", "supportive") + chip("c-mixed", "double-edged") + chip("c-negative", "strained") + chip("c-neutral", "neutral")
             + '</div></section>')

    # ---------- themes ----------
    h.append('<section id="themes"><div class="sec-head"><div class="eyebrow">Nine life areas</div><h2>What your chart would mean, area by area</h2>'
             '<p>Areas where systems agree come first. Each card gives the reading in each tradition, what it tends to look like in practice, and the evidence behind it.</p></div>')
    order = sorted(Dm, key=lambda d: ({"STRONG": 0, "MODERATE": 1, "DIVERGENT": 2, "WEAK": 3, "INSUFFICIENT": 4}[Dm[d]["grade"]], d))
    for d in order:
        v = Dm[d]
        nar = NARRATIVE.get(d)
        valid = nar and nar["expect"][0] == v["grade"] and nar["expect"][1] == v["cluster_polarity"]
        h.append(f'<article class="domain{" hi" if v["grade"] in ("STRONG", "MODERATE") else ""}" id="{d}">')
        h.append(f'<div class="dhead"><h3><small>{d}</small>{E(DOMAIN_TITLE[d])}</h3>{chip("g-" + v["grade"], GRADE_LABEL[v["grade"]] + (" · " + POL_LABEL[v["agreed_polarity"]] if v["agreed_polarity"] else ""))}</div>')
        h.append('<div class="votes">' + "".join(chip("c-" + p, f"{SYS_LABEL[c]}: {POL_LABEL[p]}") for c, p in v["cluster_polarity"].items()) + "</div>")
        if valid:
            h.append(f'<p class="headline">{E(nar["headline"])}</p><div class="cols"><div class="trad">')
            for sysk, txt in nar["traditions"]:
                h.append(f'<p><b>{SYS_LABEL[sysk]}</b>{E(txt)}</p>')
            h.append('</div><div class="practice"><span class="eyebrow">What it could look like · interpretation, not prediction</span><ul>')
            h.extend(f"<li>{E(x)}</li>" for x in nar["practice"])
            h.append("</ul>")
            if nar["reflect"]:
                h.append('<span class="eyebrow" style="margin-top:6px">Questions to test it against your life</span>')
                h.extend(f'<p class="reflect">{E(q)}</p>' for q in nar["reflect"])
            h.append("</div></div>")
        else:
            h.append('<p class="muted">The interpretation for this area was written for different results and is withheld until it is rewritten. The evidence below is current.</p>')
        wins = [w_ for w_ in syn["timing"]["windows"] if w_["domain"] == d and w_["end"] > today.isoformat()]
        if wins:
            h.append('<p class="mono muted">Timing: ' + "; ".join(f'{w_["start"]} → {w_["end"]} ({E(w_["grade"])})' for w_ in wins) + "</p>")
        h.append(f'<details class="ev"><summary>Evidence · {len(v["projections"])} computed facts</summary><div class="evtable"><table><thead><tr><th>System</th><th>Computed fact</th><th>Reads as</th><th>Rule</th><th>Source</th></tr></thead><tbody>')
        for i, p in enumerate(v["projections"]):
            h.append(f'<tr><td>{SYS_LABEL[p["system"]]}</td><td>{E(p["basis"])}</td><td>{chip("c-" + p["polarity"], POL_LABEL[p["polarity"]])}</td>'
                     f'<td><code>{E(p["mapping_rule"])}</code></td><td><a href="{GH}SYNTHESIS.json" target="_blank" rel="noopener">SYNTHESIS.json</a><br><code>scenarios.outer.domains.{d}.projections[{i}]</code></td></tr>')
        h.append("</tbody></table></div></details></article>")
    h.append("</section>")

    # ---------- temperament ----------
    h.append('<section id="temperament"><div class="sec-head"><div class="eyebrow">Six axes</div><h2>Temperament</h2>'
             '<p>How each cluster reads six personality axes. "Supported" means the relevant factor is in good condition; "strained" means it works against friction.</p></div>')
    h.append('<div class="frame"><div class="tempo"><div class="h">Axis</div><div class="h">Vedic</div><div class="h">Western</div><div class="h">Chinese</div>')
    col = {"supported": "var(--pos)", "strained": "var(--neg)", "mixed/neutral": "var(--neu)", "silent": "var(--neu)"}
    for k, v in syn["temperament"].items():
        h.append(f'<div><b>{E(k.split(" ", 1)[1])}</b><br><span class="mono muted">{E(v["summary"])}</span></div>')
        for c in ("jyotisha", "western", "sinic"):
            x_ = v["clusters"][c]
            h.append(f'<div title="{E(x_["basis"])}"><span class="dot" style="color:{col[x_["reading"]]}"></span>{E(x_["reading"])}<br><span class="mono muted" style="font-size:.72rem">{E(x_["basis"])}</span></div>')
    h.append('</div></div><p class="muted">What stands out: nurturing (Western exalted Moon, BaZi Resource star) is the most supported axis. Leadership and drive are where the systems clash: the Vedic and Western planets for them are weak, while Zi Wei places 天府 in the life palace and 破军 in the body palace. '
             f'Source: <a href="{GH}SYNTHESIS.json" target="_blank" rel="noopener">SYNTHESIS.json</a> <code>temperament</code>.</p></section>')

    # ---------- chapters ----------
    h.append('<section id="chapters"><div class="sec-head"><div class="eyebrow">2024 → 2034</div><h2>Your timeline</h2>'
             '<p>Every timing technique on one axis. The bottom row marks where two or three clusters activate the same life area at once.</p></div>')
    h.append(f'<div class="timeline">{timeline_svg(raw, syn, today)}</div>')
    V = raw["jyotisha"]["vimshottari"]["+0min"]["mahadashas"]
    curp = []
    for md in V:
        if md["start"][:10] <= today.isoformat() < md["end"][:10]:
            curp.append(md["lord"])
            for ad in md["antardashas"]:
                if ad["start"][:10] <= today.isoformat() < ad["end"][:10]:
                    curp.append(ad["lord"])
                    for pd in ad.get("pratyantardashas", []):
                        if pd["start"][:10] <= today.isoformat() < pd["end"][:10]:
                            curp.append(f'{pd["lord"]} (to {pd["end"][:10]})')
    h.append(f'<p class="mono muted">Current Vedic period: {" → ".join(curp)}.</p><div class="chapters">')
    for ch in CHAPTERS:
        now = ch["start"] <= today.isoformat() < ch["end"]
        h.append(f'<div class="chapter{" now" if now else ""}"><div class="when"><span>{ch["start"]}</span><span>→ {ch["end"]}</span>{chip("g-" + ch["tag"], ("NOW · " if now else "") + GRADE_LABEL[ch["tag"]])}</div>'
                 f'<div><h3>{E(ch["title"])}</h3><p>{E(ch["text"])}</p><div class="refs">' + " · ".join(E(r) for r in ch["refs"]) + "</div></div></div>")
    h.append('</div></section>')

    # ---------- tension ----------
    dmx = bz["dm_strength"]
    h.append('<section id="tension"><div class="sec-head"><div class="eyebrow">Kept visible on purpose</div><h2>Where the systems disagree</h2></div><div class="grid2">')
    h.append(f'<div class="frame"><h3>Home & roots</h3><p>Vedic Ketu in the 4th says detachment. The Western exalted Moon says a strong home. They contradict each other, and neither wins. <a href="#D5">See the evidence</a>.</p></div>')
    h.append(f'<div class="frame"><h3>How strong is the Day Master?</h3><p>Counted by weight, your 丙 fire has {dmx["support_share"]:.0%} support, which is weak. By season, it is at its peak. '
             'So BaZi\'s "helpful element" is low confidence: the seasonal school points to water and metal, the balancing school to wood and fire.</p>'
             f'<p class="refs">RAW_CALCULATIONS.json → bazi.primary.dm_strength · SYNTHESIS.json → yong_shen</p></div>')
    h.append('<div class="frame"><h3>Leadership & drive</h3><p>The Vedic Sun and the Western Mars are both in poor condition, while Zi Wei places the steward star 天府 in your life palace and 破军 in your body palace. The systems read your drive in opposite ways.</p><p class="refs">SYNTHESIS.json → temperament.T1, T2</p></div>')
    h.append('<div class="frame"><h3>Looking from the Moon instead</h3><p>Vedic astrology also reads houses from the Moon. From your Moon, Rahu joins it in the 1st and Ketu sits in the 7th. That would make self and partnership read harsher. It is shown but not counted.</p><p class="refs">SYNTHESIS.json → secondary_jyotisha_view</p></div>')
    h.append("</div></section>")

    # ---------- charts ----------
    h.append('<section id="charts"><div class="sec-head"><div class="eyebrow">The raw material</div><h2>Your charts</h2><p>The computed placements everything above is built from.</p></div><div class="grid2 wide">')
    h.append('<div class="frame"><h3 style="margin-bottom:10px">Vedic (sidereal, Lahiri)</h3><div class="evtable"><table><thead><tr><th>Planet</th><th>Sign</th><th>House</th><th>Nakshatra</th><th>Dignity</th><th>D9</th></tr></thead><tbody>')
    for g, v in jc["grahas"].items():
        h.append(f'<tr><td>{g}</td><td class="mono">{v["sign"]} {v["deg"]:.1f}°</td><td class="mono">{v["house"]}</td><td>{v["nakshatra"]["name"]}-{v["nakshatra"]["pada"]}</td><td>{E(v["dignity"])}</td><td>{v["d9"]}</td></tr>')
    h.append(f'</tbody></table></div><p class="refs">Lagna Cancer {lag["deg"]:.2f}° · RAW_CALCULATIONS.json → jyotisha.charts.+0min</p></div>')
    h.append('<div class="frame"><h3 style="margin-bottom:10px">Western (tropical, whole-sign)</h3><div class="evtable"><table><thead><tr><th>Planet</th><th>Sign</th><th>House</th><th>Dignity</th><th>Sect</th></tr></thead><tbody>')
    for g, v in wc["planets"].items():
        h.append(f'<tr><td>{g}</td><td class="mono">{v["sign"]} {v["deg"]:.1f}°</td><td class="mono">{v["whole_sign_house"]}</td><td>{E(", ".join(v["essential"]["planet_dignities"]))}</td><td>{E(v["sect_status"])}</td></tr>')
    h.append(f'</tbody></table></div><p class="refs">Ascendant Cancer {asc["deg"]:.2f}°, day chart · RAW_CALCULATIONS.json → western.charts.+0min</p></div>')
    h.append(f'<div class="frame"><h3 style="margin-bottom:10px">BaZi Four Pillars</h3>{pillars_html(raw)}<p class="refs">Year · Month · Day · Hour. Checked against sxtwl. RAW_CALCULATIONS.json → bazi.primary.pillars</p></div>')
    h.append(f'<div class="frame"><h3 style="margin-bottom:10px">Zi Wei Dou Shu</h3>{ziwei_html(raw, syn)}<p class="refs">Traditional ring layout; the life palace is outlined. RAW_CALCULATIONS.json → ziwei.alternatives.巳</p></div>')
    h.append("</div></section>")

    # ---------- method ----------
    files = [("FINAL_READING.md", "The full written reading"), ("SYNTHESIS.json", "Rules, projections, grades, timing"),
             ("RAW_CALCULATIONS.json", "Every computed fact"), ("VERIFICATION_REPORT.md", "Engine cross-checks and invariants"),
             ("INPUT_AUDIT.md", "Time zone, solar time, boundaries"), ("MASTER_DATASET.md", "Readable fact tables"),
             ("CALCULATION_MANIFEST.json", "Versions, checksums, conventions")]
    h.append('<section id="method"><div class="sec-head"><div class="eyebrow">Receipts</div><h2>How this was made</h2></div><div class="grid2">')
    h.append(f'<div class="frame"><ul style="margin:0;padding-left:18px;display:flex;flex-direction:column;gap:6px">'
             f'<li>Planet positions from Swiss Ephemeris, checked against NASA JPL DE440s: largest difference {ver["largest_planet_difference_deg"]:.1e}°.</li>'
             f'<li>Chinese solar terms agreed across four engines to within {max(v["max_difference_s"] for v in bz["solar_terms"].values()):.1f} s; Four Pillars matched by two independent libraries.</li>'
             f'<li>{len(ver["invariants"])} structural checks, {len(ver["failures"])} failures.</li>'
             '<li>Birth time confirmed to ±1 minute, and the place is Fatima Hospital (OpenStreetMap). No output changes inside that window.</li>'
             '<li>Life-area rules were declared before comparing systems. Different reasonable rules would give different grades.</li>'
             '<li>Maya and Tibetan meanings are left out because no verifiable source was available.</li></ul></div>')
    h.append('<div class="frame"><span class="eyebrow">Source files (branch claude/six-culture-verified-chart-j5znid)</span><ul class="sources" style="padding-left:18px;margin-top:10px">')
    h.extend(f'<li><a href="{GH}{f}" target="_blank" rel="noopener">{f}</a><br><span class="muted" style="font-size:.88rem">{E(dsc)}</span></li>' for f, dsc in files)
    h.append("</ul></div></div></section>")
    h.append('<footer>This page shows where traditional symbolic systems agree and disagree about one birth moment. It is not a validated forecast, a fate, or a basis for medical, financial or legal decisions. '
             f'Generated by render_html.py from output/*.json on {today.isoformat()}.</footer></div>')
    open(os.path.join(OUT, "LIFE_MAP.html"), "w", encoding="utf-8").write("\n".join(h))


if __name__ == "__main__":
    main()
    print("ok")
