from pathlib import Path

from src.pim_asset_inspector.config_loader import load_rules_from_json
from src.pim_asset_inspector.file_inventory import inventory_files
from src.pim_asset_inspector.filename_validation import validate_filename


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


def test_validate_filename_returns_parsed_valid_result() -> None:
    rules = {
        "filename": {
            "separator": "_",
            "required_segments": ["sku", "view", "sequence"],
            "allowed_views": ["FRONT", "BACK", "SIDE", "DETAIL"],
            "sequence_pattern": "^[0-9]{2}$",
        }
    }

    result = validate_filename(Path("ABC123_FRONT_01.jpg"), rules)

    assert result["filename"] == "ABC123_FRONT_01.jpg"
    assert result["sku"] == "ABC123"
    assert result["view"] == "FRONT"
    assert result["sequence"] == "01"
    assert result["is_valid"] is True
    assert result["issues"] == []

def test_validate_filename_fails_when_segment_count_is_wrong() -> None:
    rules = {
        "filename": {
            "separator": "_",
            "required_segments": ["sku", "view", "sequence"],
            "allowed_views": ["FRONT", "BACK", "SIDE", "DETAIL"],
            "sequence_pattern": "^[0-9]{2}$",
        }
    }

    result = validate_filename(Path("ABC123_FRONT.jpg"), rules)

    assert result["is_valid"] is False
    assert result["sku"] is None
    assert "Expected 3 filename segments, found 2" in result["issues"]


def test_validate_filename_fails_when_view_is_invalid() -> None:
    rules = {
        "filename": {
            "separator": "_",
            "required_segments": ["sku", "view", "sequence"],
            "allowed_views": ["FRONT", "BACK", "SIDE", "DETAIL"],
            "sequence_pattern": "^[0-9]{2}$",
        }
    }

    result = validate_filename(Path("ABC123_POTATO_01.jpg"), rules)

    assert result["is_valid"] is False
    assert "Invalid view value: POTATO" in result["issues"]

def test_validate_filename_fails_when_sequence_format_is_invalid() -> None:
    rules = {
        "filename": {
            "separator": "_",
            "required_segments": ["sku", "view", "sequence"],
            "allowed_views": ["FRONT", "BACK", "SIDE", "DETAIL"],
            "sequence_pattern": "^[0-9]{2}$",
        }
    }

    result = validate_filename(Path("ABC123_FRONT_A1.jpg"), rules)

    assert result["is_valid"] is False
    assert "Invalid sequence format: A1" in result["issues"]