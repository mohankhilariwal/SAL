#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export PYTHONPATH="$ROOT/src"
export NORTHSTAR_ARTIFACT_DIR="${NORTHSTAR_ARTIFACT_DIR:-$ROOT/examples/stage3b-output}"
python "$ROOT/scripts/run_stage3b_demo.py"
