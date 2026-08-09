from pathlib import Path
from northstar_compliance.security.threat_model.io import load_json
from northstar_compliance.security.threat_model.engine import ThreatModelEngine
ROOT=Path(__file__).resolve().parents[1]

def make_engine():
    return ThreatModelEngine(load_json(ROOT/'config/threat_model/architecture_snapshot.json'),load_json(ROOT/'config/threat_model/threat_catalogue.json'),load_json(ROOT/'config/threat_model/risk_policy.json'),load_json(ROOT/'config/threat_model/actors.json'),load_json(ROOT/'config/threat_model/attack_trees.json'),load_json(ROOT/'config/threat_model/misuse_cases.json'))
