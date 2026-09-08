import json
from typing import Any, Dict, Optional

def sanitize_data(data: Any) -> Any:
    """Recursively clean input data for safe processing."""
    if isinstance(data, dict):
        return {str(k): sanitize_data(v) for k, v in data.items()}
    if isinstance(data, list):
        return [sanitize_data(i) for i in data]
    if isinstance(data, (str, int, float, bool)):
        return data
    return str(data)

def load_json_file(file_path: str) -> Dict[str, Any]:
    """Safe file loader for configuration or state data."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def flatten_dict(d: Dict[str, Any], parent_key: str = '', sep: str = '_') -> Dict[str, Any]:
    """Flattens nested dictionary structures for flat data stores."""
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)