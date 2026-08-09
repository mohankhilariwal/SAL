from __future__ import annotations

import os
import sys

mode = sys.argv[1] if len(sys.argv) > 1 else "readiness"
if mode not in {"startup", "readiness", "liveness"}:
    raise SystemExit(2)
# Reference-only checks. Readiness remains false if someone attempts to enable a
# production route in this Stage 10B overlay.
if mode == "readiness" and os.getenv("NORTHSTAR_ENV") == "production":
    raise SystemExit(1)
raise SystemExit(0)
