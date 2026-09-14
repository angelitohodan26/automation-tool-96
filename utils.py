import json
import os
from datetime import datetime
from typing import Any, Dict, Optional

def load_json_config(filepath: str) -> Dict[str, Any]:
    """Loads and parses a configuration JSON file."""
    if not os.path.exists(filepath):
        return {}
    with open(filepath, 'r') as f:
        return json.load(f)

def save_json_config(filepath: str, data: Dict[str, Any]) -> None:
    """Writes data dictionary to a JSON file."""
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)

def get_timestamp_string() -> str:
    """Returns current UTC timestamp in ISO format."""
    return datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

def ensure_directory_exists(path: str) -> None:
    """Creates directory structure if missing."""
    if not os.path.exists(path):
        os.makedirs(path)

def format_byte_size(size_bytes: int) -> str:
    """Converts raw bytes into human readable string."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"