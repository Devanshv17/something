#!/usr/bin/env bash
# Reproduce every output for one chart directory (default: this folder).
# Usage: ./run_all.sh [chart_dir]   e.g. ./run_all.sh people/anju
set -euo pipefail
cd "$(dirname "$0")"
export SIX_CHART_DIR="$(cd "${1:-.}" && pwd)"
.venv/bin/python build.py
.venv/bin/python verify.py
.venv/bin/python synth.py > /dev/null
.venv/bin/python render.py
.venv/bin/python render_html.py
