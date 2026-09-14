import time
import functools
import logging
from typing import Callable, Any

# Configure logging for automation-tool-96
logger = logging.getLogger(__name__)

def retry_operation(retries: int = 3, delay: float = 1.0):
    """Decorator for retrying network operations on failure."""
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    logger.warning(f"Attempt {attempt + 1} failed: {e}")
                    if attempt < retries - 1:
                        time.sleep(delay * (2 ** attempt))  # Exponential backoff
            logger.error(f"Operation failed after {retries} attempts")
            raise last_exception
        return wrapper
    return decorator

@retry_operation(retries=3, delay=0.5)
def fetch_network_data(url: str):
    """Example of a network call decorated for retries."""
    # Simulation of network operation logic
    import random
    if random.random() < 0.7:
        raise ConnectionError("Failed to connect to host")
    return {"status": "success", "url": url}