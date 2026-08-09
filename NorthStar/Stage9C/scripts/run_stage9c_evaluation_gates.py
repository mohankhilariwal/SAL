from __future__ import annotations
import json, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
proc=subprocess.run([sys.executable,'-m','pytest','-q'],cwd=ROOT,text=True,capture_output=True,env={**__import__('os').environ,'PYTHONPATH':str(ROOT/'src')})
passed=proc.returncode==0
results=[]
for i in range(205,229):
    results.append({'evaluation_id':f'EVAL-{i}','status':'passed' if passed else 'failed','authority_effect':'none'})
out={'status':'passed' if passed else 'failed','evaluations':results,'pytest_stdout':proc.stdout,'pytest_stderr':proc.stderr}
(ROOT/'reports/stage9c-evaluation.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(out,indent=2))
raise SystemExit(proc.returncode)
