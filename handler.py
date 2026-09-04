import logging
from typing import Dict, Any, Optional

# Configure structured logging for automation flow
logger = logging.getLogger('automation-tool-96')

class AutomationHandler:
    """Manages execution tasks and state persistence."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.task_registry = {}

    def register_task(self, name: str, task_func: callable) -> None:
        """Register a task for later execution."""
        if name not in self.task_registry:
            self.task_registry[name] = task_func
            logger.debug(f"Task {name} registered successfully")

    def execute(self, task_name: str, *args, **kwargs) -> Optional[Any]:
        """Run a registered task with error handling."""
        task = self.task_registry.get(task_name)
        if not task:
            logger.error(f"Task {task_name} not found")
            return None
        
        try:
            return task(*args, **kwargs)
        except Exception as e:
            logger.error(f"Task {task_name} failed: {str(e)}")
            raise

    def cleanup(self) -> None:
        """Clear internal state and task registry."""
        self.task_registry.clear()
        logger.info("Handler resources released")