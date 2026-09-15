import os
import re
import time
from typing import Any, Dict, Optional, Callable


def safe_get_nested(data: Dict[str, Any], path: str, default: Any = None) -> Any:
    """Safely retrieve a nested value from a dictionary using a dot-separated path."""
    keys = path.split(".")
    current = data
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    return current


def slugify(text: str) -> str:
    """Convert a string to a clean, URL/filename-friendly lowercase slug."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s-]+", "-", text)
    return text.strip("-")


def ensure_directory(file_path: str) -> None:
    """Ensure that the parent directory for a given file path exists."""
    directory = os.path.dirname(file_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)


def time_execution(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator to measure and print the execution time of a function."""

    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        duration = end_time - start_time
        print(f"[Timer] '{func.__name__}' executed in {duration:.4f} seconds")
        return result

    return wrapper
