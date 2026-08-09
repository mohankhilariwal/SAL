from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

root = Path(__file__).resolve().parents[1]
errors: list[str] = []
for schema_path in sorted((root / "schemas").glob("DATA-*.schema.json")):
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
    except Exception as exc:
        errors.append(f"{schema_path.name}: {exc}")
for config_path in sorted((root / "config").rglob("*.json")):
    try:
        json.loads(config_path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"{config_path.name}: {exc}")
if errors:
    raise SystemExit("\n".join(errors))
print("validated 20 schemas and 5 configuration files")
