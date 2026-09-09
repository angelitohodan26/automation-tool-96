import json
import os
from pathlib import Path
from typing import Any, Dict, Optional

DEFAULT_CONFIG: Dict[str, Any] = {
    "app_name": "automation-tool-96",
    "version": "1.0.0",
    "debug": False,
    "log_level": "INFO",
    "max_retries": 3,
    "timeout": 30,
    "storage": {
        "path": "./data",
        "auto_clean": True
    }
}


class ConfigLoader:
    """Manages application configuration loading with default fallbacks."""

    def __init__(self, config_path: Optional[str] = None):
        self.config_path = Path(config_path) if config_path else None
        self._config: Dict[str, Any] = {}
        self.load()

    def _merge_dicts(self, base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        """Recursively merge user overrides into default configuration."""
        merged = base.copy()
        for key, value in override.items():
            if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
                merged[key] = self._merge_dicts(merged[key], value)
            else:
                merged[key] = value
        return merged

    def load(self) -> Dict[str, Any]:
        """Load configuration from file and environment variables."""
        config = DEFAULT_CONFIG.copy()

        if self.config_path and self.config_path.exists():
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    file_config = json.load(f)
                    config = self._merge_dicts(config, file_config)
            except (json.JSONDecodeError, IOError) as err:
                raise RuntimeError(f"Failed to load config file {self.config_path}: {err}")

        # Override debug flag if environment variable is present
        env_debug = os.getenv("AUTOMATION_DEBUG")
        if env_debug is not None:
            config["debug"] = env_debug.lower() in ("true", "1", "yes")

        self._config = config
        return self._config

    def get(self, key_path: str, default: Any = None) -> Any:
        """Retrieve value using dot-notation path (e.g. 'storage.path')."""
        keys = key_path.split(".")
        curr = self._config
        for k in keys:
            if isinstance(curr, dict) and k in curr:
                curr = curr[k]
            else:
                return default
        return curr


def load_config(file_path: Optional[str] = None) -> ConfigLoader:
    """Helper function to initialize configuration loader."""
    return ConfigLoader(file_path)
