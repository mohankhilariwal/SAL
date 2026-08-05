from __future__ import annotations

import signal
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    subprocess.run([sys.executable, str(ROOT / "scripts" / "bootstrap.py")], check=True, cwd=ROOT)
    api = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "governed_release.api.app:app",
            "--host",
            "127.0.0.1",
            "--port",
            "8000",
        ],
        cwd=ROOT,
    )
    ui = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            "src/governed_release/ui/app.py",
            "--server.address",
            "127.0.0.1",
            "--server.port",
            "8501",
        ],
        cwd=ROOT,
    )
    processes = [api, ui]

    def stop(*_: object) -> None:
        for process in processes:
            if process.poll() is None:
                process.terminate()
        for process in processes:
            try:
                process.wait(timeout=8)
            except subprocess.TimeoutExpired:
                process.kill()
        raise SystemExit(0)

    signal.signal(signal.SIGINT, stop)
    signal.signal(signal.SIGTERM, stop)
    print("API: http://127.0.0.1:8000")
    print("OpenAPI: http://127.0.0.1:8000/docs")
    print("Streamlit UI: http://127.0.0.1:8501")
    print("Press Ctrl+C to stop both processes cleanly.")
    try:
        while all(process.poll() is None for process in processes):
            time.sleep(1)
    finally:
        stop()


if __name__ == "__main__":
    main()
