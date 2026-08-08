from pathlib import Path
root=Path(__file__).resolve().parents[1]
chapter=(root/'docs/stages/Stage-4B-Checkpointing-Durable-Execution-and-Human-Approval.md').read_text()
checks=['GRAPH-001','AGT-001','TOOL-006','DATA-007','DATA-058','INT-036','ADR-030','TEST-134','EVAL-033','preliminary_grounded_human_approved']
missing=[x for x in checks if x not in chapter]
assert not missing, missing
assert not (root/'src/northstar_compliance/memory').exists()
assert not (root/'src/northstar_compliance/harness').exists()
assert not (root/'src/northstar_compliance/agents').exists()
print('stage4b consistency audit passed with recorded reconstruction and production exceptions')
