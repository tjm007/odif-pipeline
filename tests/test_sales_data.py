import pandas as pd

from src.config import PROCESSED_SALES_DATA_FILE
from src.data.sales_data import save_processed_sales_data


def test_save_processed_sales_data_creates_file() -> None:
    sales_df = pd.DataFrame(
        {
            "product": ["Widget A"],
            "quantity": [10],
            "revenue": [100.0],
            "unit_price": [10.0],
        }
    )
    
    save_processed_sales_data(sales_df)

    assert PROCESSED_SALES_DATA_FILE.exists()