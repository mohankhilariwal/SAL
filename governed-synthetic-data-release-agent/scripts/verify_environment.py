from __future__ import annotations

import importlib
import json
import platform
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

REQUIRED = ["pydantic", "fastapi", "sqlalchemy", "alembic", "pandas", "sklearn", "httpx"]
OPTIONAL = ["streamlit", "sdv", "sdmetrics", "presidio_analyzer"]


def version(name: str) -> str | None:
    try:
        module = importlib.import_module(name)
    except ImportError:
        return None
    return str(getattr(module, "__version__", "installed"))


def main() -> None:
    payload = {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "required": {name: version(name) for name in REQUIRED},
        "optional": {name: version(name) for name in OPTIONAL},
        "opa_binary": shutil.which("opa"),
        "ollama_binary": shutil.which("ollama"),
        "host_binding_default": "127.0.0.1",
    }
    print(json.dumps(payload, indent=2))
    missing = [name for name, value in payload["required"].items() if value is None]
    if sys.version_info < (3, 12) or sys.version_info >= (3, 14):
        raise SystemExit("Python 3.12 or 3.13 is required")
    if missing:
        raise SystemExit("Missing required dependencies: " + ", ".join(missing))
    print("Environment verification passed.")


if __name__ == "__main__":
    main()
