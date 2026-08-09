# ADR-085: Use repeated paired estimands with uncertainty

- Status: Accepted
- Date: 2026-08-01

## Context
The S08B baseline already proved judge contracts and a small replay bias lab. The explicit S08C request requires a deeper laboratory while the handoff expected a different stage.

## Decision
Require at least three repetitions, stable seeds/digests, paired deltas, bootstrap intervals and exact McNemar tests.

## Alternatives
Continue directly to deployment gates; repeat S08B unchanged; call a live provider model; use unpaired convenience samples; aggregate all biases into one score.

## Rationale
The selected design preserves the user's stage boundary, creates falsifiable measurement evidence and retains all NorthStar authority and non-activation constraints.

## Consequences
More trials, dataset/version governance and analysis cost; clearer attribution of bias signals; synthetic evidence remains non-production.

## Risks and mitigations
Matched pairs can still be semantically unequal; human review, digests, canaries, slice reports and new dataset versions are required.

## Review triggers
Live-model onboarding, real expert labels, new language/locale, rubric or judge change, adaptive attack discovery, or implementation of metrics/regression/deployment gates.
