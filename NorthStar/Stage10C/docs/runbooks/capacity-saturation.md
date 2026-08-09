# Capacity Saturation Runbook

1. Identify model, retrieval, queue, audit, tool or human-review bottleneck.
2. Enforce bounded admission and queue age.
3. Preserve one concurrent protected write.
4. Load-shed only eligible low-priority work.
5. Do not auto-approve human work or bypass audit/policy.
6. Re-run the affected workload profile and update capacity evidence.
