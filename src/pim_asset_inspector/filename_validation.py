from pathlib import Path
import re
from typing import Any

def validate_filename(
        file_path: Path,
        rules: dict[str, Any]
) -> dict[str, Any]:
    """Validate a file name against configured PIM naming rules."""
    
    filename = file_path.name
    stem = file_path.stem

    filename_rules = rules["filename"]
    separator = filename_rules["separator"]
    required_segments = filename_rules["required_segments"]
    allowed_views = filename_rules["allowed_views"]
    sequence_pattern = filename_rules["sequence_pattern"]

    segments = stem.split(separator)
    issues: list[str] = []

    details: dict[str, Any] = {
        "filename": filename,
        "sku": None,
        "view": None,
        "sequence": None,
    }

    if len(segments) != len(required_segments):
        issues.append(
            f"Expected {len(required_segments)} filename segments, found {len(segments)}"
        )
    
        validation_result = {
            "validator": "filename",
            "is_valid": False,
            "issues": issues,
            "details": details,
        }

        return validation_result

    sku, view, sequence = segments
        
    details["sku"] = sku
    details["view"] = view
    details["sequence"] = sequence
    
    if view not in allowed_views:
        issues.append(f"Invalid view value: {view}")
    
    if re.fullmatch(sequence_pattern, sequence) is None:
        issues.append(f"Invalid sequence format: {sequence}")

    validation_result = {
        "validator": "filename",
        "is_valid": len(issues) == 0,
        "issues": issues,
        "details": details,
    }

    return validation_result
    
