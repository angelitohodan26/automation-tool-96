import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logger(name='automation-tool-96', log_file='app.log', level=logging.INFO):
    """Configures a rotating file logger for system tracking."""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Prevent duplicate handlers if function is called multiple times
    if not logger.handlers:
        # Format: timestamp - name - level - message
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        # 5MB max per file, keep 3 backup files
        handler = RotatingFileHandler(
            log_file, 
            maxBytes=5*1024*1024, 
            backupCount=3
        )
        handler.setFormatter(formatter)
        
        # Add console output as well for immediate visibility
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        logger.addHandler(handler)
        logger.addHandler(console_handler)

    return logger

# Instance for global application usage
logger = setup_logger()