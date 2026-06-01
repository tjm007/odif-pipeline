import pandas as pd

from src.schema.sales_schema import UNIT_PRICE_COLUMN
from src.transform.sales_transform import transform_sales_data


def test_transform_sales_data_adds_unit_price_column() -> None:
    sales_df = pd.DataFrame(
        {
            "product": ["Widget A"],
            "quantity": [10],
            "revenue": [100.0],
        }
    )

    transformed_df = transform_sales_data(sales_df)

    assert UNIT_PRICE_COLUMN in transformed_df.columns

def test_transform_sales_data_calculates_unit_price() -> None:
    sales_df = pd.DataFrame(
        {
            "product": ["Widget A"],
            "quantity": [10],
            "revenue": [100.0],
        }
    )

    transformed_df = transform_sales_data(sales_df)

    assert transformed_df[UNIT_PRICE_COLUMN].iloc[0] == 10.0