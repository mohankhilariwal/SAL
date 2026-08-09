# NorthStar Stage 9B — Identity, Authorization and Blast-Radius Controls

Architecture/repository/handoff version: `1.13.0`  
Graph version: `GRAPH-001/1.9.0`  
Authorization model: `AUTH-001/1.0.0`  
Blast-radius model: `BR-001/1.0.0`

This repository is a compatible Stage 9B overlay reconstructed from the accepted Stage 9A handoff. It preserves exactly one active agent (`AGT-001`) and does not activate a production identity provider, OAuth authorization server, SPIFFE/SPIRE deployment, enterprise KMS, model route, deployment gate, MCP/A2A runtime, second agent, broader guardrail architecture or control-plane implementation.

The executable local reference demonstrates:

- human, workload, agent-execution, service and tool identities;
- short-lived, audience-bound, case/run/task-bound attenuated grants;
- no unrestricted user credential passthrough;
- Ed25519-signed local grant envelopes and request proofs;
- proof-key binding, request nonce replay protection, expiry, use limits and revocation;
- receiver-side policy enforcement at the enterprise tool gateway;
- autonomy/authority tiers and per-run blast-radius budgets;
- negative authorization tests and threat-model deltas.

The local grant format is **not** a JWT, OAuth token, DPoP proof, mTLS certificate or SPIFFE SVID. It is a deterministic teaching implementation mapped to those production patterns.

## Run

```bash
python -m venv .venv
. .venv/bin/activate
pip install -e '.[test]'
pytest
python scripts/run_stage9b_demo.py
python scripts/run_stage9b_evaluation_gates.py
python scripts/validate_stage9b.py
python scripts/consistency_audit_stage9b.py
```
