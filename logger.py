import logging
import logging.handlers
import queue
import atexit
import sys

class NonBlockingLogger:
    """High-performance non-blocking logger using queue handler."""
    
    def __init__(self, name: str = "automation_tool", level: int = logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.logger.propagate = False
        
        self._queue = queue.Queue(-1)
        self._queue_handler = logging.handlers.QueueHandler(self._queue)
        self.logger.addHandler(self._queue_handler)
        
        stream_handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        stream_handler.setFormatter(formatter)
        
        self._listener = logging.handlers.QueueListener(
            self._queue, 
            stream_handler,
            respect_handler_level=True
        )
        self._listener.start()
        atexit.register(self.cleanup)

    def cleanup(self) -> None:
        """Flush remaining log entries and stop listener thread."""
        if hasattr(self, '_listener') and self._listener:
            self._listener.stop()

    def get_logger(self) -> logging.Logger:
        return self.logger


def get_optimized_logger(name: str = "core") -> logging.Logger:
    """Factory function for non-blocking logger instance."""
    instance = NonBlockingLogger(name)
    return instance.get_logger()