from __future__ import annotations

import re

import pandas as pd

from governed_release.domain.enums import FieldClass, ReleaseDisposition
from governed_release.domain.models import FieldClassification

RULES: dict[str, tuple[FieldClass, ReleaseDisposition, str, str]] = {
    "transaction_id": (
        FieldClass.OPERATIONAL_ATTRIBUTE,
        ReleaseDisposition.PROHIBITED,
        "COL-OPS-001",
        "Source transaction key is not needed in the released dataset.",
    ),
    "customer_id": (
        FieldClass.DIRECT_IDENTIFIER,
        ReleaseDisposition.PROHIBITED,
        "COL-PII-001",
        "Internal customer identifier.",
    ),
    "account_number": (
        FieldClass.DIRECT_IDENTIFIER,
        ReleaseDisposition.PROHIBITED,
        "COL-PII-002",
        "Fictional account number treated as restricted identifier.",
    ),
    "transaction_timestamp": (
        FieldClass.QUASI_IDENTIFIER,
        ReleaseDisposition.PERMITTED,
        "COL-QID-001",
        "Timestamp is a quasi-identifier and is generated, not copied.",
    ),
    "city": (
        FieldClass.QUASI_IDENTIFIER,
        ReleaseDisposition.PERMITTED,
        "COL-QID-002",
        "City can contribute to re-identification risk.",
    ),
    "province": (
        FieldClass.QUASI_IDENTIFIER,
        ReleaseDisposition.PERMITTED,
        "COL-QID-003",
        "Province is a coarse quasi-identifier.",
    ),
    "is_fraud": (
        FieldClass.SENSITIVE_ATTRIBUTE,
        ReleaseDisposition.PERMITTED,
        "COL-SEN-001",
        "Fraud label is sensitive analytical data.",
    ),
    "transaction_amount": (
        FieldClass.SENSITIVE_ATTRIBUTE,
        ReleaseDisposition.PERMITTED,
        "COL-SEN-002",
        "Transaction amount is sensitive financial behaviour.",
    ),
    "account_tenure_months": (
        FieldClass.DERIVED_FEATURE,
        ReleaseDisposition.PERMITTED,
        "COL-DER-001",
        "Derived account feature.",
    ),
    "transactions_last_24h": (
        FieldClass.DERIVED_FEATURE,
        ReleaseDisposition.PERMITTED,
        "COL-DER-002",
        "Derived velocity feature.",
    ),
    "average_transaction_amount_30d": (
        FieldClass.DERIVED_FEATURE,
        ReleaseDisposition.PERMITTED,
        "COL-DER-003",
        "Derived behavioural aggregate.",
    ),
    "merchant_category": (
        FieldClass.OPERATIONAL_ATTRIBUTE,
        ReleaseDisposition.PERMITTED,
        "COL-OPS-002",
        "Operational merchant grouping.",
    ),
}

ACCOUNT_RE = re.compile(r"^\d{8,16}$")
CUSTOMER_RE = re.compile(r"^CUST[-_A-Z0-9]+$", re.I)


def classify_fields(data: pd.DataFrame) -> list[FieldClassification]:
    results: list[FieldClassification] = []
    for column in data.columns:
        if column in RULES:
            field_class, disposition, rule_id, reason = RULES[column]
            method = "deterministic-column-rule"
            confidence = 1.0
        else:
            sample = data[column].dropna().astype(str).head(50)
            if any(ACCOUNT_RE.match(v) for v in sample):
                field_class, disposition, rule_id, reason = (
                    FieldClass.DIRECT_IDENTIFIER,
                    ReleaseDisposition.PROHIBITED,
                    "REC-ACC-001",
                    "Structured account-number recognizer matched.",
                )
            elif any(CUSTOMER_RE.match(v) for v in sample):
                field_class, disposition, rule_id, reason = (
                    FieldClass.DIRECT_IDENTIFIER,
                    ReleaseDisposition.PROHIBITED,
                    "REC-CUST-001",
                    "Structured customer-ID recognizer matched.",
                )
            else:
                field_class, disposition, rule_id, reason = (
                    FieldClass.OPERATIONAL_ATTRIBUTE,
                    ReleaseDisposition.PROHIBITED,
                    "COL-UNKNOWN-001",
                    "Unknown fields default to prohibited.",
                )
            method = "deterministic-structured-recognizer"
            confidence = 0.95
        results.append(
            FieldClassification(
                field_name=column,
                field_class=field_class,
                disposition=disposition,
                detection_method=method,
                confidence=confidence,
                rule_id=rule_id,
                reason=reason,
            )
        )
    return results
