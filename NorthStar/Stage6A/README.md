# NorthStar Agentic Compliance — Stage 6A

Local/offline reference implementation for **S06A — Single-Agent versus Multi-Agent Architecture Decision and Agent Boundary Analysis**.

The accepted runtime keeps exactly one `AGT-001`, `AGT-001-spec 1.1.0`, `GRAPH-001 1.1.0`, `DATA-009 1.1.0`, gateway-only `TOOL-001`–`006`, external human approval, case-local harness-owned working memory, and no delegation, handoff, shared-agent memory, concurrency, MCP or A2A.

```bash
python3 -m compileall -q src scripts
python3 -m pytest -q
python3 scripts/run_stage6a_demo.py
python3 scripts/run_stage6a_evaluation.py
python3 scripts/benchmark_stage6a.py
python3 scripts/validate_stage6a.py
python3 scripts/consistency_audit_stage6a.py
```

Runtime modules use only Python's standard library. Tests use pytest 9.0.2.
