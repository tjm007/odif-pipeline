import pandas as pd

from src.schema.sales_schema import (
    PRODUCT_COLUMN,
    QUANTITY_COLUMN,
    REVENUE_COLUMN,
    UNIT_PRICE_COLUMN,
)

def transform_sales_data(sales_df: pd.DataFrame) -> pd.DataFrame:
    transformed_df = sales_df.copy()

    transformed_df[PRODUCT_COLUMN] = transformed_df[PRODUCT_COLUMN].str.strip()
    transformed_df[QUANTITY_COLUMN] = transformed_df[QUANTITY_COLUMN].astype(int)
    transformed_df[REVENUE_COLUMN] = transformed_df[REVENUE_COLUMN].astype(float)

    transformed_df[UNIT_PRICE_COLUMN] = (
        transformed_df[REVENUE_COLUMN] / transformed_df[QUANTITY_COLUMN]
    )

    return transformed_df