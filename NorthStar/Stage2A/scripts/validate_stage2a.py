#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from northstar_compliance.knowledge.validation import validate_prepared_corpus


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a prepared Stage 2A corpus")
    parser.add_argument("output", type=Path, nargs="?", default=Path("examples/stage2a-output"))
    args = parser.parse_args()
    print(json.dumps(validate_prepared_corpus(args.output), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
