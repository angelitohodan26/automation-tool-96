import time
import random
import logging
from typing import Callable, TypeVar

T = TypeVar('T')
logger = logging.getLogger(__name__)

def retry_operation(
    func: Callable[[], T],
    max_retries: int = 3,
    initial_delay: float = 1.0,
    backoff_factor: float = 2.0,
    exceptions: tuple = (Exception,)
) -> T:
    """
    Retries a function call with exponential backoff.
    """
    delay = initial_delay
    for attempt in range(1, max_retries + 1):
        try:
            return func()
        except exceptions as e:
            if attempt == max_retries:
                logger.error(f"Failed after {max_retries} attempts: {e}")
                raise e
            
            jitter = random.uniform(0, 0.1 * delay)
            sleep_time = delay + jitter
            logger.warning(
                f"Attempt {attempt} failed: {e}. Retrying in {sleep_time:.2f} seconds..."
            )
            time.sleep(sleep_time)
            delay *= backoff_factor