from __future__ import annotations

from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import json,re

required=[f"docs/source-of-truth/{i:02d}-{name}.md" for i,name in enumerate([
    "Project-Constitution","Business-and-User-Story-Baseline","Requirements-Register","Architecture-Baseline",
    "Component-and-Agent-Catalogue","Data-and-Schema-Register","ADR-Register","Repository-Manifest",
    "Risk-Assumption-and-Issue-Register","Stage-Handoff-Pack"
])]
errors=[]
required_diagrams=[
    "cumulative-logical-architecture.mmd",
    "stage-2b-architecture-before.mmd",
    "stage-2b-architecture-after.mmd",
    "stage-2b-ranking-pipeline.mmd",
    "stage-2b-retrieval-sequence.mmd",
    "stage-2b-trust-boundary.mmd",
    "stage-2b-evaluation-architecture.mmd",
]
for name in required_diagrams:
    path=ROOT/"docs/architecture/diagrams"/name
    if not path.exists():
        errors.append(f"missing diagram {name}")
        continue
    first=next((line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()),"")
    if not (first.startswith("flowchart") or first.startswith("sequenceDiagram")):
        errors.append(f"unsupported Mermaid declaration in {name}: {first}")
for rel in required:
    if not (ROOT/rel).exists(): errors.append(f"missing {rel}")
text="\n".join(p.read_text(encoding="utf-8") for p in (ROOT/"docs").rglob("*.md"))
for cid,name in {
    "CMP-001":"Analyst Experience Portal","CMP-002":"Regulatory Intake Boundary","CMP-003":"Case and Workflow Orchestration Boundary",
    "CMP-004":"Knowledge and Evidence Access Boundary","CMP-005":"Enterprise Integration Boundary","CMP-006":"Human Review and Approval Boundary",
    "CMP-007":"Identity, Authorization and Policy Boundary","CMP-008":"Evaluation and Assurance Boundary",
    "CMP-009":"Observability and Audit Boundary","CMP-010":"Runtime and Deployment Boundary","CMP-011":"Source-of-Truth Governance Pack",
}.items():
    if cid not in text or name not in text: errors.append(f"component missing or renamed: {cid}")
if re.search(r"AGT-\d+",text): errors.append("agent identifier allocated in S02B")
if re.search(r"TOOL-\d+",text): errors.append("tool identifier allocated in S02B")
for token in ["DATA-026","DATA-033","INT-012","INT-015","ADR-014","ADR-017","TEST-046","EVAL-013"]:
    if token not in text: errors.append(f"new identifier not documented: {token}")
report={"result":"PASSED" if not errors else "FAILED","errors":errors,"exceptions":["ISS-014 Mermaid CLI rendering not executed","ISS-015 Python 3.12 direct execution not available","ISS-016 production semantic/reranking providers not live-benchmarked","ISS-018 enterprise identity/PDP not connected","ISS-019 nine detailed prior registers/repository not attached","ISS-020 answer-generation metrics intentionally unavailable"]}
(ROOT/"reports/consistency-audit.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
print(json.dumps(report,indent=2))
if errors: raise SystemExit(1)
