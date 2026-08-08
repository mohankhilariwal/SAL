from __future__ import annotations

from pathlib import Path


def main() -> None:
    root = Path(__file__).parents[1]
    stage = (root / "docs/stages/Stage-3B-Single-Agent-Loop-and-Termination.md").read_text()
    handoff = (root / "docs/source-of-truth/09-Stage-Handoff-Pack.md").read_text()
    required = [
        "AGT-001 Regulatory Impact Assessment Agent",
        "TOOL-001", "TOOL-006", "DATA-009", "DATA-044", "INT-025",
        "ADR-022", "ADR-023", "preliminary_grounded_unapproved",
        "Stage 3C — Loop Failure Handling, Recovery and Runtime Budgets",
    ]
    for token in required:
        if token not in stage or token not in handoff:
            raise SystemExit(f"Consistency token absent: {token}")
    forbidden = ["agt-002", "multi-agent implemented", "durable checkpoint implemented", "memory implemented"]
    for token in forbidden:
        if token in stage.lower() or token in handoff.lower():
            raise SystemExit(f"Forbidden capability claim found: {token}")
    print("Stage 3B consistency audit: PASSED WITH RECORDED EXCEPTIONS")


if __name__ == "__main__":
    main()
