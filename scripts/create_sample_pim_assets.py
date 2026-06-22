"""
Generate sample PIM asset files for demos,
testing, and portfolio examples.
"""

from pathlib import Path
from PIL import Image

asset_folder = Path("data/sample/pim_assets")
asset_folder.mkdir(parents=True, exist_ok=True)

file_names = [
    "SKU123_FRONT_01.jpg",
    "SKU123_BACK_01.jpg",
    "SKU123_SIDE_01.jpg",
    "SKU456_FRONT_01.jpg",
    "SKU456_BACK_01.jpg",
]

for file_name in file_names:
    image = Image.new(
        "RGB",
        (1200, 1200),
        color="white",
    )
    output_path = asset_folder / file_name
    image.save(output_path)