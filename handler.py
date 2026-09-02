"""General data handling utilities."""

import json
from typing import Any, Dict, List, Union

def flatten_dict(d: Dict[str, Any], parent_key: str = '', sep: str = '.') -> Dict[str, Any]:
    """Flatten a nested dictionary. Handles dicts and lists."""
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            for i, item in enumerate(v):
                if isinstance(item, dict):
                    items.extend(flatten_dict(item, f"{new_key}[{i}]", sep=sep).items())
                else:
                    items.append((f"{new_key}[{i}]", item))
        else:
            items.append((new_key, v))
    return dict(items)

def unflatten_dict(flat_dict: Dict[str, Any], sep: str = '.') -> Dict[str, Any]:
    """Unflatten a dictionary to nested structure."""
    result = {}
    for key, value in flat_dict.items():
        parts = key.split(sep)
        current = result
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
        current[parts[-1]] = value
    return result

def clean_data(data: Any) -> Any:
    """Remove None and empty strings from data structures."""
    if isinstance(data, dict):
        return {k: clean_data(v) for k, v in data.items() if v is not None and v != ""}
    elif isinstance(data, list):
        return [clean_data(item) for item in data if item is not None and item != ""]
    return data

def handle_data(data: Union[Dict[str, Any], List[Any], str], operation: str = 'flatten', **kwargs) -> Any:
    """Utility function for general data handling.
    Available operations: flatten, unflatten, clean, to_json.
    """
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except (json.JSONDecodeError, TypeError):
            pass
    if operation == 'flatten' and isinstance(data, dict):
        return flatten_dict(data, **kwargs)
    elif operation == 'flatten' and isinstance(data, list):
        return [flatten_dict(d) if isinstance(d, dict) else d for d in data]
    elif operation == 'unflatten' and isinstance(data, dict):
        return unflatten_dict(data, **kwargs)
    elif operation == 'clean':
        return clean_data(data)
    elif operation == 'to_json':
        return json.dumps(data, indent=2)
    return data