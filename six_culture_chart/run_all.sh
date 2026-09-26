#!/usr/bin/env bash
# Reproduce every output from BIRTH_INPUT.json. See README.md for environment setup.
set -euo pipefail
cd "$(dirname "$0")"
.venv/bin/python build.py
.venv/bin/python verify.py
.venv/bin/python synth.py > /dev/null
.venv/bin/python render.py
