# NorthStar Agentic Compliance — Stage 7C

This compatible `1.8.0` repository overlay implements a provider-neutral inference optimization planner, local analytical proxy, quality/performance gates and a tiny lossless speculative-sampling laboratory for the NorthStar playbook.

It preserves exactly one active `AGT-001`, gateway-only tools, external human authority, bounded concurrency and advisory-only admission/optimization evidence.

## What is implemented

- Managed-default, self-hosted-candidate and local-simulated deployment profiles.
- Workload-specific optimization plans for `WP-001`–`007`.
- Exact cache isolation and semantic regulatory-answer cache prohibition.
- Batching, chunked-prefill, quantization, parallelism and speculative candidate assessments.
- Disabled-by-default profile-gated speculative policy.
- Toy distribution-preserving speculative sampling.
- Transparent simulated baseline/candidate metrics.
- `EVAL-101`–`115` and 58 pytest cases.

## What is not implemented

No live model, GPU, endpoint, production cache, serving runtime, quantization, parallelism, autoscaling, routing or production speedup/capacity claim.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[test]'
python -m compileall -q src tests scripts
pytest -q
python scripts/run_stage7c_inference_plan.py
python scripts/run_stage7c_demo.py
python scripts/run_stage7c_speculative_benchmark.py
python scripts/run_stage7c_evaluation.py
python scripts/validate_stage7c.py
python scripts/consistency_audit_stage7c.py
```

See `docs/stages/NorthStar-Stage-7C-Inference-Optimization-and-Speculative-Decoding.md` and `NorthStar-Stage-7C-Handoff-Pack.md`.
