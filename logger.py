import logging
import sys
from logging.handlers import RotatingFileHandler

def setup_logger(name: str = 'automation-tool-96', log_file: str = 'app.log') -> logging.Logger:
    """Configures a standard logging instance with rotating file support."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Console handler for terminal output
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Rotating file handler to manage disk space
    file_handler = RotatingFileHandler(
        log_file, maxBytes=1048576, backupCount=3
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

# Instantiate default logger for general usage
app_logger = setup_logger()