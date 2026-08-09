from __future__ import annotations

import json
from pathlib import Path
from jsonschema import Draft202012Validator
from _bootstrap import ROOT


def main() -> None:
    schemas = sorted((ROOT / "schemas").glob("DATA-*.schema.json"))
    configs = sorted((ROOT / "config").rglob("*.json"))
    for path in schemas:
        schema = json.loads(path.read_text())
        Draft202012Validator.check_schema(schema)
        assert schema["properties"]["authority_effect"]["const"] == "none"
    for path in configs:
        json.loads(path.read_text())
    assert len(schemas) == 22
    assert len(configs) == 7
    print(f"validated {len(schemas)} schemas and {len(configs)} configuration files")

if __name__ == "__main__":
    main()
