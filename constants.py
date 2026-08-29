import os
from enum import Enum

# Centralized constants for automation-tool-96
# Reorganized from scattered definitions during cleanup

DEFAULT_CONFIG_FILE = "config.yaml"
LOG_FILE_NAME = "automation.log"
MAX_WORKERS = 4
TIMEOUT_SECONDS = 60
RETRY_ATTEMPTS = 3
BATCH_SIZE = 100

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
LOGS_DIR = os.path.join(BASE_DIR, "logs")
TEMP_DIR = os.path.join(BASE_DIR, "temp")

class TaskType(Enum):
    BACKUP = "backup"
    DATA_SYNC = "sync"
    FILE_CLEANUP = "cleanup"
    GENERATE_REPORT = "report"

class OperationStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

DEFAULT_CONFIG = {
    "max_workers": MAX_WORKERS,
    "timeout": TIMEOUT_SECONDS,
    "retries": RETRY_ATTEMPTS,
    "batch_size": BATCH_SIZE,
    "log_level": "INFO",
}

ENV_VAR_PREFIX = "AUTO_"
ENV_CONFIG = ENV_VAR_PREFIX + "CONFIG"
ENV_LOG_LEVEL = ENV_VAR_PREFIX + "LOG_LEVEL"

SUPPORTED_EXTENSIONS = {".txt", ".csv", ".json", ".yaml", ".log"}

ERROR_CODES = {
    100: "Configuration error",
    200: "File operation error",
    300: "Network error",
    400: "Permission error",
}

def load_from_env():
    """Load overrides from environment"""
    config = DEFAULT_CONFIG.copy()
    log_level = os.environ.get(ENV_LOG_LEVEL)
    if log_level:
        config["log_level"] = log_level
    return config

def get_task_type(value):
    """Convert string to TaskType if valid"""
    try:
        return TaskType(value)
    except ValueError:
        return None