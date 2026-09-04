import json
from typing import Any, Dict, List, Optional, Generator


def batch_iterable(items: List[Any], batch_size: int) -> Generator[List[Any], None, None]:
    """Yield successive n-sized batches from an iterable list."""
    if batch_size <= 0:
        raise ValueError("Batch size must be greater than zero.")
    for i in range(0, len(items), batch_size):
        yield items[i : i + batch_size]


def sanitize_keys(data: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize dictionary keys by stripping whitespace and converting to lowercase."""
    cleaned = {}
    for key, value in data.items():
        new_key = str(key).strip().lower().replace(" ", "_")
        if isinstance(value, dict):
            cleaned[new_key] = sanitize_keys(value)
        else:
            cleaned[new_key] = value
    return cleaned


def safe_json_parse(json_str: str, default: Optional[Any] = None) -> Any:
    """Attempt to parse a JSON string, returning a default value on failure."""
    try:
        return json.loads(json_str)
    except (json.JSONDecodeError, TypeError):
        return default
