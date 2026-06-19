from pathlib import Path
from typing import Any

from src.pim_asset_inspector.file_inventory import inventory_files
from src.pim_asset_inspector.filename_validation import validate_filename

def inspect_assets(
        asset_folder: Path,
        rules: dict[str, Any]
) -> list[dict[str, Any]]:
    """Inspect asset files and return validation results."""

    file_paths = inventory_files(asset_folder)

    inspection_results = []

    for file_path in file_paths:
        validation_result = validate_filename(
            file_path,
            rules,
        )

        inspection_results.append(
            validation_result,
        )
    
    return inspection_results