from __future__ import annotations

from datetime import UTC, datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd


def generate_maplebridge_source(path: Path, rows: int = 2000, seed: int = 20260804) -> pd.DataFrame:
    """Generate entirely fictional payment data with reproducible fraud signal."""
    rng = np.random.default_rng(seed)
    cities = np.array(
        [
            "Toronto",
            "Ottawa",
            "Mississauga",
            "Brampton",
            "Vancouver",
            "Calgary",
            "Montreal",
            "Halifax",
            "Winnipeg",
            "Yellowknife",
        ]
    )
    provinces = {
        "Toronto": "ON",
        "Ottawa": "ON",
        "Mississauga": "ON",
        "Brampton": "ON",
        "Vancouver": "BC",
        "Calgary": "AB",
        "Montreal": "QC",
        "Halifax": "NS",
        "Winnipeg": "MB",
        "Yellowknife": "NT",
    }
    city_probs = np.array([0.27, 0.09, 0.11, 0.08, 0.12, 0.10, 0.11, 0.05, 0.06, 0.01])
    categories = np.array(
        ["grocery", "fuel", "restaurant", "retail", "travel", "electronics", "gaming", "jewellery"]
    )
    category_probs = np.array([0.25, 0.14, 0.19, 0.18, 0.08, 0.08, 0.06, 0.02])

    city = rng.choice(cities, rows, p=city_probs)
    merchant_category = rng.choice(categories, rows, p=category_probs)
    tenure = np.clip(rng.gamma(3.2, 16.0, rows).round(), 1, 180).astype(int)
    tx_24h = np.clip(rng.poisson(3.5, rows) + 1, 1, 40).astype(int)
    avg_30d = np.clip(rng.lognormal(4.0, 0.7, rows), 8, 1200)
    amount_multiplier = np.where(
        np.isin(merchant_category, ["travel", "electronics", "jewellery"]), 2.2, 1.0
    )
    amount = np.clip(rng.lognormal(3.8, 0.9, rows) * amount_multiplier, 1.5, 5000)

    rare_combo = ((city == "Yellowknife") & np.isin(merchant_category, ["jewellery", "gaming"])) | (
        (city == "Halifax") & (merchant_category == "jewellery")
    )
    unusual = (amount > 1500) & (tenure < 6) & (tx_24h > 8)
    logit = (
        -4.65
        + 0.75 * (amount > 600)
        + 0.9 * (amount > 1500)
        + 0.7 * (tx_24h > 8)
        + 0.8 * (tenure < 6)
        + 1.2 * rare_combo
        + 1.1 * unusual
    )
    fraud_probability = 1.0 / (1.0 + np.exp(-logit))
    is_fraud = rng.binomial(1, fraud_probability).astype(int)

    now = datetime(2026, 8, 1, 12, 0, tzinfo=UTC)
    minutes_ago = rng.integers(0, 60 * 24 * 90, rows)
    timestamps = [now - timedelta(minutes=int(v)) for v in minutes_ago]

    data = pd.DataFrame(
        {
            "transaction_id": [f"TXN-{seed}-{i:07d}" for i in range(rows)],
            "customer_id": [f"CUST-{rng.integers(100000, 999999)}" for _ in range(rows)],
            "account_number": [f"{rng.integers(100000000000, 999999999999)}" for _ in range(rows)],
            "transaction_amount": amount.round(2),
            "merchant_category": merchant_category,
            "city": city,
            "province": [provinces[str(c)] for c in city],
            "transaction_timestamp": pd.to_datetime(timestamps, utc=True),
            "is_fraud": is_fraud,
            "account_tenure_months": tenure,
            "transactions_last_24h": tx_24h,
            "average_transaction_amount_30d": avg_30d.round(2),
        }
    )

    # Guarantee a small, auditable set of unusual and rare profiles.
    special = min(12, rows)
    data.loc[: special - 1, "city"] = "Yellowknife"
    data.loc[: special - 1, "province"] = "NT"
    data.loc[: special - 1, "merchant_category"] = "jewellery"
    data.loc[: special - 1, "transaction_amount"] = np.linspace(1800, 4200, special).round(2)
    data.loc[: special - 1, "account_tenure_months"] = 2
    data.loc[: special - 1, "transactions_last_24h"] = 15
    data.loc[: special - 1, "is_fraud"] = 1

    path.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(path, index=False)
    return data


def load_source(path: Path) -> pd.DataFrame:
    data = pd.read_csv(path)
    data["transaction_timestamp"] = pd.to_datetime(data["transaction_timestamp"], utc=True)
    data["account_number"] = data["account_number"].astype(str)
    return data
