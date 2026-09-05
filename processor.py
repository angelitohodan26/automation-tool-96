import re
from typing import List, Dict, Any, Optional

class DataProcessor:
    """Processes and normalizes raw dataset records for downstream automation tasks."""

    def __init__(self, default_value: Optional[Any] = None):
        self.default_value = default_value
        # Compile regex pattern to strip non-alphanumeric characters
        self._clean_pattern = re.compile(r'[^\w\s\-\.\,]')

    def clean_string(self, value: str) -> str:
        """Removes unwanted special characters and normalizes whitespace."""
        if not isinstance(value, str):
            return str(value)
        # Remove special characters except common punctuation
        cleaned = self._clean_pattern.sub("", value)
        # Collapse multiple whitespaces into a single space and strip
        return " ".join(cleaned.split())

    def process_record(self, record: Dict[str, Any], fields_to_clean: List[str]) -> Dict[str, Any]:
        """Cleans specified string fields within a single record dict."""
        processed = record.copy()
        for key, val in processed.items():
            if key in fields_to_clean and isinstance(val, str):
                processed[key] = self.clean_string(val)
        return processed

    def batch_process(self, records: List[Dict[str, Any]], target_fields: List[str]) -> List[Dict[str, Any]]:
        """Filters out invalid records and cleans target fields in batch."""
        results = []
        for record in records:
            if not isinstance(record, dict):
                continue
            cleaned_record = self.process_record(record, target_fields)
            results.append(cleaned_record)
        return results
