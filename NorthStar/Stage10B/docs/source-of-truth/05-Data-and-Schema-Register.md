# 05 — Data and Schema Register: Stage 10B Overlay

Version: `1.16.0`

Preserve `DATA-001`–`236`. Add:

| ID | Name | Owner | Purpose |
|---|---|---|---|
| `DATA-237` | FailureEnvelope | `CMP-003` | Safe failure context and correlation. |
| `DATA-238` | FailureClassification | `CMP-003` | Transience, ambiguity, effect and retry decision inputs. |
| `DATA-239` | RetryPolicy | `CMP-010`/`CMP-011` | Attempts, budget, backoff and allowed classes. |
| `DATA-240` | TimeoutPolicy | `CMP-010` | Connect, request, operation and workflow deadlines. |
| `DATA-241` | CircuitBreakerPolicy | `CMP-010` | Threshold, open interval and half-open probes. |
| `DATA-242` | BulkheadPolicy | `CMP-010` | Capacity partition and rejection behavior. |
| `DATA-243` | DeadLetterRecord | `CMP-003` | Quarantined message metadata and controlled redrive evidence. |
| `DATA-244` | WorkflowCheckpoint | `CMP-003` | Atomic, digest-verified resumable workflow state. |
| `DATA-245` | RecoveryDecision | `CMP-003` | Deterministic recovery action with no authority effect. |
| `DATA-246` | CompensationPlan | `CMP-005` | Explicit reverse/mitigation action subject to current controls. |
| `DATA-247` | DegradedModeProfile | `CMP-003`/`CMP-007` | Allowed partial modes and fail-closed boundaries. |
| `DATA-248` | IncidentRecord | `CMP-009`/`CMP-011` | Severity, timeline, owners, evidence and status. |
| `DATA-249` | ChaosExperiment | `CMP-008` | Bounded fault hypothesis, target and abort criteria. |
| `DATA-250` | ChaosResult | `CMP-008` | Invariant and recovery results. |
| `DATA-251` | RecoveryStatusReport | `CMP-010` | Current circuits, backlog, checkpoints and degradation. |
| `DATA-252` | ReleaseManifest | `CMP-011` | Version/digest-bound release evidence. |
| `DATA-253` | DeploymentEnvironmentProfile | `CMP-010`/`CMP-011` | Environment boundaries and route status. |
| `DATA-254` | PromotionDecision | `CMP-011` | Gate results and reasons; non-authorizing. |
| `DATA-255` | RollbackPlan | `CMP-010`/`CMP-011` | Software/config rollback plus explicit compensation references. |
| `DATA-256` | RuntimeSLO | `CMP-011` | Provisional non-production reliability objectives. |

All schemas require `authority_effect: none`. None can serve as a grant, approval or business-state mutation.
