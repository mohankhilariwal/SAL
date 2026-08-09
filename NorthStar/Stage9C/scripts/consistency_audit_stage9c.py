from __future__ import annotations
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
checks={}
checks['stage_doc_exists']=(ROOT/'docs/stages/NorthStar-Stage-9C-Guardrails-Governance-and-Control-Plane.md').exists()
checks['ten_source_files']=len(list((ROOT/'docs/source-of-truth').glob('*.md')))==10
checks['schemas_193_216']=all((ROOT/f'schemas/DATA-{n}.schema.json').exists() for n in range(193,217))
checks['adr_104_113']=all(any((ROOT/'docs/adr').glob(f'ADR-{n}-*.md')) for n in range(104,114))
text='\n'.join(p.read_text(encoding='utf-8') for p in (ROOT/'docs/source-of-truth').glob('*.md'))
checks['one_active_agent']='only active agent' in text.lower() and 'AGT-001' in text
checks['stage8d_unresolved']='Stage 8D remains unresolved' in text
checks['no_new_tool_definition']='TOOL-007' not in (ROOT/'config/guardrails/guardrail_policy_bundle.json').read_text()
checks['auth_br_preserved']='AUTH-001/1.0.0' in text and 'BR-001/1.0.0' in text
checks['data106_boundary']='DATA-106' in text and 'cannot mutate' in text
checks['full_control_plane_not_claimed']='full production control plane is not implemented' in text.lower()
status='passed_with_recorded_exceptions' if all(checks.values()) else 'failed'
out={'status':status,'checks':checks,'exceptions':['ISS-096','ISS-131','ISS-141','ISS-147','ISS-158','ISS-159','ISS-160','ISS-161','ISS-162','ISS-163','ISS-164','ISS-165','ISS-166','ISS-167','ISS-168','ISS-169']}
(ROOT/'reports/stage9c-consistency-audit.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(out,indent=2))
raise SystemExit(0 if status!='failed' else 1)
