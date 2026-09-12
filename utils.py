import time
import functools
import logging
from typing import Callable, Any

# Configure logger for automation-tool-96
logger = logging.getLogger(__name__)

def retry_operation(max_attempts: int = 3, delay: float = 1.0):
    """Decorator for retrying network operations with exponential backoff."""
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None
            current_delay = delay
            
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    logger.warning(f"Attempt {attempt} failed: {e}. Retrying...")
                    if attempt < max_attempts:
                        time.sleep(current_delay)
                        current_delay *= 2
            
            logger.error(f"Operation failed after {max_attempts} attempts.")
            raise last_exception
        return wrapper
    return decorator

# Example usage helper for network calls
@retry_operation(max_attempts=3, delay=2.0)
def safe_network_request(request_func: Callable, *args, **kwargs) -> Any:
    """Execute network request function with built-in retry logic."""
    return request_func(*args, **kwargs)