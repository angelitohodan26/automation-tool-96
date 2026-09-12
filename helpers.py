import time
from datetime import datetime, timezone
from typing import Any, Callable, List, Dict, Optional, TypeVar

T = TypeVar('T')

def retry_operation(
    func: Callable[..., T],
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff_factor: float = 2.0,
    *args: Any,
    **kwargs: Any
) -> Optional[T]:
    """Retry a callable with exponential backoff if exceptions occur."""
    current_delay = delay
    for attempt in range(1, max_attempts + 1):
        try:
            return func(*args, **kwargs)
        except Exception as err:
            if attempt == max_attempts:
                raise err
            time.sleep(current_delay)
            current_delay *= backoff_factor
    return None

def chunk_list(items: List[T], batch_size: int) -> List[List[T]]:
    """Split a list into smaller chunks of specified batch size."""
    if batch_size <= 0:
        raise ValueError("batch_size must be a positive integer")
    return [items[i:i + batch_size] for i in range(0, len(items), batch_size)]

def get_nested_key(data: Dict[str, Any], path: str, default: Any = None) -> Any:
    """Extract a value from a nested dictionary using a dot-separated path."""
    keys = path.split(".")
    current = data
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    return current

def generate_timestamp(fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Generate a current UTC timestamp formatted string."""
    return datetime.now(timezone.utc).strftime(fmt)