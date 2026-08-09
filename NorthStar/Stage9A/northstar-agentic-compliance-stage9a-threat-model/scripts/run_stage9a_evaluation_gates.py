from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from northstar_compliance.security.threat_model.io import load_json, write_json
from northstar_compliance.security.threat_model.engine import ThreatModelEngine

def engine():
    return ThreatModelEngine(
        load_json(ROOT/'config/threat_model/architecture_snapshot.json'),
        load_json(ROOT/'config/threat_model/threat_catalogue.json'),
        load_json(ROOT/'config/threat_model/risk_policy.json'),
        load_json(ROOT/'config/threat_model/actors.json'),
        load_json(ROOT/'config/threat_model/attack_trees.json'),
        load_json(ROOT/'config/threat_model/misuse_cases.json'),
    )

if __name__ == '__main__':
    result = engine().evaluate()
    write_json(ROOT/'reports/stage9a-evaluation-gates.json', result)
    print(f"EVALUATION GATES: {len(result['passed'])}/{len(result['passed']) + len(result['failed'])} passed")
