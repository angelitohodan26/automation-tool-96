import json
import os
from typing import List, Dict, Any

def load_json_data(file_path: str) -> List[Dict[str, Any]]:
    """Load data from a JSON file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    if not isinstance(data, list):
        data = [data]
    return data

def filter_data(data: List[Dict[str, Any]], key: str, value: Any) -> List[Dict[str, Any]]:
    """Filter data by key and value."""
    return [item for item in data if item.get(key) == value]

def transform_data(data: List[Dict[str, Any]], transform_func) -> List[Dict[str, Any]]:
    """Apply a transformation function to each item."""
    return [transform_func(item) for item in data]

def save_to_json(data: List[Dict[str, Any]], file_path: str) -> None:
    """Save data to a JSON file."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

def chunk_data(data: List[Any], chunk_size: int) -> List[List[Any]]:
    """Split data into chunks of specified size."""
    return [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]