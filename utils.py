import time
import random
import logging
from typing import Callable, Any, Type

logger = logging.getLogger(__name__)

def retry_network_operation(
    func: Callable, 
    max_retries: int = 3, 
    backoff_factor: float = 1.0,
    exceptions: tuple[Type[Exception], ...] = (Exception,)
) -> Any:
    """Executes a callable with exponential backoff strategy."""
    last_exception = None
    
    for attempt in range(max_retries):
        try:
            return func()
        except exceptions as e:
            last_exception = e
            wait_time = backoff_factor * (2 ** attempt) + random.uniform(0, 0.1)
            
            logger.warning(
                f"Attempt {attempt + 1} failed: {e}. Retrying in {wait_time:.2f}s..."
            )
            
            if attempt < max_retries - 1:
                time.sleep(wait_time)
            else:
                break
                
    logger.error(f"Operation failed after {max_retries} attempts.")
    raise last_exception