#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    required = [
        root / "docs/source-of-truth/03-Architecture-Baseline.md",
        root / "docs/source-of-truth/04-Component-and-Agent-Catalogue.md",
        root / "docs/source-of-truth/05-Data-and-Schema-Register.md",
        root / "docs/source-of-truth/06-ADR-Register.md",
        root / "docs/source-of-truth/09-Stage-Handoff-Pack.md",
        root / "docs/architecture/diagrams/GRAPH-001-v1.3.0.mmd",
    ]
    missing = [str(path.relative_to(root)) for path in required if not path.exists()]
    if missing:
        raise SystemExit(f"missing required files: {missing}")

    corpus = "\n".join(path.read_text(encoding="utf-8") for path in required)
    assertions = {
        "exactly one active agent": "exactly one active `AGT-001`" in corpus,
        "graph version": "GRAPH-001/1.3.0" in corpus,
        "no protected concurrent writes": "no concurrent protected-state writes" in corpus,
        "advisory capacity": "advisory" in corpus.lower(),
        "inactive multi-agent profile": "WP-008" in corpus and "inactive_future" in corpus,
        "overlay exception": "ISS-096" in corpus,
    }
    failed = [name for name, passed in assertions.items() if not passed]
    if failed:
        raise SystemExit(f"consistency audit failed: {failed}")
    print("Stage 7B consistency audit passed with recorded reconstruction exception ISS-096")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
