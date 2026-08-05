from __future__ import annotations

import random
from typing import Any

import numpy as np
import pandas as pd


class FallbackStatisticalGenerator:
    name = "deterministic-statistical-fallback"

    def generate(
        self, source: pd.DataFrame, rows: int, seed: int, *, unsafe_mode: bool = False
    ) -> pd.DataFrame:
        rng = np.random.default_rng(seed)
        result: dict[str, Any] = {}
        fraud_source = (
            source["is_fraud"].astype(int)
            if "is_fraud" in source
            else pd.Series(np.zeros(len(source), dtype=int))
        )
        fraud_rate = float(fraud_source.mean())
        result["is_fraud"] = rng.binomial(1, fraud_rate, rows)
        for column in source.columns:
            if column == "is_fraud":
                continue
            series = source[column]
            if pd.api.types.is_datetime64_any_dtype(series):
                values = series.astype("int64").to_numpy()
                sampled = rng.choice(values, rows)
                jitter = rng.normal(0, 12 * 3600 * 1e9, rows)
                result[column] = pd.to_datetime(sampled + jitter.astype("int64"), utc=True)
            elif pd.api.types.is_numeric_dtype(series):
                fraud = np.asarray(result["is_fraud"])
                nonfraud_values = series[fraud_source == 0].to_numpy(dtype=float)
                fraud_values = series[fraud_source == 1].to_numpy(dtype=float)
                base = np.empty(rows, dtype=float)
                for label, values in ((0, nonfraud_values), (1, fraud_values)):
                    mask = fraud == label
                    pool = values if len(values) else series.to_numpy(dtype=float)
                    base[mask] = rng.choice(pool, int(mask.sum()))
                scale = max(float(series.std(ddof=0)), 1.0) * 0.10
                generated = base + rng.normal(0, scale, rows)
                generated = np.clip(generated, float(series.min()), float(series.max()))
                result[column] = generated
            else:
                values = series.dropna().astype(str).to_numpy()
                result[column] = rng.choice(values, rows)
        frame = pd.DataFrame(result)[list(source.columns)]
        return _postprocess(frame, source, seed, unsafe_mode)


class SDVGaussianCopulaGenerator:
    name = "sdv-gaussian-copula"

    def generate(
        self, source: pd.DataFrame, rows: int, seed: int, *, unsafe_mode: bool = False
    ) -> pd.DataFrame:
        try:
            from sdv.metadata import Metadata
            from sdv.single_table import GaussianCopulaSynthesizer
        except ImportError as exc:
            raise RuntimeError(
                "SDV is not installed. Run `make setup` or use the fallback generator."
            ) from exc
        np.random.seed(seed)
        random.seed(seed)
        metadata = Metadata.detect_from_dataframe(source)
        try:
            metadata.update_column(column_name="is_fraud", sdtype="categorical")
        except Exception as metadata_error:
            # Older/future SDV metadata detectors may already infer this correctly.
            del metadata_error
        synthesizer = GaussianCopulaSynthesizer(
            metadata,
            enforce_min_max_values=True,
            enforce_rounding=True,
            default_distribution="beta",
        )
        synthesizer.fit(source)
        frame = synthesizer.sample(num_rows=rows)
        return _postprocess(frame, source, seed, unsafe_mode)


def _postprocess(
    frame: pd.DataFrame, source: pd.DataFrame, seed: int, unsafe_mode: bool
) -> pd.DataFrame:
    rng = np.random.default_rng(seed + 31)
    frame = frame.copy()
    for column in source.columns:
        if column not in frame:
            continue
        if pd.api.types.is_datetime64_any_dtype(source[column]):
            frame[column] = pd.to_datetime(frame[column], utc=True, errors="coerce")
            frame[column] = frame[column].fillna(source[column].median())
        elif pd.api.types.is_integer_dtype(source[column]):
            frame[column] = (
                pd.to_numeric(frame[column], errors="coerce")
                .fillna(source[column].median())
                .round()
                .astype(int)
            )
            frame[column] = frame[column].clip(int(source[column].min()), int(source[column].max()))
        elif pd.api.types.is_numeric_dtype(source[column]):
            frame[column] = pd.to_numeric(frame[column], errors="coerce").fillna(
                source[column].median()
            )
            frame[column] = (
                frame[column]
                .clip(float(source[column].min()), float(source[column].max()))
                .round(2)
            )
        else:
            frame[column] = frame[column].astype(str)
    if "is_fraud" in frame:
        frame["is_fraud"] = (
            pd.to_numeric(frame["is_fraud"], errors="coerce")
            .fillna(0)
            .round()
            .clip(0, 1)
            .astype(int)
        )
        if frame["is_fraud"].nunique() < 2 and source["is_fraud"].nunique() == 2:
            count = max(1, int(len(frame) * float(source["is_fraud"].mean())))
            frame.loc[frame.index[:count], "is_fraud"] = 1
    if unsafe_mode:
        n = len(frame)
        exact_n = max(1, int(n * 0.10))
        near_n = max(1, int(n * 0.10))
        rare_n = max(1, int(n * 0.12))
        exact = (
            source.sample(exact_n, replace=True, random_state=seed).reset_index(drop=True).copy()
        )
        near = (
            source.sample(near_n, replace=True, random_state=seed + 1).reset_index(drop=True).copy()
        )
        for col in near.select_dtypes(include=["floating"]).columns:
            near[col] = (near[col].astype(float) * (1 + rng.normal(0, 0.0001, near_n))).round(2)
        if "transaction_timestamp" in near:
            near["transaction_timestamp"] = pd.to_datetime(
                near["transaction_timestamp"], utc=True
            ) + pd.to_timedelta(rng.integers(1, 30, near_n), unit="s")
        injected = [exact, near]
        if {"city", "merchant_category"}.issubset(source.columns):
            counts = source.groupby(["city", "merchant_category"]).size()
            rare_keys = set(counts[counts <= 12].index)
            rare_source = source[
                source.apply(lambda r: (r["city"], r["merchant_category"]) in rare_keys, axis=1)
            ]
            if not rare_source.empty:
                injected.append(
                    rare_source.sample(rare_n, replace=True, random_state=seed + 2)
                    .reset_index(drop=True)
                    .copy()
                )
        injected_rows = sum(len(part) for part in injected)
        remainder = frame.iloc[injected_rows:].copy()
        frame = pd.concat([*injected, remainder], ignore_index=True).iloc[:n]
        frame = frame[list(source.columns)]
    return frame.reset_index(drop=True)


def build_generator(mode: str) -> FallbackStatisticalGenerator | SDVGaussianCopulaGenerator:
    if mode == "fallback":
        return FallbackStatisticalGenerator()
    if mode == "sdv":
        return SDVGaussianCopulaGenerator()
    try:
        import sdv  # noqa: F401
    except ImportError:
        return FallbackStatisticalGenerator()
    return SDVGaussianCopulaGenerator()
