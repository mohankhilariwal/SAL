# 05 — Data and Schema Register (1.9.0 Overlay)

All accepted `DATA-001`–`130` and `INT-001`–`102` remain.

## New data

| ID | Name | Owner | Invariant |
|---|---|---|---|
| `DATA-131` | EvaluationSuite | CMP-008/CMP-011 | Versioned suite, datasets, graders, coverage and authority_effect=none |
| `DATA-132` | EvaluationDataset | CMP-008 | Immutable dataset version and split inventory |
| `DATA-133` | EvaluationCase | CMP-008 | Task, expected outcome, assertions, provenance and scope |
| `DATA-134` | GroundTruthReference | CMP-008/domain owner | Versioned evidence-backed expected state |
| `DATA-135` | EvaluationRubric | CMP-008 | Criteria/anchors; model judging not active |
| `DATA-136` | GraderSpecification | CMP-008 | Type, version, inputs and failure semantics |
| `DATA-137` | EvaluationRun | CMP-008 | Candidate/suite/environment identity |
| `DATA-138` | TrialRecord | CMP-008/CMP-009 | Isolated payload-minimized trial |
| `DATA-139` | EvaluationResult | CMP-008 | Advisory aggregation and mandatory gates |
| `DATA-140` | DatasetLineageRecord | CMP-011 | Case/file digests and provenance |
| `DATA-141` | ContaminationAssessment | CMP-008 | Method, threshold, findings and limitations |
| `DATA-142` | HumanReviewAssignment | CMP-006 | Risk-based sample; decision remains human |

## New interfaces

| ID | Name | Control |
|---|---|---|
| `INT-103` | Evaluation Suite Registry | Fails closed on missing version/scope/integrity or authority crossing |
| `INT-104` | Dataset Registry and Version Resolution | Fails closed on missing version/scope/integrity or authority crossing |
| `INT-105` | Authorized Case Materialization | Fails closed on missing version/scope/integrity or authority crossing |
| `INT-106` | Isolated Evaluation Execution | Fails closed on missing version/scope/integrity or authority crossing |
| `INT-107` | Deterministic Grader Execution | Fails closed on missing version/scope/integrity or authority crossing |
| `INT-108` | Human Review Sampling | Fails closed on missing version/scope/integrity or authority crossing |
| `INT-109` | Result Aggregation | Fails closed on missing version/scope/integrity or authority crossing |
| `INT-110` | Dataset Promotion or Quarantine | Fails closed on missing version/scope/integrity or authority crossing |
| `INT-111` | Evaluation Evidence Export | Fails closed on missing version/scope/integrity or authority crossing |

JSON schemas exist at `schemas/DATA-131.schema.json` through `DATA-142.schema.json`.
