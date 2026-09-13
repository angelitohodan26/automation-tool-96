import logging
from typing import Any, Callable, Optional

logger = logging.getLogger(__name__)

def safe_execute(func: Callable, *args: Any, **kwargs: Any) -> Optional[Any]:
    """
    Executes a function with broad error handling for edge cases.
    Returns the result if successful, or None if an error occurs.
    """
    try:
        return func(*args, **kwargs)
    except (ValueError, TypeError) as e:
        logger.error(f"Invalid data input: {e}")
    except PermissionError as e:
        logger.error(f"Insufficient system permissions: {e}")
    except Exception as e:
        logger.critical(f"Unexpected automation failure: {e}")
    return None

def validate_input(data: Any, expected_type: type) -> bool:
    """
    Verifies that the provided input is not null and matches type.
    """
    if data is None:
        logger.warning("Input validation failed: received None")
        return False
    if not isinstance(data, expected_type):
        logger.warning(f"Input validation failed: expected {expected_type}, got {type(data)}")
        return False
    return True

def retry_operation(func: Callable, retries: int = 3, *args: Any, **kwargs: Any) -> Any:
    """
    Attempt to execute an operation multiple times on transient failures.
    """
    last_exception = None
    for attempt in range(retries):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            last_exception = e
            logger.info(f"Retry {attempt + 1}/{retries} due to {e}")
    raise last_exception if last_exception else RuntimeError("Operation failed")