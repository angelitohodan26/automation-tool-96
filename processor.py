import json
from typing import Any, Dict, List, Optional


def clean_record(record: Dict[str, Any]) -> Dict[str, Any]:
    """Remove keys with null values and strip string whitespace."""
    cleaned = {}
    for key, value in record.items():
        if value is None:
            continue
        if isinstance(value, str):
            cleaned[key] = value.strip()
        elif isinstance(value, dict):
            cleaned[key] = clean_record(value)
        else:
            cleaned[key] = value
    return cleaned


def batch_process_data(raw_data: List[Dict[str, Any]], batch_size: int = 100) -> List[Dict[str, Any]]:
    """Process raw data in batches, cleaning each record."""
    if batch_size <= 0:
        raise ValueError("Batch size must be greater than zero")
    
    processed_results = []
    for i in range(0, len(raw_data), batch_size):
        batch = raw_data[i:i + batch_size]
        for item in batch:
            try:
                processed_results.append(clean_record(item))
            except Exception as e:
                # Skip malformed records during batch processing
                continue
                
    return processed_results


def export_to_json(data: List[Dict[str, Any]], file_path: str) -> None:
    """Serialize processed data directly to a JSON file."""
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, sort_keys=True)
