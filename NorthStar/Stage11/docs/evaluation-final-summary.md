# Final Evaluation Summary

NorthStar’s evaluation hierarchy includes deterministic unit and contract tests, retrieval tests, agent-loop and graph-path tests, security tests, performance proxies, synthetic golden and adversarial datasets, human-review contracts, model-judge contracts, judge-bias probes, threat misuse cases, reliability/chaos exercises and FinOps/capacity/readiness checks.

## Evidence classifications

- **Strong local deterministic evidence:** schema/contract validation, stable identifier checks, authority denial, tool gateway, route ownership, retry/reconciliation, one-protected-write and final-route denial.
- **Useful local synthetic evidence:** retrieval quality on small corpora, judge-bias probes, threat scenarios, simulated workload/cost and local chaos exercises.
- **Proposed evidence:** SLOs, error budgets, RTO/RPO, regional and operating profiles.
- **Missing production evidence:** live model quality, representative human calibration, production traffic, provider billing, enterprise control plane, audit durability, provenance/admission, multi-region recovery and legal/compliance approval.

No local score or pass count is interpreted as production accuracy, fairness, reliability, cost or certification evidence. Stage 11 adds `EVAL-273`–`284` to prove package reconciliation, route denial, one-agent preservation, blocker semantics, RACI, diagrams, summaries, assignment and bibliography presence.
