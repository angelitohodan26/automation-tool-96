from typing import List, Dict, Any, Optional
import json
import os

def load_json_config(file_path: str) -> Dict[str, Any]:
    """Loads a JSON configuration file from the filesystem.

    Args:
        file_path: The path to the JSON file.

    Returns:
        A dictionary containing the configuration data.
    """
    if not os.path.exists(file_path):
        return {}
    
    with open(file_path, 'r', encoding='utf-8') as f:
        return dict(json.load(f))

def format_payload(data: List[Any], prefix: Optional[str] = None) -> str:
    """Formats a list of data into a string with an optional prefix.

    Args:
        data: A list of items to be stringified.
        prefix: An optional string to prepend to the result.

    Returns:
        A formatted string representation.
    """
    items: List[str] = [str(item) for item in data]
    content: str = ", ".join(items)
    return f"{prefix}: {content}" if prefix else content

def validate_environment_keys(required_keys: List[str]) -> bool:
    """Checks if all required environment variables are present.

    Args:
        required_keys: A list of environment variable names.

    Returns:
        True if all keys are present, False otherwise.
    """
    return all(key in os.environ for key in required_keys)