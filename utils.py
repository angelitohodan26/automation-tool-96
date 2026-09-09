import json
import os
from typing import Any, Dict, Optional

def load_json_file(file_path: str) -> Optional[Dict[str, Any]]:
    """
    Safely load and parse a JSON configuration file.
    Returns None if file is missing or corrupted.
    """
    if not os.path.exists(file_path):
        return None
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return None

def sanitize_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Remove null values from dictionary to clean payloads.
    """
    return {k: v for k, v in data.items() if v is not None}

def format_byte_size(size_bytes: int) -> str:
    """
    Convert raw bytes into a human readable string.
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} TB"

def get_env_var(key: str, default: str = "") -> str:
    """
    Retrieve environment variables with sensible defaults.
    """
    return os.environ.get(key, default)