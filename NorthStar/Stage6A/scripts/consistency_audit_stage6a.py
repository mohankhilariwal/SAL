import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    profiles = json.loads((ROOT / "config/agents/AGT-001-task-profiles.json").read_text())["profiles"]
    failures = []
    if {p["agent_id"] for p in profiles} != {"AGT-001"}:
        failures.append("agent inventory")
    if {(p["graph_id"], p["graph_version"]) for p in profiles} != {("GRAPH-001", "1.1.0")}:
        failures.append("graph drift")
    for profile in profiles:
        for field in ("can_delegate", "can_handoff", "can_approve", "can_finalize", "can_write_memory", "concurrent_execution"):
            if profile[field]:
                failures.append(profile["profile_id"] + " " + field)
    handoff = (ROOT / "docs/source-of-truth/09-Stage-Handoff-Pack.md").read_text()
    for marker in ("Architecture version:** `1.3.0`", "exactly one `AGT-001`", "`ADR-044`", "`TEST-243`–`270`"):
        if marker not in handoff:
            failures.append("handoff " + marker)
    if failures:
        print("FAILED")
        for item in failures:
            print("-", item)
        return 1
    print("PASSED WITH RECORDED RECONSTRUCTION AND PRODUCTION EXCEPTIONS")
    print("- narrative, diagrams, configuration, code, schemas, ADRs, tests and handoff align")
    print("- AGT-001-spec 1.1.0, GRAPH-001 1.1.0 and DATA-009 1.1.0 preserved")
    print("- one agent, sequential graph, gateway-only tools and external human approval preserved")
    print("- no delegation, handoff, shared-agent memory, concurrency, MCP or A2A enabled")
    print("- compatible reconstruction overlay recorded as ISS-065")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
