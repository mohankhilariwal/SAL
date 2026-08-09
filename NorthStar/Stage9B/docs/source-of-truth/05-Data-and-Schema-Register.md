# 05 - Data and Schema Register (S09B overlay)

Preserve `DATA-001`-`176` and `INT-001`-`139`. Add:

| ID | Object | Version | Location |
|---|---|---|---|
| `DATA-177` | PrincipalIdentity | `1.0.0` | S09B schema in `/schemas` |
| `DATA-178` | AgentExecutionIdentity | `1.0.0` | S09B schema in `/schemas` |
| `DATA-179` | DelegationRequest | `1.0.0` | S09B schema in `/schemas` |
| `DATA-180` | AttenuatedAuthorizationGrant | `1.0.0` | S09B schema in `/schemas` |
| `DATA-181` | ProofOfPossessionBinding | `1.0.0` | S09B schema in `/schemas` |
| `DATA-182` | ApprovalAuthorizationBinding | `1.0.0` | S09B schema in `/schemas` |
| `DATA-183` | RevocationRecord | `1.0.0` | S09B schema in `/schemas` |
| `DATA-184` | GrantUseRecord | `1.0.0` | S09B schema in `/schemas` |
| `DATA-185` | PolicyDecision | `1.0.0` | S09B schema in `/schemas` |
| `DATA-186` | ToolInvocationAuthorizationContext | `1.0.0` | S09B schema in `/schemas` |
| `DATA-187` | BlastRadiusBudget | `1.0.0` | S09B schema in `/schemas` |
| `DATA-188` | BlastRadiusDecision | `1.0.0` | S09B schema in `/schemas` |
| `DATA-189` | AuthorizationAuditEvidence | `1.0.0` | S09B schema in `/schemas` |
| `DATA-190` | IdentityAuthorizationSnapshot | `1.0.0` | S09B schema in `/schemas` |
| `DATA-191` | ThreatModelDelta | `1.0.0` | S09B schema in `/schemas` |
| `DATA-192` | Stage9BReport | `1.0.0` | S09B schema in `/schemas` |

| ID | Interface |
|---|---|
| `INT-140` | Resolve human identity claims |
| `INT-141` | Attest workload identity |
| `INT-142` | Bind agent execution identity |
| `INT-143` | Exchange context for attenuated grant |
| `INT-144` | Verify grant signature/claims |
| `INT-145` | Verify proof of possession |
| `INT-146` | Evaluate authorization policy |
| `INT-147` | Authorize retrieval/context |
| `INT-148` | Authorize tool invocation |
| `INT-149` | Consume use/proof nonce |
| `INT-150` | Revoke/check/introspect grant |
| `INT-151` | Verify approval binding |
| `INT-152` | Evaluate/reserve blast radius |
| `INT-153` | Emit authorization evidence |
| `INT-154` | Validate/export S09B snapshot/report |

No S09B evaluation/audit object can approve/finalize or mutate protected case state.
