"""
Logging configuration and utilities for the AI Assistant.
"""

import logging
import logging.handlers
from pathlib import Path
from typing import Optional
from config.settings import settings


class LoggerSetup:
    """Configure logging for the application."""

    _loggers = {}

    @classmethod
    def setup_logger(
        cls,
        name: str,
        log_file: Optional[str] = None,
        level: Optional[str] = None,
    ) -> logging.Logger:
        """
        Setup and return a logger with both file and console handlers.

        Args:
            name: Logger name (usually __name__)
            log_file: Optional custom log file path
            level: Optional custom log level

        Returns:
            Configured logger instance
        """
        if name in cls._loggers:
            return cls._loggers[name]

        logger = logging.getLogger(name)
        logger.setLevel(getattr(logging, level or settings.LOG_LEVEL))

        # Avoid duplicate handlers
        if logger.hasHandlers():
            return logger

        formatter = logging.Formatter(settings.LOG_FORMAT)

        # Console Handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, settings.LOG_LEVEL))
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # File Handler
        log_file_path = log_file or settings.LOG_FILE
        file_path = Path(log_file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.handlers.RotatingFileHandler(
            log_file_path,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5,
        )
        file_handler.setLevel(getattr(logging, settings.LOG_LEVEL))
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        cls._loggers[name] = logger
        return logger

    @classmethod
    def get_logger(cls, name: str) -> logging.Logger:
        """Get or create a logger."""
        if name not in cls._loggers:
            cls.setup_logger(name)
        return cls._loggers[name]


def get_logger(name: str) -> logging.Logger:
    """Convenience function to get a logger."""
    return LoggerSetup.get_logger(name)
