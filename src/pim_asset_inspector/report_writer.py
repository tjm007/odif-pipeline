from typing import Any
import csv
from pathlib import Path


def format_status(is_valid: bool) -> str:
    """Convert validation boolean into report friendly status text."""

    status = "PASS"

    if is_valid is False:
        status = "FAIL"

    return status

def build_report_rows(
        inspection_results: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Build flattened report rows from asset inspection results."""

    report_rows = []

    for inspection_result in inspection_results:
        filename_result = inspection_result["validators"]["filename"]
        image_result = inspection_result["validators"]["image"]

        filename_details = filename_result["details"]
        image_details = image_result["details"]

        issues = "; ".join(inspection_result["issues"])

        report_row = {
            "file_name": inspection_result["file_name"],
            "overall_status": format_status(
                inspection_result["is_valid"],
            ),
            "filename_status": format_status(
                filename_result["is_valid"],
            ),
            "image_status": format_status(
                image_result["is_valid"],
            ),
            "sku": filename_details["sku"],
            "view": filename_details["view"],
            "sequence": filename_details["sequence"],
            "detected_format": image_details["detected_format"],
            "width": image_details["width"],
            "height": image_details["height"],
            "file_size_mb": image_details["file_size_mb"],
            "issues": issues,
        }

        report_rows.append(report_row)

    return report_rows

def write_csv_report(
    report_rows: list[dict[str, Any]],
    output_path: Path,
) -> None:
    """Write report rows to a CSV file."""

    if len(report_rows) == 0:
        raise ValueError("Cannot write CSV report with no report rows.")

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    fieldnames = list(report_rows[0].keys())

    with output_path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )

        writer.writeheader()
        writer.writerows(report_rows)