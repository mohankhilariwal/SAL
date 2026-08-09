import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def test_270_evaluation_ids_and_one_agent_gate():
 c=json.loads((ROOT/'config/evaluation/stage6a-evaluations.json').read_text());assert c['evaluation_ids']==[f'EVAL-{i:03d}' for i in range(55,62)] and c['required_agent_count']==1
def test_stage6a_config_has_no_future_markers():
 t=(ROOT/'config/agents/AGT-001-task-profiles.json').read_text().lower()
 for m in ('agt-002','"can_delegate": true','"can_handoff": true','"concurrent_execution": true'):assert m not in t
