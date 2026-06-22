import pandas as pd
import pytest

from pathlib import Path
from typing import Any



@pytest.fixture
def valid_sales_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "product": ["Widget A"],
            "quantity": [10],
            "revenue": [100.0],
        }
    )

@pytest.fixture
def sample_sales_csv_path() -> Path:
    return Path("data/sample/sales_data_sample.csv")


@pytest.fixture
def processed_sales_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "product": ["Notebook", "Sticker", "Mug", "Pen"],
            "quantity": [25, 40, 15, 30],
            "revenue": [125.00, 80.00, 150.00, 45.00],
            "unit_price": [5.00, 2.00, 10.00, 1.50],
        }
    )

@pytest.fixture
def pim_image_rules() -> dict:
    return {
        "filename": {
            "separator": "_",
            "required_segments": ["sku", "view", "sequence"],
            "allowed_views": ["FRONT", "BACK", "SIDE", "DETAIL"],
            "sequence_pattern": "^[0-9]{2}$",
        },
        "allowed_extensions": [".jpg", ".jpeg", ".png", ".webp"],
        "allowed_color_modes": ["RGB"],
        "max_file_size_mb": 5,
        "min_width": 1200,
        "min_height": 1200,
    }

@pytest.fixture
def required_asset_views() -> list[str]:
    required_views = ["FRONT", "BACK", "SIDE"]

    return required_views

def build_asset_result_with_filename_parts(
    sku: str,
    view: str,
    sequence: str,
) -> dict[str, Any]:
    file_name = f"{sku}_{view}_{sequence}.jpg"
    file_path = f"data/sample/assets/{file_name}"

    asset_result = {
        "file_path": file_path,
        "file_name": file_name,
        "validators": {
            "filename": {
                "is_valid": True,
                "details": {
                    "parsed_values": {
                        "sku": sku,
                        "view": view,
                        "sequence": sequence,
                    }
                },
            }
        },
    }

    return asset_result