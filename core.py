import json
import logging
from typing import Any, Dict, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AutomationError(Exception):
    """Custom exception for automation tool failures."""
    pass

def process_payload(raw_data: Optional[str]) -> Dict[str, Any]:
    """Process and validate incoming automation payload with edge case handling."""
    if raw_data is None:
        logger.warning("Received null payload")
        raise AutomationError("Payload cannot be None")
    
    if not isinstance(raw_data, str):
        logger.error("Invalid payload type: %s", type(raw_data))
        raise TypeError("Payload must be a string representation of JSON")
    
    stripped_data = raw_data.strip()
    if not stripped_data:
        logger.warning("Received empty payload string")
        return {"status": "empty", "data": {}}
    
    try:
        parsed_data = json.loads(stripped_data)
    except json.JSONDecodeError as exc:
        logger.exception("Failed to parse JSON payload")
        raise AutomationError(f"Malformed JSON input: {exc}") from exc
    
    if not isinstance(parsed_data, dict):
        logger.error("Parsed payload is not a dictionary: %s", type(parsed_data))
        raise AutomationError("Root JSON structure must be an object/dictionary")
    
    logger.info("Payload successfully processed and validated")
    return {"status": "success", "data": parsed_data}