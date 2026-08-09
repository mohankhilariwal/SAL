# Final Threat-Model Summary

`TM-001/1.4.0` remains the accepted threat model. Stage 11 adds no new runtime attack surface; it consolidates current and inactive-future scope.

## Current trust boundaries

- TB-00 external sources and human environment.
- TB-01 experience/intake.
- TB-02 orchestration and the single active agent.
- TB-03 knowledge and enterprise integrations.
- TB-04 human authority, identity and policy.
- TB-05 assurance, observability, audit and runtime.
- TB-06 governance and configuration.
- TB-07 future interoperability and multi-agent boundary, inactive.

## Highest residual production threats

1. Production identity, key, signing and policy-distribution compromise.
2. Audit-log destruction or inability to prove time, integrity and retention.
3. Prompt/retrieval/tool-result injection under live data and model behaviour.
4. Cross-tenant or excessive-authority failure in enterprise integration.
5. Supply-chain or provenance compromise at deployment admission.
6. Resource exhaustion, cost attack and overload under representative demand.
7. Recovery failure, stale data or duplicate protected effects during regional disruption.
8. Judge/evaluation manipulation and unrepresentative quality evidence.
9. Human automation bias, reviewer fatigue and separation-of-duties breakdown.
10. Future agent/protocol spoofing if inactive surfaces are later enabled.

Hard authority, approval, tenant-isolation, audit, integrity, code-execution and production-gate failures remain non-overridable. Threat-treatment outputs have `authority_effect: none`.
