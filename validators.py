import re
import os

def is_valid_email(email: str) -> bool:
    """Validate email address format using regex."""
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(pattern, email))

def is_valid_file_path(path: str) -> bool:
    """Verify file exists and is accessible."""
    return os.path.isfile(path) and os.access(path, os.R_OK)

def sanitize_input(value: str) -> str:
    """Strip whitespace and prevent basic injection characters."""
    if not isinstance(value, str):
        return ""
    cleaned = value.strip()
    return re.sub(r'[;<>"\\'&]', '', cleaned)

def validate_numeric_range(value: int, min_val: int, max_val: int) -> bool:
    """Check if integer falls within specific bounds."""
    return min_val <= value <= max_val

def is_empty_string(value: str) -> bool:
    """Check if string is null or whitespace only."""
    return not (value and value.strip())