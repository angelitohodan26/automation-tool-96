import json
from typing import Any, Dict, Optional

def sanitize_data(data: Any) -> Any:
    """Recursively convert complex objects to JSON serializable formats."""
    if isinstance(data, dict):
        return {str(k): sanitize_data(v) for k, v in data.items()}
    if isinstance(data, (list, tuple, set)):
        return [sanitize_data(i) for i in data]
    if hasattr(data, '__dict__'):
        return sanitize_data(vars(data))
    return data

def load_json_file(file_path: str) -> Optional[Dict]:
    """Safely load and parse a local JSON configuration file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def format_bytes(size: int) -> str:
    """Human readable string for byte sizes."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} TB"

def flatten_dict(d: Dict, parent_key: str = '', sep: str = '_') -> Dict:
    """Nested dictionary flattening utility for flat storage."""
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)