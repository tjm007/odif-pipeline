import pandas as pd

from src.validation.sales_validation import validate_sales_data


def test_validate_sales_data_passes_for_valid_data() -> None:
    sales_df = pd.DataFrame(
        {
            "product": ["Widget A"],
            "quantity": [10],
            "revenue": [100.0],
        }
    )

    errors = validate_sales_data(sales_df)

    assert errors == []

def test_validate_sales_date_fails_for_negative_revenue() -> None:
    sales_df = pd.DataFrame(
        {
            "product": ["Widget A"],
            "quantity": [10],
            "revenue": [-100.0],
        }
    )

    errors = validate_sales_data(sales_df)

    assert "Revenue column contains negative values." in errors

def test_validate_sales_data_fails_for_missing_revenue_column() -> None:
    sales_df = pd.DataFrame(
        {
            "product": ["Widget A"],
            "quantity": [10],
        }
    )

    errors = validate_sales_data(sales_df)

    assert "Missing required column: revenue" in errors
    