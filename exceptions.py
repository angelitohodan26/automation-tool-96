import time
import functools
import logging

# Configure basic logger for network events
logger = logging.getLogger('automation-tool-96')

def retry_network_operation(max_retries=3, delay=2, backoff=2):
    """
    Decorator to retry network-related functions with exponential backoff.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    if attempt == max_retries - 1:
                        logger.error(f"Final attempt failed: {e}")
                        raise
                    
                    logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {current_delay}s...")
                    time.sleep(current_delay)
                    current_delay *= backoff
            return None
        return wrapper
    return decorator

class NetworkException(Exception):
    """Custom base exception for network operations in automation-tool-96."""
    pass