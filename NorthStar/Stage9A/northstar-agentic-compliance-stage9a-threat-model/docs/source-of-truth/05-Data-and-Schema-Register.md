# 05 Data and Schema Register - S09A Overlay

Preserve `DATA-001`-`164`, `INT-001`-`129` and `TOOL-001`-`006`.

## New data objects

| ID | Contract | Owner/authority |
|---|---|---|
| `DATA-165` | ThreatModelScope and architecture snapshot | `CMP-008` with `CMP-011` governance; `authority_effect: none` |
| `DATA-166` | TrustBoundary | `CMP-008` with `CMP-011` governance; `authority_effect: none` |
| `DATA-167` | DataFlow | `CMP-008` with `CMP-011` governance; `authority_effect: none` |
| `DATA-168` | ThreatActor | `CMP-008` with `CMP-011` governance; `authority_effect: none` |
| `DATA-169` | ThreatScenario | `CMP-008` with `CMP-011` governance; `authority_effect: none` |
| `DATA-170` | STRIDEAssessment | `CMP-008` with `CMP-011` governance; `authority_effect: none` |
| `DATA-171` | AttackTree | `CMP-008` with `CMP-011` governance; `authority_effect: none` |
| `DATA-172` | MisuseCase | `CMP-008` with `CMP-011` governance; `authority_effect: none` |
| `DATA-173` | ControlMapping | `CMP-008` with `CMP-011` governance; `authority_effect: none` |
| `DATA-174` | ThreatRiskAssessment | `CMP-008` with `CMP-011` governance; `authority_effect: none` |
| `DATA-175` | ThreatModelReport | `CMP-008` with `CMP-011` governance; `authority_effect: none` |
| `DATA-176` | ThreatTreatmentRecommendation | `CMP-008` with `CMP-011` governance; `authority_effect: none` |

## New interfaces

| ID | Contract | Enforcement |
|---|---|---|
| `INT-130` | Load/version architecture snapshot | authenticated design-time access; no runtime mutation |
| `INT-131` | Register trust boundaries, assets and actors | authenticated design-time access; no runtime mutation |
| `INT-132` | Enumerate and validate data flows | authenticated design-time access; no runtime mutation |
| `INT-133` | Generate STRIDE and OWASP agentic crosswalk | authenticated design-time access; no runtime mutation |
| `INT-134` | Build/validate attack trees | authenticated design-time access; no runtime mutation |
| `INT-135` | Register/validate misuse cases | authenticated design-time access; no runtime mutation |
| `INT-136` | Calculate ordinal inherent/residual risk | authenticated design-time access; no runtime mutation |
| `INT-137` | Map preventive/detective/response controls and tests | authenticated design-time access; no runtime mutation |
| `INT-138` | Produce threat-model report | authenticated design-time access; no runtime mutation |
| `INT-139` | Export advisory treatment recommendation | authenticated design-time access; no runtime mutation |

No object writes `DATA-106`, changes a route, grants authority, approves/finalizes, creates an agent or deploys a control.
