import pandas as pd


def transform_sales_data(sales_df: pd.DataFrame) -> pd.DataFrame:
    transformed_df = sales_df.copy()

    transformed_df["product"] = transformed_df["product"].str.strip()
    transformed_df["quantity"] = transformed_df["quantity"].astype(int)
    transformed_df["revenue"] = transformed_df["revenue"].astype(float)

    transformed_df["unit_price"] = (
        transformed_df["revenue"] / transformed_df["quantity"]
    )

    return transformed_df