import logging
from typing import Any, Dict, List

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def validate_item(item: Dict[str, Any]) -> bool:
    """Validate item payload before processing."""
    if not isinstance(item, dict):
        logging.warning(f"Invalid item format: expected dict, got {type(item).__name__}")
        return False

    required_keys = {"id", "action", "payload"}
    missing_keys = required_keys - item.keys()
    if missing_keys:
        logging.warning(f"Item {item.get('id', 'unknown')} missing required keys: {missing_keys}")
        return False

    if not isinstance(item["id"], (int, str)) or not str(item["id"]).strip():
        logging.warning("Item ID must be a non-empty string or integer")
        return False

    allowed_actions = {"transform", "filter", "export"}
    if item["action"] not in allowed_actions:
        logging.warning(f"Item {item['id']} has unsupported action: {item['action']}")
        return False

    return True


def process_batch(items: List[Dict[str, Any]]) -> Dict[str, int]:
    """Main processing loop with input validation."""
    stats = {"processed": 0, "skipped": 0, "failed": 0}

    for idx, item in enumerate(items):
        if not validate_item(item):
            logging.error(f"Validation failed for item at index {idx}, skipping processing")
            stats["skipped"] += 1
            continue

        try:
            item_id = item["id"]
            action = item["action"]
            logging.info(f"Processing item {item_id} with action '{action}'")

            if action == "transform":
                _ = str(item["payload"]).strip().upper()
            elif action == "filter":
                _ = bool(item["payload"])

            stats["processed"] += 1
        except Exception as exc:
            logging.error(f"Processing error on item {item.get('id')}: {exc}")
            stats["failed"] += 1

    return stats
