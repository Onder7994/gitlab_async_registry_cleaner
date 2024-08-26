"""Logger module."""

import logging
import json


class JSONFormatter(logging.Formatter):
    """Custom json formatter"""

    def __init__(self):
        """Override class."""
        super().__init__()

    def format(self, record):
        """Custom log format."""
        log_record = {
            "module": record.name,
            "asctime": self.formatTime(record, self.datefmt),
            "levelname": record.levelname,
            "message": record.getMessage(),
        }
        if hasattr(record, "operation"):
            log_record["operation"] = record.operation
        if hasattr(record, "tag_name"):
            log_record["tag_name"] = record.tag_name
        if hasattr(record, "tag_location"):
            log_record["tag_location"] = record.tag_location
        return json.dumps(log_record, ensure_ascii=False)


class Logging:
    """Init logger class."""

    def __init__(self, logger_name: str):
        """Constructor."""
        self.logger_name = logger_name
        self.logger = logging.getLogger(self.logger_name)
        self.logger.setLevel(logging.INFO)
        formatter = JSONFormatter()
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def log(self, level, message, *args, **kwargs):
        """General log method."""
        extra = kwargs.get("extra", {})
        self.logger.log(level, message, *args, extra=extra)

    def info(self, message, *args, **kwargs):
        """INFO."""
        self.log(logging.INFO, message, *args, **kwargs)

    def debug(self, message, *args, **kwargs):
        """DEBUG."""
        self.log(logging.DEBUG, message, *args, **kwargs)

    def warning(self, message, *args, **kwargs):
        """WARNING."""
        self.log(logging.WARNING, message, *args, **kwargs)

    def error(self, message, *args, **kwargs):
        """ERROR."""
        self.log(logging.ERROR, message, *args, **kwargs)

    def critical(self, message, *args, **kwargs):
        """CRITICAL."""
        self.log(logging.CRITICAL, message, *args, **kwargs)
