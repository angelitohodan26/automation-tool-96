import json
from typing import Any, Optional

def clean_payload(data: Any) -> Any:
    """
    Recursively strips whitespace from string values in nested dictionaries.
    """
    if isinstance(data, dict):
        return {k: clean_payload(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [clean_payload(i) for i in data]
    elif isinstance(data, str):
        return data.strip()
    return data

def safe_load_json(json_str: str) -> Optional[dict]:
    """
    Attempts to parse a JSON string and returns None on failure.
    """
    try:
        return json.loads(json_str)
    except (json.JSONDecodeError, TypeError):
        return None

def format_data_for_export(data: dict, indent: int = 4) -> str:
    """
    Serializes data to a formatted JSON string.
    """
    try:
        return json.dumps(data, indent=indent, sort_keys=True)
    except (TypeError, ValueError) as e:
        return f"Serialization error: {e}"

def validate_schema(data: dict, required_keys: list) -> bool:
    """
    Checks if all required keys exist in the provided dictionary.
    """
    if not isinstance(data, dict):
        return False
    return all(key in data for key in required_keys)