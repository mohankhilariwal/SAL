from __future__ import annotations

import json
import re
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    errors: list[str] = []
    schemas = sorted((ROOT / "schemas").glob("DATA-*.schema.json"))
    if len(schemas) != 20:
        errors.append(f"expected 20 Stage 10A schemas, found {len(schemas)}")
    for path in schemas:
        schema = json.loads(path.read_text(encoding="utf-8"))
        try:
            Draft202012Validator.check_schema(schema)
        except Exception as exc:  # noqa: BLE001
            errors.append(f"invalid schema {path.name}: {exc}")
        if "authority_effect" not in schema.get("required", []):
            errors.append(f"{path.name} does not require authority_effect")

    for config_name, schema_name in [
        (ROOT / "config/observability/telemetry-policy.json", "DATA-234.schema.json"),
        (ROOT / "config/audit/audit-policy.json", "DATA-235.schema.json"),
    ]:
        instance = json.loads(config_name.read_text(encoding="utf-8"))
        schema = json.loads((ROOT / "schemas" / schema_name).read_text(encoding="utf-8"))
        for error in Draft202012Validator(schema).iter_errors(instance):
            errors.append(f"{config_name.name}: {error.message}")

    source = "\n".join(path.read_text(encoding="utf-8") for path in (ROOT / "src").rglob("*.py"))
    if "AGT-002" in source or "TOOL-007" in source:
        errors.append("new active agent or tool identifier found in source")
    if re.search(r"production_ready[\"']?\s*[:=]\s*True", source):
        errors.append("source falsely claims production readiness")
    if "authority_effect\": \"none\"" not in source and "authority_effect: str = \"none\"" not in source:
        errors.append("non-authorizing evidence invariant missing")

    result = {
        "valid": not errors,
        "schemas_checked": len(schemas),
        "configs_checked": 2,
        "errors": errors,
        "python_target": "3.12-3.13",
        "architecture_version": "1.15.0",
    }
    (ROOT / "reports/stage10a-validation.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
