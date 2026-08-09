# Non-Production Deployment and Rollback Runbook — Stage 10B

1. Verify the release manifest binds source, config, graph, agent spec and test evidence.
2. Verify unit, integration, security, schema, chaos and compatibility gates.
3. Require authenticated human release approval.
4. Confirm target environment is local, shared-dev, test or pre-production.
5. Confirm `production_route_enabled=false` and `NORTHSTAR_PRODUCTION_PROMOTION_ENABLED=false`.
6. Deploy using the reference rolling strategy and monitor readiness, error rate, retry rate, circuit state and audit failures.
7. Stop the rollout on failed readiness or recovery invariant.
8. Roll back software/config to the prior manifest.
9. Do not assume rollback reverses completed external effects. Invoke a separately approved compensation through `CMP-005` where permitted.
10. Record release, rollback, incident and compensation references in `CMP-009`.
