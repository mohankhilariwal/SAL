# Final Operating Runbook Index

| Scenario | Primary owner | Required response |
|---|---|---|
| Prompt/retrieval injection | Marcus | Quarantine evidence, preserve trace, deny protected effects, investigate source and guardrails. |
| Authorization or replay failure | Marcus | Fail closed, revoke/inspect grant, preserve proof and receiver evidence. |
| Audit intent/outcome failure | Liam | Block protected effect, restore audit path, reconcile in-flight outcome. |
| Ambiguous protected write | Liam / Elena | Use `CMP-005` reconciliation before any repeat. |
| Model or retrieval outage | Liam | Apply classified retry/circuit/degraded-mode policy; never convert partial result to approval. |
| Queue/capacity saturation | Liam | Enforce admission, backpressure, load shedding for allowed work and preserve protected-write limit. |
| Budget anomaly | Elena / Daniel | Stop optional work, preserve mandatory controls and reconcile in-flight effects. |
| Human approval timeout | Maya / Daniel | Keep pending, escalate; timeout never approves. |
| Policy bundle invalid/stale | Sofia / Marcus | Fail closed for affected hard controls; restore approved immutable bundle. |
| Checkpoint corruption | Liam | Reject resume, preserve evidence, restore valid checkpoint or perform manual recovery. |
| Dead-letter redrive | Liam / Marcus | Authenticate operator, review cause, reauthorize and preserve causation/idempotency. |
| Compensation | Aisha / Liam | Treat as a new controlled action through `CMP-005`; obtain required approval. |
| Deployment rollback | Elena / Liam | Verify rollback manifest, preserve audit and avoid schema/state incompatibility. |
| DR exercise | Aisha / Liam | Use approved scenario, measure RTO/RPO and record gaps; exercise result cannot self-approve. |
| Emergency stop | Marcus / Daniel | Stop admissions/actions through authorized control; preserve forensic evidence and human command. |
| Final production review | Priya / Sofia | Rebuild evidence index, close every hard blocker, rerun full cumulative suite and seek external deployment authority. |
