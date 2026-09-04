import time
import functools
import logging

logger = logging.getLogger(__name__)

def retry(max_attempts=3, delay=2, backoff=2, exceptions=(Exception,)): 
    """Decorator to implement exponential backoff retry logic."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            current_delay = delay
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    attempts += 1
                    if attempts >= max_attempts:
                        logger.error(f"Failed after {max_attempts} attempts: {e}")
                        raise
                    
                    logger.warning(f"Attempt {attempts} failed, retrying in {current_delay}s...")
                    time.sleep(current_delay)
                    current_delay *= backoff
        return wrapper
    return decorator

@retry(max_attempts=3, delay=1)
def fetch_network_resource(url):
    """Example network operation function."""
    # Simulation of a network call
    print(f"Fetching from {url}...")
    raise ConnectionError("Server unreachable")

if __name__ == "__main__":
    try:
        fetch_network_resource("https://api.example.com")
    except Exception:
        print("Operation exhausted all retries.")