from __future__ import annotations

import hashlib
import json
from typing import Any

import numpy as np
import pandas as pd
from scipy.stats import ks_2samp
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, f1_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import NearestNeighbors
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from governed_release.config.settings import Settings
from governed_release.domain.models import PrivacyReport, UtilityReport


def _hash(payload: dict[str, Any]) -> str:
    return hashlib.sha256(json.dumps(payload, sort_keys=True, default=str).encode()).hexdigest()


def _prepare(frame: pd.DataFrame) -> pd.DataFrame:
    data = frame.copy()
    for column in data.columns:
        if pd.api.types.is_datetime64_any_dtype(data[column]) or "timestamp" in column:
            parsed = pd.to_datetime(data[column], utc=True, errors="coerce")
            data[column] = parsed.astype("int64") / 1e9
    return data


def evaluate_utility(
    source: pd.DataFrame, synthetic: pd.DataFrame, settings: Settings, seed: int
) -> UtilityReport:
    common = [c for c in source.columns if c in synthetic.columns]
    source = _prepare(source[common])
    synthetic = _prepare(synthetic[common])
    distribution_scores: list[float] = []
    for column in common:
        real = source[column].dropna()
        synth = synthetic[column].dropna()
        if pd.api.types.is_numeric_dtype(real):
            if real.nunique() <= 2:
                distribution_scores.append(1.0 - abs(float(real.mean()) - float(synth.mean())))
            else:
                distribution_scores.append(max(0.0, 1.0 - float(ks_2samp(real, synth).statistic)))
        else:
            rp = real.astype(str).value_counts(normalize=True)
            sp = synth.astype(str).value_counts(normalize=True)
            idx = rp.index.union(sp.index)
            tvd = 0.5 * float(
                (rp.reindex(idx, fill_value=0) - sp.reindex(idx, fill_value=0)).abs().sum()
            )
            distribution_scores.append(max(0.0, 1.0 - tvd))
    distribution_similarity = float(np.mean(distribution_scores))

    numeric = [
        c for c in common if pd.api.types.is_numeric_dtype(source[c]) and source[c].nunique() > 1
    ]
    if len(numeric) >= 2:
        real_corr = source[numeric].corr().fillna(0).to_numpy()
        synth_corr = synthetic[numeric].corr().fillna(0).to_numpy()
        relationship_similarity = max(
            0.0, 1.0 - float(np.mean(np.abs(real_corr - synth_corr))) / 2.0
        )
    else:
        relationship_similarity = 1.0

    target = "is_fraud"
    features = [c for c in common if c != target]
    x_train, x_test, y_train, y_test = train_test_split(
        source[features],
        source[target].astype(int),
        test_size=0.30,
        random_state=seed,
        stratify=source[target].astype(int),
    )
    synth_x = synthetic[features]
    synth_y = synthetic[target].astype(int)
    categorical = [c for c in features if not pd.api.types.is_numeric_dtype(source[c])]
    numerical = [c for c in features if c not in categorical]
    preprocessor = ColumnTransformer(
        [
            (
                "num",
                Pipeline(
                    [("impute", SimpleImputer(strategy="median")), ("scale", StandardScaler())]
                ),
                numerical,
            ),
            (
                "cat",
                Pipeline(
                    [
                        ("impute", SimpleImputer(strategy="most_frequent")),
                        ("encode", OneHotEncoder(handle_unknown="ignore")),
                    ]
                ),
                categorical,
            ),
        ]
    )
    classifier = Pipeline(
        [
            ("preprocess", preprocessor),
            ("model", LogisticRegression(max_iter=500, class_weight="balanced", random_state=seed)),
        ]
    )
    if synth_y.nunique() < 2:
        synth_y.iloc[:1] = 1 - int(synth_y.iloc[0])
    classifier.fit(synth_x, synth_y)
    probabilities = classifier.predict_proba(x_test)[:, 1]
    predictions = (probabilities >= 0.5).astype(int)
    roc_auc = float(roc_auc_score(y_test, probabilities))
    pr_auc = float(average_precision_score(y_test, probabilities))
    f1 = float(f1_score(y_test, predictions, zero_division=0))
    recall = float(recall_score(y_test, predictions, zero_division=0))
    fraud_score = float(
        np.clip((roc_auc + min(1.0, pr_auc / max(float(y_test.mean()), 0.01))) / 2.0, 0, 1)
    )
    normalized = float(np.mean([distribution_similarity, relationship_similarity, fraud_score]))
    payload = {
        "distribution_similarity": distribution_similarity,
        "relationship_similarity": relationship_similarity,
        "roc_auc": roc_auc,
        "pr_auc": pr_auc,
        "f1": f1,
        "recall": recall,
        "normalized": normalized,
        "seed": seed,
    }
    return UtilityReport(
        distribution_similarity=round(distribution_similarity, 6),
        relationship_similarity=round(relationship_similarity, 6),
        fraud_roc_auc=round(roc_auc, 6),
        fraud_pr_auc=round(pr_auc, 6),
        fraud_f1=round(f1, 6),
        fraud_recall=round(recall, 6),
        normalized_utility_score=round(normalized, 6),
        threshold=settings.utility_score_min,
        passed=normalized >= settings.utility_score_min,
        seed=seed,
        limitations=[
            "Toy fictional dataset; metrics do not establish production model fitness.",
            "Utility does not imply privacy.",
        ],
        evidence_hash=_hash(payload),
    )


def _normalized_rows(frame: pd.DataFrame) -> pd.Series:
    normalized = frame.copy()
    for col in normalized.columns:
        if pd.api.types.is_datetime64_any_dtype(normalized[col]) or "timestamp" in col:
            normalized[col] = (
                pd.to_datetime(normalized[col], utc=True, errors="coerce")
                .dt.round("min")
                .astype(str)
            )
        elif pd.api.types.is_numeric_dtype(normalized[col]):
            normalized[col] = pd.to_numeric(normalized[col], errors="coerce").round(2).astype(str)
        else:
            normalized[col] = normalized[col].astype(str).str.strip().str.lower()
    return normalized.astype(str).agg("|".join, axis=1)


def evaluate_privacy(
    source: pd.DataFrame, synthetic: pd.DataFrame, settings: Settings, seed: int
) -> PrivacyReport:
    common = [c for c in source.columns if c in synthetic.columns]
    source = source[common].copy()
    synthetic = synthetic[common].copy()
    source_rows = set(_normalized_rows(source))
    synthetic_rows = _normalized_rows(synthetic)
    exact_matches = int(synthetic_rows.isin(source_rows).sum())
    exact_rate = exact_matches / max(len(synthetic), 1)

    sample_n = min(1200, len(source), len(synthetic))
    real_sample = _prepare(source.sample(sample_n, random_state=seed)).reset_index(drop=True)
    synth_sample = _prepare(synthetic.sample(sample_n, random_state=seed + 1)).reset_index(
        drop=True
    )
    categorical = [c for c in common if not pd.api.types.is_numeric_dtype(real_sample[c])]
    numerical = [c for c in common if c not in categorical]
    transformer = ColumnTransformer(
        [
            (
                "num",
                Pipeline(
                    [("impute", SimpleImputer(strategy="median")), ("scale", StandardScaler())]
                ),
                numerical,
            ),
            (
                "cat",
                Pipeline(
                    [
                        ("impute", SimpleImputer(strategy="most_frequent")),
                        ("encode", OneHotEncoder(handle_unknown="ignore")),
                    ]
                ),
                categorical,
            ),
        ]
    )
    combined = pd.concat([real_sample, synth_sample], ignore_index=True)
    matrix = transformer.fit_transform(combined)
    real_matrix = matrix[:sample_n]
    synth_matrix = matrix[sample_n:]
    neighbours = NearestNeighbors(n_neighbors=1, metric="euclidean").fit(real_matrix)
    distances, _ = neighbours.kneighbors(synth_matrix)
    similarities = 1.0 / (1.0 + distances[:, 0])
    mean_similarity = float(np.mean(similarities))
    near_count_sample = int((similarities >= 0.995).sum())
    near_rate = near_count_sample / max(sample_n, 1)
    near_count = int(round(near_rate * len(synthetic)))

    rare_exposure = 0.0
    if {"city", "merchant_category"}.issubset(common):
        source_counts = source.groupby(["city", "merchant_category"]).size()
        rare_keys = set(source_counts[source_counts <= 12].index)
        if rare_keys:
            candidate_pairs = list(
                zip(synthetic["city"], synthetic["merchant_category"], strict=False)
            )
            rare_exposure = sum(pair in rare_keys for pair in candidate_pairs) / max(
                len(candidate_pairs), 1
            )
    quasi_risk = float(np.clip((mean_similarity + rare_exposure + exact_rate) / 3.0, 0, 1))
    gates = {
        "exact_match": exact_rate <= settings.privacy_exact_match_max,
        "mean_similarity": mean_similarity <= settings.privacy_mean_similarity_max,
        "near_duplicate_rate": near_rate <= settings.privacy_near_duplicate_rate_max,
        "rare_combination_exposure": rare_exposure <= settings.privacy_rare_exposure_max,
    }
    passed = all(gates.values())
    risk_category = "LOW" if passed and quasi_risk < 0.35 else "MEDIUM" if passed else "HIGH"
    payload = {
        "exact_match_rate": exact_rate,
        "mean_source_similarity": mean_similarity,
        "near_duplicate_rate": near_rate,
        "rare_combination_exposure": rare_exposure,
        "quasi_identifier_risk": quasi_risk,
        "gates": gates,
    }
    return PrivacyReport(
        exact_match_rate=round(exact_rate, 6),
        mean_source_similarity=round(mean_similarity, 6),
        near_duplicate_count=near_count,
        near_duplicate_rate=round(near_rate, 6),
        rare_combination_exposure=round(rare_exposure, 6),
        quasi_identifier_risk=round(quasi_risk, 6),
        threshold_results=gates,
        passed=passed,
        risk_category=risk_category,
        residual_risk="Synthetic data is not automatically anonymous; recipient auxiliary information and rare combinations remain relevant.",
        limitations=[
            "Local nearest-neighbour test is a reproducible screening gate, not a formal privacy guarantee.",
            "No production population or adversary model is represented.",
        ],
        evidence_hash=_hash(payload),
    )
