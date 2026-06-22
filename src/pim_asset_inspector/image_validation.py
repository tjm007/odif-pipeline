from pathlib import Path
from typing import Any
from PIL import Image

def extract_image_properties(file_path: Path) -> dict[str, Any]:
    """Extract image file properties without applying validation rules."""

    file_size_mb = round(
        file_path.stat().st_size / (1024 * 1024),
        2,
    )

    with Image.open(file_path) as image:
        image_properties = {
            "filename": file_path.name,
            "extension": file_path.suffix.lower(),
            "detected_format": image.format,
            "width": image.width,
            "height": image.height,
            "file_size_mb": file_size_mb,
            "color_mode": image.mode
        }
    
    return image_properties

def validate_image_properties(
        image_properties: dict[str, Any],
        rules: dict[str, Any],
) -> dict[str, Any]:
    """Validate extracted image properties against configured rules"""

    issues: list[str] = []

    allowed_extensions = rules["allowed_extensions"]
    max_file_size_mb = rules["max_file_size_mb"]
    min_width = rules["min_width"]
    min_height = rules["min_height"]
    allowed_color_modes = rules["allowed_color_modes"]

    if image_properties["extension"] not in allowed_extensions:
        issues.append(
            f"Extension not allowed: {image_properties['extension']}"
        )

    if image_properties["file_size_mb"] > max_file_size_mb:
        issues.append(
            f"File size exceeds maximum: {image_properties['file_size_mb']:.2f} MB"
        )
    
    if image_properties["width"] < min_width:
        issues.append(
            f"Width below minimum: {image_properties['width']}"
        )

    if image_properties["height"] < min_height:
        issues.append(
            f"Height below minimum: {image_properties['height']}"
        )
    
    if image_properties["color_mode"] not in allowed_color_modes:
        issues.append(
            f"Color mode not allowed: {image_properties['color_mode']}"
        )


    validation_result = {
        "validator": "image",
        "is_valid": len(issues) == 0,
        "issues": issues,
        "details": image_properties,
    }

    return validation_result