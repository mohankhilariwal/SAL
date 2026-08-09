from pathlib import Path
from northstar_compliance.evaluation.datasets import build_manifest, contamination_report, load_jsonl
from northstar_compliance.evaluation.io import write_json

ROOT = Path(__file__).resolve().parents[1]
paths = [ROOT / "datasets" / "evaluation" / "v1.0.0" / f"{s}.jsonl" for s in ("dev", "validation", "test")]
cases = [c for p in paths for c in load_jsonl(p)]
write_json(ROOT / "datasets" / "evaluation" / "v1.0.0" / "manifest.json", build_manifest(cases, paths))
write_json(ROOT / "reports" / "stage8a-contamination.json", contamination_report(cases))
print("dataset manifest and contamination report written")
