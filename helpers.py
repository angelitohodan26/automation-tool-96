import json
import os
from datetime import datetime
from typing import Any, Dict


def load_json_file(file_path: str) -> Dict[str, Any]:
    """Load and parse a JSON file from disk."""
    if not os.path.exists(file_path):
        return {}
    
    with open(file_path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}


def save_json_file(file_path: str, data: Dict[str, Any]) -> bool:
    """Serialize and save dictionary data to a JSON file."""
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        return True
    except IOError:
        return False


def get_current_timestamp() -> str:
    """Generate a standardized ISO timestamp string."""
    return datetime.utcnow().isoformat() + "Z"


def sanitize_string(text: str) -> str:
    """Strip whitespace and normalize string input."""
    if not isinstance(text, str):
        return ""
    return " ".join(text.strip().split())
