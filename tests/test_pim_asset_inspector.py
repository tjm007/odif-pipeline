from pathlib import Path
from PIL import Image


from src.pim_asset_inspector.config_loader import load_rules_from_json
from src.pim_asset_inspector.file_inventory import inventory_files
from src.pim_asset_inspector.filename_validation import validate_filename
from src.pim_asset_inspector.asset_inspector import inspect_assets
from src.pim_asset_inspector.image_validation import extract_image_properties
from src.pim_asset_inspector.image_validation import validate_image_properties
from src.pim_asset_inspector.report_writer import (
    build_report_rows,
    write_csv_report,
)
from src.pim_asset_inspector.required_asset_validation import validate_required_assets

from tests.fixtures import build_asset_result_with_filename_parts



def test_load_rules_from_json_returns_rules_dictionary() -> None:
    rules_path = Path("config/pim_asset_rules.json")

    rules = load_rules_from_json(rules_path)

    assert isinstance(rules, dict)
    assert rules["asset_type"] == "image"
    assert ".jpg" in rules["allowed_extensions"]
    assert rules["filename"]["separator"] == "_"


def test_inventory_files_returns_files_from_asset_folder(tmp_path: Path) -> None:
    asset_folder = tmp_path / "assets"
    asset_folder.mkdir()

    image_file = asset_folder / "ABC123_FRONT_01.jpg"
    image_file.write_text("fake image content")

    files = inventory_files(asset_folder)

    assert files == [image_file]


def test_validate_filename_returns_parsed_valid_result(
        pim_image_rules: dict,
) -> None:

    result = validate_filename(Path("ABC123_FRONT_01.jpg"), pim_image_rules)

    assert result["details"]["filename"] == "ABC123_FRONT_01.jpg"
    assert result["details"]["sku"] == "ABC123"
    assert result["details"]["view"] == "FRONT"
    assert result["details"]["sequence"] == "01"
    assert result["is_valid"] is True
    assert result["issues"] == []

def test_validate_filename_fails_when_segment_count_is_wrong(
        pim_image_rules: dict,
) -> None:

    result = validate_filename(Path("ABC123_FRONT.jpg"), pim_image_rules)

    assert result["is_valid"] is False
    assert result["details"]["sku"] is None
    assert "Expected 3 filename segments, found 2" in result["issues"]


def test_validate_filename_fails_when_view_is_invalid(
        pim_image_rules: dict,
) -> None:

    result = validate_filename(Path("ABC123_POTATO_01.jpg"), pim_image_rules)

    assert result["is_valid"] is False
    assert "Invalid view value: POTATO" in result["issues"]

def test_validate_filename_fails_when_sequence_format_is_invalid(
        pim_image_rules: dict,
) -> None:

    result = validate_filename(Path("ABC123_FRONT_A1.jpg"), pim_image_rules)

    assert result["is_valid"] is False
    assert "Invalid sequence format: A1" in result["issues"]

def test_inspect_assets_returns_results_for_all_files(
        tmp_path: Path,
        pim_image_rules: dict,
) -> None:

    asset_folder = tmp_path / "assets"
    asset_folder.mkdir()

    valid_file = asset_folder / "ABC123_FRONT_01.jpg"
    invalid_file = asset_folder / "ABC123_POTATO_01.jpg"

    valid_image = Image.new(
        "RGB",
        (1200, 1200),
    )

    invalid_image = Image.new(
        "RGB",
        (1200, 1200),
    )

    valid_image.save(valid_file)
    invalid_image.save(invalid_file)

    results = inspect_assets(asset_folder, pim_image_rules)

    assert len(results) == 2

    valid_results = [
        result
        for result in results
        if result["is_valid"] is True
    ]

    invalid_results = [
        result
        for result in results
        if result["is_valid"] is False
    ]

    assert len(valid_results) == 1
    assert len(invalid_results) == 1

def test_extract_image_properties_returns_image_metadata(tmp_path: Path) -> None:
    image_path = tmp_path / "ABC123_FRONT_01.jpg"

    test_image = Image.new(
        "RGB",
        (1200, 1200),
    )

    test_image.save(image_path)

    image_properties = extract_image_properties(image_path)

    assert image_properties["filename"] == "ABC123_FRONT_01.jpg"
    assert image_properties["extension"] == ".jpg"
    assert image_properties["detected_format"] == "JPEG"
    assert image_properties["width"] == 1200
    assert image_properties["height"] == 1200
    assert image_properties["file_size_mb"] > 0

def test_validation_image_properties_returns_valid_result(
        pim_image_rules: dict,
) -> None:
    image_properties = {
        "filename": "ABC123_FRONT_01.jpg",
        "extension": ".jpg",
        "detected_format": "JPEG",
        "width": 1200,
        "height": 1200,
        "file_size_mb": 1.0,
        "color_mode": "RGB",
    }

    validation_result = validate_image_properties(
        image_properties,
        pim_image_rules,
    )

    assert validation_result["validator"] == "image"
    assert validation_result["is_valid"] is True
    assert validation_result["issues"] == []
    assert validation_result["details"]["width"] == 1200

def test_validate_image_properties_fails_for_disallowed_extension(
        pim_image_rules: dict,
) -> None:
    image_properties = {
        "filename": "ABC123_FRONT_01.gif",
        "extension": ".gif",
        "detected_format": "GIF",
        "width": 1200,
        "height": 1200,
        "file_size_mb": 1.0,
        "color_mode": "RGB",
    }

    validation_result = validate_image_properties(
        image_properties,
        pim_image_rules,
    )

    assert validation_result["is_valid"] is False
    assert "Extension not allowed: .gif" in validation_result["issues"]

def test_validate_image_properties_fails_for_small_width(
        pim_image_rules: dict,
) -> None:
    image_properties = {
        "filename": "ABC123_FRONT_01.jpg",
        "extension": ".jpg",
        "detected_format": "JPEG",
        "width": 800,
        "height": 1200,
        "file_size_mb": 1.0,
        "color_mode": "RGB",
    }

    validation_result = validate_image_properties(
        image_properties,
        pim_image_rules,
    )

    assert validation_result["is_valid"] is False
    assert "Width below minimum: 800" in validation_result["issues"]

def test_validate_image_properties_fails_for_small_height(
        pim_image_rules: dict,
) -> None:
    image_properties = {
        "filename": "ABC123_FRONT_01.jpg",
        "extension": ".jpg",
        "detected_format": "JPEG",
        "width": 1200,
        "height": 800,
        "file_size_mb": 1.0,
        "color_mode": "RGB",
    }

    validation_result = validate_image_properties(
        image_properties,
        pim_image_rules,
    )

    assert validation_result["is_valid"] is False
    assert "Height below minimum: 800" in validation_result["issues"]

def test_validate_image_properties_fails_for_large_file_size(
        pim_image_rules: dict,
) -> None:
    image_properties = {
        "filename": "ABC123_FRONT_01.jpg",
        "extension": ".jpg",
        "detected_format": "JPEG",
        "width": 1200,
        "height": 1200,
        "file_size_mb": 10.0,
        "color_mode": "RGB",
    }

    validation_result = validate_image_properties(
        image_properties,
        pim_image_rules,
    )

    assert validation_result["is_valid"] is False
    assert any(
        "File size exceeds maximum" in issue
        for issue in validation_result["issues"]
    )

def test_validate_image_properties_fails_for_disallowed_color_mode(
        pim_image_rules: dict,
) -> None:
    image_properties = {
        "filename": "ABC123_FRONT_01.jpg",
        "extension": ".jpg",
        "detected_format": "JPEG",
        "color_mode": "CMYK",
        "width": 1200,
        "height": 1200,
        "file_size_mb": 1.0,
    }

    validation_result = validate_image_properties(
        image_properties,
        pim_image_rules,
    )

    assert validation_result["is_valid"] is False
    assert "Color mode not allowed: CMYK" in validation_result["issues"]

def test_inspect_assets_returns_combined_validator_results(
    tmp_path: Path,
    pim_image_rules: dict,
) -> None:

    asset_folder = tmp_path / "assets"
    asset_folder.mkdir()

    image_path = asset_folder / "ABC123_FRONT_01.jpg"

    image = Image.new(
        "RGB",
        (1200, 1200),
    )

    image.save(image_path)

    results = inspect_assets(
        asset_folder,
        pim_image_rules,
    )

    result = results[0]

    assert "validators" in result
    assert "filename" in result["validators"]
    assert "image" in result["validators"]

    assert (
        result["validators"]["filename"]["validator"]
        == "filename"
    )

    assert (
        result["validators"]["image"]["validator"]
        == "image"
    )

def test_build_report_rows_flattens_inspection_results() -> None:
    inspection_results = [
        {
            "file_path": "data/sample/pim_assets/ABC123_FRONT_01.jpg",
            "file_name": "ABC123_FRONT_01.jpg",
            "validators": {
                "filename": {
                    "validator": "filename",
                    "is_valid": True,
                    "issues": [],
                    "details": {
                        "filename": "ABC123_FRONT_01.jpg",
                        "sku": "ABC123",
                        "view": "FRONT",
                        "sequence": "01",
                    },
                },
                "image": {
                    "validator": "image",
                    "is_valid": True,
                    "issues": [],
                    "details": {
                        "filename": "ABC123_FRONT_01.jpg",
                        "extension": ".jpg",
                        "detected_format": "JPEG",
                        "color_mode": "RGB",
                        "width": 1200,
                        "height": 1200,
                        "file_size_mb": 0.1,
                    },
                },
            },
            "is_valid": True,
            "issues": [],
        }
    ]

    report_rows = build_report_rows(inspection_results)

    assert len(report_rows) == 1

    report_row = report_rows[0]

    assert report_row["file_name"] == "ABC123_FRONT_01.jpg"
    assert report_row["overall_status"] == "PASS"
    assert report_row["filename_status"] == "PASS"
    assert report_row["image_status"] == "PASS"
    assert report_row["sku"] == "ABC123"
    assert report_row["view"] == "FRONT"
    assert report_row["sequence"] == "01"
    assert report_row["detected_format"] == "JPEG"
    assert report_row["color_mode"] == "RGB"
    assert report_row["width"] == 1200
    assert report_row["height"] == 1200
    assert report_row["issues"] == ""

def test_write_csv_report_creates_report_file(tmp_path: Path) -> None:
    report_rows = [
        {
            "file_name": "ABC123_FRONT_01.jpg",
            "overall_status": "PASS",
            "filename_status": "PASS",
            "image_status": "PASS",
            "sku": "ABC123",
            "view": "FRONT",
            "sequence": "01",
            "detected_format": "JPEG",
            "color_mode": "RGB",
            "width": 1200,
            "height": 1200,
            "file_size_mb": 0.1,
            "issues": "",
        }
    ]

    output_path = tmp_path / "reports" / "pim_asset_inspection_report.csv"

    write_csv_report(
        report_rows,
        output_path,
    )

    assert output_path.exists()

    report_content = output_path.read_text(
        encoding="utf-8",
    )

    assert "file_name" in report_content
    assert "ABC123_FRONT_01.jpg" in report_content

def test_required_asset_validation_returns_empty_list_for_no_assets() -> None:
    asset_results = []
    required_views = ["FRONT", "BACK", "SIDE"]

    validation_results = validate_required_assets(
        asset_results,
        required_views,
    )

    expected_batch_result = {
        "validation_results": [],
        "skipped_files": [],
    }

    assert validation_results == expected_batch_result

def test_required_asset_validation_returns_valid_result_when_all_required_views_exist(
        required_asset_views,
) -> None:
    asset_results = [
        build_asset_result_with_filename_parts("SKU123", "FRONT", "01"),
        build_asset_result_with_filename_parts("SKU123", "BACK", "01"),
        build_asset_result_with_filename_parts("SKU123", "SIDE", "01"),
    ]
    
    required_views = ["FRONT", "BACK", "SIDE"]

    validation_results = validate_required_assets(
        asset_results,
        required_views,
    )

    expected_result = {
        "validator": "required_assets",
        "scope": "collection",
        "collection_key": "SKU123",
        "is_valid": True,
        "issues": [],
        "details": {
            "required_views": required_asset_views,
            "found_views": ["BACK","FRONT", "SIDE"],
            "missing_views": [],
            "file_count": 3,
        },
    }

    expected_batch_result = {
        "validation_results": [expected_result],
        "skipped_files": [],
    }

    assert validation_results == expected_batch_result

def test_required_asset_validation_returns_invalid_result_when_required_view_is_missing(
        required_asset_views,
) -> None:
    asset_results = [
        build_asset_result_with_filename_parts("SKU123", "FRONT", "01"),
        build_asset_result_with_filename_parts("SKU123", "BACK", "01"),
    ]

    required_views = required_asset_views

    validation_results = validate_required_assets(
        asset_results,
        required_views,
    )

    expected_result = {
        "validator": "required_assets",
        "scope": "collection",
        "collection_key": "SKU123",
        "is_valid": False,
        "issues": ["Missing required view: SIDE"],
        "details": {
            "required_views": ["FRONT", "BACK", "SIDE"],
            "found_views": ["BACK", "FRONT"],
            "missing_views": ["SIDE"],
            "file_count": 2,

        },
    }

    expected_batch_result = {
    "validation_results": [expected_result],
    "skipped_files": [],
    }

    assert validation_results == expected_batch_result

def test_required_asset_validation_returns_result_for_each_sku(
        required_asset_views,
) -> None:
    asset_results = [
        build_asset_result_with_filename_parts("SKU123", "FRONT", "01"),
        build_asset_result_with_filename_parts("SKU123", "BACK", "01"),
        build_asset_result_with_filename_parts("SKU123", "SIDE", "01"),
        build_asset_result_with_filename_parts("SKU456", "FRONT", "01"),
        build_asset_result_with_filename_parts("SKU456", "BACK", "01"),        
    ]

    validation_results = validate_required_assets(
        asset_results,
        required_asset_views,
    )

    sku_results = validation_results["validation_results"]

    first_result = sku_results[0]
    second_result = sku_results[1]

    assert first_result["collection_key"] == "SKU123"
    assert first_result["is_valid"] is True
    assert first_result["details"]["missing_views"] == []

    assert second_result["collection_key"] == "SKU456"
    assert second_result["is_valid"] is False
    assert second_result["details"]["missing_views"] == ["SIDE"]

    assert validation_results["skipped_files"] == []

def test_required_asset_validation_returns_multiple_missing_view_issues(
    required_asset_views,
) -> None:
    asset_results = [
        build_asset_result_with_filename_parts("SKU123", "FRONT", "01"),
    ]

    validation_results = validate_required_assets(
        asset_results,
        required_asset_views,
    )

    expected_result = {
        "validator": "required_assets",
        "scope": "collection",
        "collection_key": "SKU123",
        "is_valid": False,
        "issues": [
            "Missing required view: BACK",
            "Missing required view: SIDE",
        ],
        "details": {
            "required_views": ["FRONT", "BACK", "SIDE"],
            "found_views": ["FRONT"],
            "missing_views": ["BACK", "SIDE"],
            "file_count": 1,
        },
    }

    expected_batch_result = {
        "validation_results": [expected_result],
        "skipped_files": [],
    }

    assert validation_results == expected_batch_result

def test_required_asset_validation_tracks_skipped_files_when_filename_parts_are_missing(
    required_asset_views,
) -> None:
    asset_results = [
        build_asset_result_with_filename_parts("SKU123", "FRONT", "01"),
        {
            "file_path": "data/sample/assets/BAD_FILENAME.jpg",
            "file_name": "BAD_FILENAME.jpg",
            "validators": {
                "filename": {
                    "is_valid": False,
                    "details": {},
                }
            },
        },
    ]

    validation_results = validate_required_assets(
        asset_results,
        required_asset_views,
    )

    expected_result = {
        "validator": "required_assets",
        "scope": "collection",
        "collection_key": "SKU123",
        "is_valid": False,
        "issues": [
            "Missing required view: BACK",
            "Missing required view: SIDE",
        ],
        "details": {
            "required_views": ["FRONT", "BACK", "SIDE"],
            "found_views": ["FRONT"],
            "missing_views": ["BACK", "SIDE"],
            "file_count": 1,
        },
    }

    expected_batch_result = {
        "validation_results": [expected_result],
        "skipped_files": [
            {
                "file_path": "data/sample/assets/BAD_FILENAME.jpg",
                "file_name": "BAD_FILENAME.jpg",
                "reason": "Filename parsing unavailable",
            }
        ],
    }

    assert validation_results == expected_batch_result

def test_required_asset_validation_tracks_multiple_skipped_files(
    required_asset_views,
) -> None:
    asset_results = [
        build_asset_result_with_filename_parts("SKU123", "FRONT", "01"),
        {
            "file_path": "data/sample/assets/BAD_FILENAME_01.jpg",
            "file_name": "BAD_FILENAME_01.jpg",
            "validators": {
                "filename": {
                    "is_valid": False,
                    "details": {},
                }
            },
        },
        {
            "file_path": "data/sample/assets/BAD_FILENAME_02.jpg",
            "file_name": "BAD_FILENAME_02.jpg",
            "validators": {
                "filename": {
                    "is_valid": False,
                    "details": {},
                }
            },
        },
    ]

    validation_results = validate_required_assets(
        asset_results,
        required_asset_views,
    )

    expected_skipped_files = [
        {
            "file_path": "data/sample/assets/BAD_FILENAME_01.jpg",
            "file_name": "BAD_FILENAME_01.jpg",
            "reason": "Filename parsing unavailable",
        },
        {
            "file_path": "data/sample/assets/BAD_FILENAME_02.jpg",
            "file_name": "BAD_FILENAME_02.jpg",
            "reason": "Filename parsing unavailable",
        },
    ]

    assert validation_results["skipped_files"] == expected_skipped_files