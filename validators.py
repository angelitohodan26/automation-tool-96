import logging

logger = logging.getLogger(__name__)

class InputValidationError(Exception):
    """Raised when input data fails validation checks."""
    pass

def validate_task_payload(payload: dict) -> bool:
    """
    Validates the structure and data types of an incoming task payload.
    
    Args:
        payload (dict): The task dictionary to validate.
        
    Returns:
        bool: True if validation passes.
        
    Raises:
        InputValidationError: If required fields are missing or invalid.
    """
    if not isinstance(payload, dict):
        logger.error("Payload is not a dictionary: %s", type(payload))
        raise InputValidationError("Payload must be a dictionary")

    required_fields = {"task_id": str, "action": str, "params": dict}
    
    for field, expected_type in required_fields.items():
        if field not in payload:
            logger.error("Missing required field in payload: %s", field)
            raise InputValidationError(f"Missing required field: '{field}'")
            
        if not isinstance(payload[field], expected_type):
            logger.error(
                "Invalid type for field '%s'. Expected %s, got %s",
                field,
                expected_type.__name__,
                type(payload[field]).__name__
            )
            raise InputValidationError(
                f"Field '{field}' must be of type {expected_type.__name__}"
            )

    logger.debug("Payload validation successful for task: %s", payload.get("task_id"))
    return True
