import pandas as pd

def validate_sales_data(sales_df: pd.DataFrame) -> list[str]:
    errors: list[str] = []

    required_columns = ["product", "quantity", "revenue"]

    for column in required_columns:
        if column not in sales_df.columns:
            errors.append(f"Missing required column: (column)")
    
    if errors:
        return errors


    if sales_df.empty:
        errors.append("Sales data is empty.")
    
    if sales_df["product"].isnull().any():
        errors.append("Product column contains null values.")

    if sales_df["quantity"].isnull().any():
        errors.append("Quantity column contains null values.")

    if sales_df["revenue"].isnull().any():
        errors.append("Revenue column contains null values.")

    if (sales_df["quantity"] < 0).any():
        errors.append("Sales column contains negative values.")

    if (sales_df["revenue"] < 0).any():
        errors.append("Revenue column contains negative values.")

    return errors
