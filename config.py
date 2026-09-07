import os
import logging
from typing import Any, Optional

logger = logging.getLogger(__name__)

class ConfigError(Exception):
    """Custom exception for configuration failures."""
    pass

def get_env_variable(key: str, default: Optional[Any] = None) -> Any:
    """Retrieves environment variables with validation and fallback."""
    try:
        value = os.getenv(key)
        if value is None:
            if default is not None:
                return default
            raise ConfigError(f"Missing required environment variable: {key}")
        return value
    except Exception as e:
        logger.error(f"Unexpected error retrieving config {key}: {str(e)}")
        raise ConfigError(f"Failed to load config for {key}") from e

def load_app_settings() -> dict:
    """Safely loads application configuration settings."""
    try:
        return {
            "api_key": get_env_variable("API_KEY"),
            "timeout": int(get_env_variable("TIMEOUT", 30)),
            "debug": get_env_variable("DEBUG", "false").lower() == "true"
        }
    except (ValueError, TypeError) as e:
        logger.error(f"Invalid configuration format: {e}")
        return {"api_key": None, "timeout": 30, "debug": False}
    except ConfigError as e:
        logger.critical(f"Application startup aborted: {e}")
        raise