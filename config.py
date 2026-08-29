import json
import os
from typing import Any, Dict, Optional

DEFAULTS = {
    "max_retries": 5,
    "timeout_seconds": 60,
    "enable_logging": True,
    "log_file": "automation.log",
    "batch_size": 100,
    "debug_mode": False,
}


class ConfigLoader:
    """Loads configuration by merging defaults with user-provided settings."""

    def __init__(self, defaults: Optional[Dict[str, Any]] = None) -> None:
        self.defaults = defaults or DEFAULTS.copy()
        self.config: Dict[str, Any] = self.defaults.copy()

    def load_from_file(self, filepath: str) -> Dict[str, Any]:
        """Load and merge configuration from a JSON file."""
        if os.path.exists(filepath):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    user_config = json.load(f)
                if isinstance(user_config, dict):
                    self.config.update(user_config)
            except (json.JSONDecodeError, IOError, OSError) as e:
                print(f"Warning: Failed to load {filepath}: {e}")
        return self.config

    def override_from_env(self, prefix: str = "AUTOMATION_") -> Dict[str, Any]:
        """Override values using environment variables."""
        for key, value in list(self.config.items()):
            env_key = f"{prefix}{key.upper()}"
            if env_key in os.environ:
                env_value = os.environ[env_key]
                orig_type = type(value)
                if orig_type is bool:
                    self.config[key] = env_value.lower() in ("true", "1", "yes")
                elif orig_type is int:
                    try:
                        self.config[key] = int(env_value)
                    except ValueError:
                        pass
                elif orig_type is float:
                    try:
                        self.config[key] = float(env_value)
                    except ValueError:
                        pass
                else:
                    self.config[key] = env_value
        return self.config

    def get(self, key: str, default: Any = None) -> Any:
        """Retrieve a configuration value or default."""
        return self.config.get(key, default)

    def get_all(self) -> Dict[str, Any]:
        """Return a copy of the current configuration."""
        return self.config.copy()
