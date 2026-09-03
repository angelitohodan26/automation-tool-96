import functools
import time
from typing import Any, Callable, Dict, Tuple

class PerformanceCache:
    """A high-performance in-memory cache with Time-To-Live (TTL) support."""
    
    def __init__(self, default_ttl: float = 300.0):
        self.default_ttl = default_ttl
        self._cache: Dict[Any, Tuple[Any, float]] = {}

    def get(self, key: Any) -> Any:
        """Retrieve an item from the cache if it has not expired."""
        if key not in self._cache:
            return None
        value, expiry = self._cache[key]
        if time.time() > expiry:
            del self._cache[key]
            return None
        return value

    def set(self, key: Any, value: Any, ttl: float = None) -> None:
        """Store an item in the cache with an optional TTL."""
        duration = ttl if ttl is not None else self.default_ttl
        expiry = time.time() + duration
        self._cache[key] = (value, expiry)

    def clear(self) -> None:
        """Clear all cached items."""
        self._cache.clear()

def memoize(ttl: float = 300.0):
    """Decorator to cache function results with TTL."""
    cache = PerformanceCache(default_ttl=ttl)
    
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
            cached_result = cache.get(key)
            if cached_result is not None:
                return cached_result
            result = func(*args, **kwargs)
            cache.set(key, result)
            return result
        return wrapper
    return decorator