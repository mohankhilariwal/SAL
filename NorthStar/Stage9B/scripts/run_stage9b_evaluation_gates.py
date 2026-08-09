from __future__ import annotations
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/"src"))
import json, subprocess, sys
checks=[]
proc=subprocess.run([sys.executable,"-m","pytest","-q"],capture_output=True,text=True)
checks.append({"id":"EVAL-185-204","name":"stage9b_test_suite","passed":proc.returncode==0,"stdout":proc.stdout[-4000:],"stderr":proc.stderr[-2000:]})
result={"stage":"S09B","passed":all(c["passed"] for c in checks),"checks":checks,"authority_effect":"none"}
p=Path("reports/stage9b-evaluation.json")
p.parent.mkdir(exist_ok=True)
p.write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2))
raise SystemExit(0 if result["passed"] else 1)
