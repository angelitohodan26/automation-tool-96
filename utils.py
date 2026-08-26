import logging
import sys
from typing import Any, Callable, TypeVar

logger = logging.getLogger("automation-tool-96")
T = TypeVar('T')

def safe_execute(func: Callable[..., T], *args: Any, **kwargs: Any) -> T | None:
    """Execute a function with robust error handling for edge cases."""
    try:
        return func(*args, **kwargs)
    except ValueError as val_err:
        logger.error(f"Invalid value encountered in {func.__name__}: {val_err}")
    except TypeError as type_err:
        logger.error(f"Type mismatch in {func.__name__}: {type_err}")
    except ZeroDivisionError:
        logger.error(f"Mathematical error (division by zero) in {func.__name__}")
    except Exception as exc:
        logger.critical(f"Unexpected error in {func.__name__}: {exc}", exc_info=True)
        raise
    return None

def validate_payload(data: dict[str, Any] | None) -> bool:
    """Ensure payload is not None and contains necessary structure."""
    if data is None:
        logger.warning("Payload validation failed: data is None")
        return False
    if not isinstance(data, dict):
        logger.warning(f"Payload validation failed: expected dict, got {type(data).__name__}")
        return False
    if not data:
        logger.warning("Payload validation failed: dictionary is empty")
        return False
    return True
