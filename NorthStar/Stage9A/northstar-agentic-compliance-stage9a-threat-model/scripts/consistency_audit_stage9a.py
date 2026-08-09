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
    e = engine(); report=e.report(); ev=e.evaluate()
    assertions = {
        'one_active_agent': e.snapshot['active_agents'] == ['AGT-001'],
        'wp008_inactive': 'WP-008' in e.snapshot['inactive_future'],
        'authority_effect_none': report['authority_effect'] == 'none' and ev['authority_effect'] == 'none',
        'no_route_activation': 'no_model_provider_or_route_activated' in e.snapshot['invariants'],
        'tool_gateway_preserved': 'CMP-005_only_tool_gateway' in e.snapshot['invariants'],
        'authority_issuer_preserved': 'CMP-007_only_authority_issuer' in e.snapshot['invariants'],
        'critical_non_overridable': 'critical_deterministic_and_bias_failures_non_overridable' in e.snapshot['invariants'],
        'threat_count': report['counts']['threats'] == 36,
        'evaluations': len(ev['passed']) == 16 and not ev['failed'],
    }
    failed = [k for k,v in assertions.items() if not v]
    out = {'result':'passed_with_recorded_exceptions' if not failed else 'failed','assertions':assertions,'failed':failed,'exceptions':['ISS-096','ISS-131','ISS-140','ISS-141','ISS-142','ISS-143','ISS-144','ISS-145','ISS-146']}
    write_json(ROOT/'reports/stage9a-consistency-audit.json', out)
    if failed: raise SystemExit(1)
    print('STAGE 9A CONSISTENCY AUDIT PASSED WITH RECORDED EXCEPTIONS')
