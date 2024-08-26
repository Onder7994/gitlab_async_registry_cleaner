"""config reader module."""

import json
import sys
from typing import Any
from gitlab_registry_async_cleaner.logger.logger import Logging

logger = Logging(__name__)


def read_json_config(json_config_path: str) -> Any:
    """Read json config."""
    if json_config_path:
        try:
            with open(json_config_path, encoding="utf-8") as file:
                json_config = json.load(file)
            return json_config
        except FileNotFoundError:
            logger.error("File %s not found.", json_config_path)
            sys.exit(1)
    else:
        logger.error("Argument --config is empty.")
        return None
