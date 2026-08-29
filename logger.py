import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

def setup_logger(
    name="automation-tool-96",
    log_dir="logs",
    log_file="app.log",
    max_bytes=5 * 1024 * 1024,  # 5 MB per file
    backup_count=3,
    level=logging.INFO
):
    """Configure logger with rotating file handler and console output."""
    # Ensure log directory exists
    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)
    log_filepath = log_path / log_file
    logger = logging.getLogger(name)
    logger.setLevel(level)
    # Clear existing handlers to prevent duplicate logs
    if logger.hasHandlers():
        logger.handlers.clear()
    # Set up rotating file handler
    file_handler = RotatingFileHandler(
        filename=str(log_filepath),
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8"
    )
    file_handler.setLevel(level)
    # Set up console handler for real-time output
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    # Define log format
    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    # Attach handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger