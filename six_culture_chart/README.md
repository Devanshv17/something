# Six-culture verified chart

This folder holds a reproducible, fact-first chart pipeline for one birth input (`BIRTH_INPUT.json`). It covers Jyotisha, BaZi, Western/Hellenistic astrology, Zi Wei Dou Shu, the Maya calendar and the Tibetan element-animal year.

The output is **symbolic corroboration between traditions, not a validated forecast.**

## Outputs (`output/`)

| File | Contents |
|---|---|
| `BIRTH_INPUT.json` | the original and interpreted input |
| `INPUT_AUDIT.md` | civil-time, solar-time and boundary audit, with every crossing inside ±30 min |
| `CALCULATION_MANIFEST.json` | runtime, package versions, ephemeris checksums, conventions and source checksums |
| `RAW_CALCULATIONS.json` | all computed facts, including every time-ensemble alternative |
| `MASTER_DATASET.json` / `.md` | facts, provenance, verification and excluded methods (no interpretation) |
| `VERIFICATION_REPORT.json` / `.md` | primary-vs-validator differences, invariants and confidence |
| `SYNTHESIS.json` | predeclared mapping registry, projections, domain grades, timing windows and temperament |
| `FINAL_READING.md` | the human-readable reading; every statement is traceable to `SYNTHESIS.json` |
| `LIFE_MAP.html` | visual reading: plain-language implications per life area, timeline, charts, with each claim linked to its JSON source |

## Reproduce

```bash
uv venv -p python3.12 .venv
uv pip install -p .venv/bin/python -r requirements.lock
(cd js && npm ci)
mkdir -p ephe && cd ephe
for f in sepl_18.se1 semo_18.se1 seas_18.se1; do curl -sSfLO https://raw.githubusercontent.com/aloistr/swisseph/master/ephe/$f; done
curl -sSfLO https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/de440s.bsp
cd .. && sha256sum ephe/*   # compare with CALCULATION_MANIFEST.json
./run_all.sh
```

Pipeline: `build.py` computes facts, `verify.py` checks them against validators and invariants, `synth.py` projects them through the declared registry, and `render.py` writes the Markdown.
