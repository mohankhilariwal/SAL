# ADR-067 — Managed Inference Default with a Governed Self-Hosted Benchmark Lane

- **Status:** Accepted
- **Date:** 2026-08-01

## Context
NorthStar has workload evidence but no selected model, serving engine or accelerator. Managed APIs reduce operational burden, while self-hosted serving can improve control, residency and optimization access but introduces GPU, scheduler, patching, observability and reliability ownership.

## Decision
Use a provider-neutral managed inference profile as the default production deployment class. Maintain a version-pinned self-hosted profile only as a governed candidate benchmark lane until workload-specific quality, residency, security, performance, reliability and cost gates justify promotion.

## Alternatives
1. Self-host immediately.
2. Managed-only with no exit path.
3. Hybrid routing immediately.
4. Managed default plus self-hosted evidence lane.

## Rationale
The fourth option preserves local and sovereign optionality without pretending NorthStar has selected hardware or has the operating maturity to run production inference.

## Consequences
Managed provider batching and kernel choices remain opaque. The self-hosted lane requires reproducible profiles and full-stack measurements. No automatic routing is introduced.

## Risks and mitigations
Vendor dependency is mitigated through canonical contracts and portable evidence. Self-hosted benchmark drift is mitigated by pinned runtime/model/tokenizer/hardware metadata.

## Review triggers
Measured residency need, unacceptable managed cost/latency, vendor concentration risk, approved open-weight model, or completed self-hosted SRE readiness review.
