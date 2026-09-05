import functools
import time
import logging
from typing import Callable, Any

# configure logging for performance metrics
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('core-performance')

# thread-safe lru cache for repetitive calculations
CACHE_SIZE = 128

def memoize_performance(func: Callable) -> Callable:
    """decorator for caching expensive computation results."""
    @functools.lru_cache(maxsize=CACHE_SIZE)
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

class DataProcessor:
    def __init__(self):
        self.metrics = {}

    @memoize_performance
    def transform_dataset(self, data_hash: int, raw_data: tuple) -> list:
        """optimizes data processing using cached state."""
        start_time = time.perf_counter()
        
        # simulate complex transformation logic
        processed = [x * 2 for x in raw_data]
        
        duration = time.perf_counter() - start_time
        self.metrics[data_hash] = duration
        return processed

    def clear_cache(self):
        """resets cache to free up memory."""
        self.transform_dataset.cache_clear()
        logger.info("cache cleared successfully")