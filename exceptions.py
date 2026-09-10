"""Custom exception classes and error handling utilities for automation-tool-96."""

from typing import Optional, Dict, Any


class AutomationError(Exception):
    """Base exception class for all automation workflow errors."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}

    def to_dict(self) -> Dict[str, Any]:
        """Serialize exception information into a dictionary format."""
        return {
            "error_type": self.__class__.__name__,
            "message": self.message,
            "details": self.details,
        }


class TaskTimeoutError(AutomationError):
    """Raised when an automated task exceeds its allocated execution time."""

    def __init__(self, task_name: str, timeout_seconds: float):
        message = f"Task '{task_name}' timed out after {timeout_seconds}s"
        super().__init__(message, {"task_name": task_name, "timeout_seconds": timeout_seconds})


class ResourceUnavailableError(AutomationError):
    """Raised when a required system resource or service is missing."""

    def __init__(self, resource_id: str, reason: str = "Not accessible"):
        message = f"Resource '{resource_id}' is unavailable: {reason}"
        super().__init__(message, {"resource_id": resource_id, "reason": reason})


class InvalidPayloadError(AutomationError):
    """Raised when task input data fails validation or structural checks."""

    def __init__(self, payload_key: str, expected_type: str, actual_value: Any):
        actual_type = type(actual_value).__name__
        message = f"Invalid payload key '{payload_key}': expected {expected_type}, got {actual_type}"
        super().__init__(
            message,
            {
                "payload_key": payload_key,
                "expected_type": expected_type,
                "actual_value": str(actual_value),
            },
        )


def format_edge_case_error(exc: Exception) -> Dict[str, Any]:
    """Convert arbitrary exceptions into structured error payloads."""
    if isinstance(exc, AutomationError):
        return exc.to_dict()
    return {
        "error_type": "UnhandledEdgeCaseError",
        "message": str(exc) or "An unexpected runtime error occurred",
        "details": {"raw_type": type(exc).__name__},
    }
