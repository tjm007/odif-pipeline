import pandas as pd

from src.config import SALES_DATA_FILE

def generate_sales_data() -> pd.DataFrame:
    data = {
        "product": ["Widget A", "Widget B", "Widget C"],
        "quantity": [10, 15, 8],
        "revenue": [100.0, 225.0, 96.0]
    }

    return pd.DataFrame(data)

def save_sales_data(df: pd.DataFrame) -> None:
    SALES_DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    df.to_csv(SALES_DATA_FILE, index = False)


def load_sales_data() -> pd.DataFrame:
    return pd.read_csv(SALES_DATA_FILE)