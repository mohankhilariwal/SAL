from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from governed_release.adapters.local_files.source_data import generate_maplebridge_source


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rows", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=20260804)
    args = parser.parse_args()
    path = ROOT / "data" / "source" / "maplebridge_transactions.csv"
    frame = generate_maplebridge_source(path, rows=args.rows, seed=args.seed)
    print(f"Wrote {len(frame)} fictional rows to {path}")
    print(f"Fraud rate: {frame['is_fraud'].mean():.4f}")


if __name__ == "__main__":
    main()
