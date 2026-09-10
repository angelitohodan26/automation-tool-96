class AutomationError(Exception):
    """Base exception for all automation-tool-96 errors."""
    pass

class ConfigurationError(AutomationError):
    """Raised when config files are missing or malformed."""
    pass

class ProcessingError(AutomationError):
    """Raised when core logic fails during execution."""
    pass

class ValidationError(AutomationError):
    """Raised when input data fails validation checks."""
    pass

def handle_exception(e: Exception) -> str:
    """Format exception details for standardized logging."""
    if isinstance(e, AutomationError):
        return f"[{type(e).__name__}]: {str(e)}"
    return f"[UnexpectedError]: {str(e)}"

def raise_if_none(value, name: str):
    """Helper to ensure required fields are not empty."""
    if value is None:
        raise ValidationError(f"Field '{name}' cannot be None")

def validate_path(path: str):
    """Verify file system path existence for safety."""
    import os
    if not os.path.exists(path):
        raise ConfigurationError(f"Path not found: {path}")