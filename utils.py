import time
import functools
import logging

logger = logging.getLogger("automation_tool_96")

def retry(retries: int = 3, delay: float = 1.0, backoff: float = 2.0, exceptions: tuple = (Exception,)):
    """
    A decorator that retries a function upon encountering specified exceptions.
    Uses exponential backoff for spacing out consecutive retries.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            for attempt in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == retries:
                        logger.error(
                            f"Function '{func.__name__}' failed after {retries} attempts. Error: {e}"
                        )
                        raise
                    
                    logger.warning(
                        f"Attempt {attempt} failed for '{func.__name__}': {e}. "
                        f"Retrying in {current_delay:.1f}s..."
                    )
                    time.sleep(current_delay)
                    current_delay *= backoff
            return None
        return wrapper
    return decorator
