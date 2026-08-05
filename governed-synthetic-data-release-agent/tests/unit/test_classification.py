import pandas as pd

from governed_release.application.classification import classify_fields
from governed_release.domain.enums import FieldClass, ReleaseDisposition


def test_direct_identifiers_are_prohibited() -> None:
    frame = pd.DataFrame(
        {"customer_id": ["CUST-1234"], "account_number": ["123456789012"], "city": ["Toronto"]}
    )
    results = {item.field_name: item for item in classify_fields(frame)}
    assert results["customer_id"].field_class == FieldClass.DIRECT_IDENTIFIER
    assert results["account_number"].disposition == ReleaseDisposition.PROHIBITED
    assert results["city"].disposition == ReleaseDisposition.PERMITTED
