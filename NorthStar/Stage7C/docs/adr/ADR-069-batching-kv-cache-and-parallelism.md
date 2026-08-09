# ADR-069 — Runtime-Owned Batching and Explicit KV-Cache Pressure Evidence

- **Status:** Accepted
- **Date:** 2026-08-01

## Context
Continuous batching, chunked prefill, quantization and model parallelism can improve throughput or fit, but they can also worsen TTFT, fairness, communication overhead and memory pressure.

## Decision
Treat batching, KV-cache allocation, quantization and parallelism as serving-runtime policies inside `CMP-010`. `CMP-003` keeps workflow admission ownership. Managed providers expose only declared capabilities and observed metrics. Self-hosted candidates must benchmark cold, warm and representative cache states, mixed profiles, fairness, OOM behaviour and quality parity. No parallelism topology or quantization mode is selected for production in S07C.

## Alternatives
Application-managed batching; fixed universal batch sizes; quantize by default; or workload-gated runtime tuning.

## Rationale
The runtime has the information required for token-level scheduling; the orchestrator must not become a GPU scheduler. Workload-specific gates prevent throughput gains from hiding interactive regressions.

## Consequences
A serving adapter must normalize queue, TTFT, ITL, KV memory, rejection and fairness evidence. Configuration remains explicit and versioned.

## Risks and mitigations
Starvation and OOM are mitigated through bounded token budgets, profile-aware tests and fail-closed admission. Quality changes from quantization require existing task evaluators.

## Review triggers
A concrete serving engine/model/hardware selection or mixed-profile endpoint benchmark.
