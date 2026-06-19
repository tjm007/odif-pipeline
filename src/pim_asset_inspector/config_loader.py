from pathlib import Path
import json
from typing import Any



def load_rules_from_json(rules_path: Path) -> dict[str, Any]:
    """Load PIM asset inspection rules from a JSON file."""

    if not rules_path.exists():
        raise FileNotFoundError(f"Rules file not found: {rules_path}")
    
    with rules_path.open("r", encoding="utf-8") as file:
        rules = json.load(file)

    return rules