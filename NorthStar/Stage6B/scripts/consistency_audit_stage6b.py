from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    checks = {
        "versions_1_4_0": all("1.4.0" in (ROOT / "docs/source-of-truth" / name).read_text() for name in [
            "00-Project-Constitution.md", "03-Architecture-Baseline.md", "07-Repository-Manifest.md", "09-Stage-Handoff-Pack.md"
        ]),
        "one_active_agent": '"active_agent_ids": ["AGT-001"]' in (ROOT / "config/architecture/handoff-policy-v1.json").read_text(),
        "graph_version_preserved": "GRAPH-001 1.1.0" in (ROOT / "docs/source-of-truth/03-Architecture-Baseline.md").read_text(),
        "state_version_preserved": "DATA-009 1.1.0" in (ROOT / "docs/source-of-truth/03-Architecture-Baseline.md").read_text(),
        "no_protocol_selection": '"protocol_selected": false' in (ROOT / "config/architecture/handoff-policy-v1.json").read_text(),
        "no_concurrency": '"concurrent_execution": false' in (ROOT / "config/architecture/handoff-policy-v1.json").read_text(),
        "tests_range_documented": "TEST-271" in (ROOT / "docs/source-of-truth/09-Stage-Handoff-Pack.md").read_text() and "TEST-306" in (ROOT / "docs/source-of-truth/09-Stage-Handoff-Pack.md").read_text(),
        "eval_range_documented": "EVAL-062" in (ROOT / "docs/source-of-truth/09-Stage-Handoff-Pack.md").read_text() and "EVAL-069" in (ROOT / "docs/source-of-truth/09-Stage-Handoff-Pack.md").read_text(),
    }
    failed = [name for name, passed in checks.items() if not passed]
    lines = ["Stage 6B Consistency Audit", ""] + [f"- {name}: {'PASS' if passed else 'FAIL'}" for name, passed in checks.items()]
    lines += ["", "Result: " + ("PASSED WITH RECORDED RECONSTRUCTION AND PRODUCTION EXCEPTIONS" if not failed else "FAILED")]
    (ROOT / "reports/Stage-6B-Consistency-Audit.txt").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
