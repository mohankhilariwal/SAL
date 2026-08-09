# NorthStar Agentic Compliance — Stage 6C

Version `1.5.0`. This package adds a serialized HTTP/JSON reference boundary plus deterministic MCP and A2A protocol mappings to the accepted `DATA-091`–`099` handoff contracts.

It preserves exactly one active `AGT-001`, keeps the evidence verifier as `candidate_sandbox_only`, and does not enable concurrent execution, shared state, shared memory, a production MCP server or a production A2A endpoint.

## Run

```bash
python -m compileall -q src scripts
pytest
PYTHONPATH=src python scripts/run_stage6c_demo.py
PYTHONPATH=src python scripts/run_stage6c_evaluation.py
PYTHONPATH=src python scripts/benchmark_stage6c.py
PYTHONPATH=src python scripts/validate_stage6c.py
PYTHONPATH=src python scripts/consistency_audit_stage6c.py
```

The local HTTP process-boundary integration test starts a single-threaded loopback server and sends one request at a time. It is not a production HTTPS, mTLS, OAuth, DPoP, KMS, audit or durable-delivery implementation.
