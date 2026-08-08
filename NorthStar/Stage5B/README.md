# NorthStar Agentic Compliance — Stage 5B

Version `1.2.0` adds deterministic context regeneration, extractive compaction, and an opt-in case-local working-memory boundary to the accepted Stage 5A architecture.

The implementation deliberately does **not** add cross-case recall, semantic memory, episodic memory, user-profile memory, organizational memory, shared-agent memory, multiple agents, concurrent graph branches, MCP/A2A, a production control plane, or an audit/WORM ledger.

## Run

```bash
python -m pip install -e .
pytest
python scripts/run_stage5b_demo.py
python scripts/run_stage5b_evaluation.py
python scripts/benchmark_stage5b.py
python scripts/validate_stage5b.py
python scripts/consistency_audit_stage5b.py
```

Tested on Python `3.13.5` with standard-library runtime code and pytest `9.0.2`.
