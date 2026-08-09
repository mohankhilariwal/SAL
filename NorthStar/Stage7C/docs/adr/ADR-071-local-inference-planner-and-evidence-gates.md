# ADR-071 — Standard-Library Inference Planner and Toy Lossless Speculation Lab

- **Status:** Accepted
- **Date:** 2026-08-01

## Context
NorthStar still lacks a live inference endpoint and GPU. It needs runnable validation without inventing production performance.

## Decision
Implement a deterministic standard-library planner, analytical proxy and tiny Markov-model speculative-sampling lab. The lab verifies rejection-correction distribution semantics statistically; the proxy evaluates policy arithmetic and negative gates. All results are labelled simulated. `DATA-130` recommendations remain advisory and cannot grant authority, mutate `DATA-106`, approve a case or change a route.

## Alternatives
Documentation only; require paid GPU access; embed vendor SDKs now; or local evidence plus future adapters.

## Rationale
The selected option makes architecture constraints executable while maintaining a clean distinction between semantic correctness, simulated sensitivity and endpoint evidence.

## Consequences
No claim of production speedup, capacity, model quality or cost is permitted. External adapters must preserve canonical data contracts.

## Risks and mitigations
Proxy overconfidence is mitigated through evidence-kind labels, required endpoint gates and explicit limitations.

## Review triggers
Endpoint access, measured traces, model selection or production telemetry availability.
