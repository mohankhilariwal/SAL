from __future__ import annotations
import json
from pathlib import Path
from importlib.metadata import version
from jsonschema import Draft202012Validator
from northstar_compliance.guardrails.policy import PolicyBundle

ROOT=Path(__file__).resolve().parents[1]
errors=[]
try:
    bundle=PolicyBundle.load(ROOT/'config/guardrails/guardrail_policy_bundle.json')
    if len(bundle.controls)!=59: errors.append('expected 59 controls')
except Exception as exc: errors.append(f'policy bundle: {exc}')
for n in range(193,217):
    p=ROOT/f'schemas/DATA-{n}.schema.json'
    try:
        schema=json.loads(p.read_text())
        Draft202012Validator.check_schema(schema)
    except Exception as exc: errors.append(f'{p.name}: {exc}')
for path in [ROOT/'config/guardrails/exception_policy.json',ROOT/'config/guardrails/control_plane_profile.json',ROOT/'config/guardrails/control_owners.json']:
    try: json.loads(path.read_text())
    except Exception as exc: errors.append(f'{path.name}: {exc}')
result={'status':'passed' if not errors else 'failed','errors':errors,'jsonschema_version':version('jsonschema'),'schemas_validated':24,'controls_validated':59}
(ROOT/'reports/stage9c-validation.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
raise SystemExit(0 if not errors else 1)
