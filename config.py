import json
import os
from typing import Any, Dict, Optional

class Config:
    """Configuration handler with defaults."""

    def __init__(self, default_config: Optional[Dict[str, Any]] = None) -> None:
        self._config: Dict[str, Any] = {}
        self._defaults: Dict[str, Any] = default_config or {}

    def load_from_file(self, filepath: str) -> None:
        """Load configuration from a JSON file, merging with defaults."""

        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                file_config = json.load(file)
            self._config = {**self._defaults, **file_config}
        except FileNotFoundError:
            self._config = self._defaults.copy()
        except json.JSONDecodeError:
            self._config = self._defaults.copy()

    def load_from_env(self, prefix: str = "APP_") -> None:
        """Load additional config from environment variables."""

        for key, value in os.environ.items():
            if key.startswith(prefix):
                config_key = key[len(prefix):].lower()
                self._config[config_key] = value

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """Get a config value, falling back to provided default."""

        return self._config.get(key, default)

    def get_all(self) -> Dict[str, Any]:
        """Return the entire configuration dictionary."""

        return self._config.copy()

    def set(self, key: str, value: Any) -> None:
        """Set a configuration value."""

        self._config[key] = value

# Example usage for testing
if __name__ == "__main__":
    defaults = {
        "debug": False,
        "port": 8080,
        "host": "localhost"
    }
    config = Config(defaults)
    config.load_from_file("config.json")
    config.load_from_env()
    print(config.get("port"))
    print(config.get_all())
