from dataclasses import asdict,is_dataclass
import json
def to_json(v):
    if is_dataclass(v): v=asdict(v)
    return json.dumps(v,indent=2,sort_keys=True)
