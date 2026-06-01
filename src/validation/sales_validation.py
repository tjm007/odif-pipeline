import pandas as pd

from src.schema.sales_schema import (
    PRODUCT_COLUMN,
    QUANTITY_COLUMN,
    REVENUE_COLUMN,
    REQUIRED_RAW_SALES_COLUMNS,
)

def validate_sales_data(sales_df: pd.DataFrame) -> list[str]:
    errors: list[str] = []

    for column in REQUIRED_RAW_SALES_COLUMNS:
        if column not in sales_df.columns:
            errors.append(f"Missing required column: {column}")
    
    if errors:
        return errors


    if sales_df.empty:
        errors.append("Sales data is empty.")
    
    if sales_df[PRODUCT_COLUMN].isnull().any():
        errors.append("Product column contains null values.")

    if sales_df[QUANTITY_COLUMN].isnull().any():
        errors.append("Quantity column contains null values.")

    if sales_df[REVENUE_COLUMN].isnull().any():
        errors.append("Revenue column contains null values.")

    if (sales_df[QUANTITY_COLUMN] < 0).any():
        errors.append("Sales column contains negative values.")

    if (sales_df[REVENUE_COLUMN] < 0).any():
        errors.append("Revenue column contains negative values.")

    return errors
