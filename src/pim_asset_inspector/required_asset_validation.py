

"""
Required Asset Validation operates at the batch level.

Output structure:

{
    "validation_results": [...],
    "skipped_files": [...]
}
"""


from typing import Any


def validate_required_assets(
    asset_results: list[dict[str, Any]],
    required_views: list[str],
) -> list[dict[str, Any]]:
    assets_by_sku: dict[str, list[dict[str, Any]]] = {}
    skipped_files = []

    for asset_result in asset_results:
        filename_validator = asset_result["validators"]["filename"]
        filename_details = filename_validator["details"]
        parsed_values = filename_details.get("parsed_values")

        if parsed_values is None:
            if "sku" in filename_details and "view" in filename_details:
                parsed_values = {
                    "sku": filename_details["sku"],
                    "view": filename_details["view"],
                    "sequence": filename_details.get("sequence"),
                }

        if parsed_values is None:
            skipped_file = {
                "file_path": asset_result["file_path"],
                "file_name": asset_result["file_name"],
                "reason": "Filename parsing unavailable",
            }

            skipped_files.append(skipped_file)
            continue

        sku = parsed_values["sku"]

        if sku not in assets_by_sku:
            assets_by_sku[sku] = []

        assets_by_sku[sku].append(asset_result)

    validation_results = []

    for sku, sku_assets in assets_by_sku.items():
        found_views = []

        for sku_asset in sku_assets:
            filename_validator = sku_asset["validators"]["filename"]
            filename_details = filename_validator["details"]
            parsed_values = filename_details.get("parsed_values")

            if parsed_values is None:
                parsed_values = {
                    "sku": filename_details["sku"],
                    "view": filename_details["view"],
                    "sequence": filename_details.get("sequence"),
                }

            view = parsed_values["view"]

            found_views.append(view)

        missing_views = []

        for required_view in required_views:
            if required_view not in found_views:
                missing_views.append(required_view)

        issues = []

        for missing_view in missing_views:
            issue = f"Missing required view: {missing_view}"
            issues.append(issue)

        sorted_found_views = sorted(found_views)

        result = {
            "validator": "required_assets",
            "scope": "collection",
            "collection_key": sku,
            "is_valid": len(missing_views) == 0,
            "issues": issues,
            "details": {
                "required_views": required_views,
                "found_views": sorted_found_views,
                "missing_views": missing_views,
                "file_count": len(sku_assets),
            },
        }

        validation_results.append(result)

    batch_result = {
        "validation_results": validation_results,
        "skipped_files": skipped_files,
    }

    return batch_result