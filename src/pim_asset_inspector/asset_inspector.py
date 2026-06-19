from pathlib import Path
from typing import Any

from src.pim_asset_inspector.file_inventory import inventory_files
from src.pim_asset_inspector.filename_validation import validate_filename
from src.pim_asset_inspector.image_validation import(
    extract_image_properties,
    validate_image_properties,
)

def inspect_assets(
        asset_folder: Path,
        rules: dict[str, Any]
) -> list[dict[str, Any]]:
    """Inspect asset files and return validation results."""

    file_paths = inventory_files(asset_folder)

    inspection_results = []

    for file_path in file_paths:
        filename_result = validate_filename(
            file_path,
            rules,
        )

        image_properties = extract_image_properties(file_path)

        image_result = validate_image_properties(
            image_properties,
            rules,
        )

        asset_issues = []
        asset_issues.extend(filename_result["issues"])
        asset_issues.extend(image_result["issues"])

        asset_result = {
            "file_path": str(file_path),
            "file_name": file_path.name,
            "validators": {
                "filename": filename_result,
                "image": image_result,
            },
            "is_valid": len(asset_issues) == 0,
            "issues": asset_issues,
        }

        inspection_results.append(asset_result)

    return inspection_results