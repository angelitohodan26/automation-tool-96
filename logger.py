import logging
import sys
from typing import Optional

class AutomationLogger:
    """Standardized logging utility for automation-tool-96."""

    def __init__(self, name: str = "automation-tool"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def safe_log_execution(self, func, *args, **kwargs) -> Optional[any]:
        """Executes a function with error catching and logging."""
        try:
            return func(*args, **kwargs)
        except (ValueError, TypeError) as e:
            self.logger.error(f"Invalid input provided: {e}")
            return None
        except ConnectionError as e:
            self.logger.critical(f"Network failure during execution: {e}")
            raise
        except Exception as e:
            self.logger.exception(f"Unexpected system failure: {e}")
            return None

    def log_event(self, message: str, level: str = "info"):
        """Routes messages to appropriate log levels."""
        levels = {
            "info": self.logger.info,
            "warning": self.logger.warning,
            "error": self.logger.error
        }
        log_func = levels.get(level.lower(), self.logger.info)
        log_func(message)