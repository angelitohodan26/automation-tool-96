import json
import os
from typing import Any, Dict, Optional

class ConfigurationLoader:
    """Loads configuration with support for defaults and file overrides."""

    def __init__(self, default_config: Optional[Dict[str, Any]] = None) -> None:
        """Initialize with optional default configuration."""
        self.default_config: Dict[str, Any] = default_config or {}
        self.config: Dict[str, Any] = self.default_config.copy()

    def load_from_file(self, filepath: str) -> Dict[str, Any]:
        """Load configuration from a JSON file and merge with defaults."""
        if not os.path.isfile(filepath):
            return self.config

        try:
            with open(filepath, 'r', encoding='utf-8') as config_file:
                file_config: Dict[str, Any] = json.load(config_file)
            if isinstance(file_config, dict):
                self.config.update(file_config)

        except (json.JSONDecodeError, IOError, OSError) as error:
            print(f"Warning: Could not load config from {filepath}: {error}")

        return self.config

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value, falling back to defaults if needed."""
        return self.config.get(key, default)

    def get_all(self) -> Dict[str, Any]:
        """Return the full configuration dictionary."""
        return self.config.copy()

    def set_default(self, key: str, value: Any) -> None:
        """Set or update a default value."""
        self.default_config[key] = value
        if key not in self.config:
            self.config[key] = value
