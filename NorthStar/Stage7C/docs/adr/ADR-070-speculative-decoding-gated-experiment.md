# ADR-070 — Speculative Decoding Is a Disabled-by-Default, Profile-Gated Experiment

- **Status:** Accepted
- **Date:** 2026-08-01

## Context
Speculative decoding can preserve a target distribution when implemented with correct verification, but benefit depends on draft cost, acceptance, verification, output length, batch size, concurrency and memory. Tool-dominated NorthStar workflows may see little end-to-end benefit.

## Decision
Keep speculative decoding disabled by default. The first eligible local-compatible experiment is prompt-lookup speculation for long, input-grounded, low-to-moderate-concurrency profiles. Draft-model, self-speculative, MTP and Medusa-style methods remain candidates only after a concrete compatible model/runtime exists. Promotion requires quality parity, lossless-distribution evidence where claimed, minimum acceptance, minimum decode improvement, minimum end-to-end improvement and maximum memory overhead. Failure of any gate disables speculation for that profile.

## Alternatives
Enable globally; never evaluate; use draft-model speculation first; or profile-gated experimentation.

## Rationale
Profile gating captures the technique's real operating envelope and avoids treating a decode microbenchmark as workflow proof.

## Consequences
Every run must record method, draft/target identity, tokenizer, lookahead, acceptance distribution, verification cost, concurrency, memory and quality evidence.

## Risks and mitigations
Low acceptance, target-verification dominance, draft contention and KV overhead are mitigated by negative tests, baseline comparisons and automatic recommendation rollback—not automatic runtime changes.

## Review triggers
Measured NorthStar traces, a selected model/runtime, or new native speculative support.
