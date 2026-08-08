#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from northstar_compliance.knowledge.service import KnowledgePreparationService
from northstar_compliance.knowledge.validation import validate_prepared_corpus


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare the NorthStar Stage 2A knowledge corpus")
    parser.add_argument("--input-root", type=Path, default=Path("datasets/stage2a/input"))
    parser.add_argument("--manifest", type=Path, default=Path("datasets/stage2a/input/manifest.json"))
    parser.add_argument("--output", type=Path, default=Path("examples/stage2a-output"))
    args = parser.parse_args()

    service = KnowledgePreparationService(input_root=args.input_root, output_root=args.output)
    run = service.prepare(args.manifest)
    validation = validate_prepared_corpus(args.output)
    print(json.dumps({"run": run.to_dict(), "validation": validation}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
