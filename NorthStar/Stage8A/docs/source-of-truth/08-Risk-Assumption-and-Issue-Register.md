# 08 — Risk, Assumption and Issue Register (1.9.0 Overlay)

## New risks

| ID | Risk | Status | Treatment |
|---|---|---|---|
| `RSK-248` | Synthetic dataset misrepresents production distribution | Open | Add approved production-derived samples later |
| `RSK-249` | Golden-answer ambiguity | Open | Domain review, permissible variants and adjudication |
| `RSK-250` | Cross-split leakage | Controlled local | Digests and near-duplicate checks |
| `RSK-251` | Provider training contamination | Open | Private held-back tests and uncertainty disclosure |
| `RSK-252` | Test-set overfitting through repeated tuning | Open | Exposure logging and rotation |
| `RSK-253` | Grader bug or underspecification | Controlled local | Reference solutions and grader tests |
| `RSK-254` | Evaluation prompt injection | Open for future judge | Deterministic graders now; adversarial judge tests later |
| `RSK-255` | Unauthorized dataset access | Open production | CMP-007 authorization and data classification |
| `RSK-256` | Reference answer contains privileged interpretation | Open | Classification, access, temporal validity |
| `RSK-257` | Aggregate score masks catastrophic failure | Controlled | Mandatory binary gates |
| `RSK-258` | Dirty environment creates correlated results | Controlled local | Per-trial environment IDs; future reset proof |
| `RSK-259` | Flaky dependency causes false regression | Open live | Retries separated from score and environment health |
| `RSK-260` | Perfect score from narrow coverage | Controlled | Required categories and saturation review |
| `RSK-261` | Multilingual undercoverage | Open | French synthetic only; add expert cases |
| `RSK-262` | Temporal drift invalidates labels | Open | Effective-date metadata and review triggers |
| `RSK-263` | Human reviewer disagreement/fatigue | Open | Instructions, calibration, sampling and adjudication |
| `RSK-264` | Raw payload or personal data enters evaluation evidence | Controlled local | Validation and payload-minimized export |
| `RSK-265` | Evaluation result becomes de facto authority | Controlled | authority_effect=none and negative tests |
| `RSK-266` | Local harness diverges from production scaffold | Open | Production-equivalence adapter and trace replay |
| `RSK-267` | Model selection remains delayed | Accepted | Evaluation evidence is prerequisite |
| `RSK-268` | Evaluation cost grows without value | Open | Risk-based sampling and suite tiers |
| `RSK-269` | Dataset case ownership unclear | Open | Registry owner/review dates |
| `RSK-270` | Sealed test only logically protected | Open | Future access-controlled store |
| `RSK-271` | Near-duplicate threshold misses semantic leakage | Open | Human review and stronger methods later |
| `RSK-272` | Business metric not represented by proxy gates | Open | Stage 8B outcome metrics |
| `RSK-273` | Future LLM judge bias | Deferred | Stage 8C |
| `RSK-274` | Evaluation evidence retention conflicts with privacy | Open | Retention schedule and minimization |

## New assumptions

- `ASM-081`: synthetic cases are adequate only for architecture-contract validation.
- `ASM-082`: future production candidate adapters can emit the canonical outcome/trace contract.
- `ASM-083`: domain owners will provide temporal labels and permissible outcomes.
- `ASM-084`: independent cases may be evaluated concurrently when environments are isolated.
- `ASM-085`: test exposure can be governed by a future access-controlled registry.
- `ASM-086`: deterministic hard gates remain outside probabilistic reasoning.
- `ASM-087`: Stage 8B will define metrics/thresholds before deployment gates are activated.

## New issues

- `ISS-114`: Stage 7D was not executed; model selection/routing remains unresolved. S08A is treated as its evidence prerequisite.
- `ISS-115`: no live candidate model or endpoint is evaluated.
- `ISS-116`: no production-derived dataset or representative distribution.
- `ISS-117`: no approved annotation guide or inter-rater study.
- `ISS-118`: no independent expert/human evaluation executed.
- `ISS-119`: no online, shadow, canary or A/B evaluation.
- `ISS-120`: no LLM judge, calibration or bias laboratory.
- `ISS-121`: no enterprise dataset registry, exposure log or WORM backend.
- `ISS-122`: Mermaid was syntax-reviewed but not CLI-rendered.

Inherited `ISS-096` and all unresolved production gaps remain.
