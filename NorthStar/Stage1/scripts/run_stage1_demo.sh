#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
OUT="${NORTHSTAR_OUTPUT_DIR:-examples/stage1-output}"
PYTHONPATH=src python3 -m northstar_compliance.cli \
  --provider mock \
  --input datasets/stage1/sample-publication.txt \
  --title "Synthetic Supervisory Notice 2026-NS-17" \
  --source-uri "synthetic://northstar/2026-NS-17" \
  --jurisdiction CA \
  --output-dir "$OUT"
