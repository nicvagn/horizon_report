"""Logger setup for the package.

This module configures logging for the package-level operations.
"""
import logging

from .constants import DEBUG, FILE_HANDLER, LOGGER_NAME

# Extracted constants for logging config
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


def setup_logger() -> logging.Logger:
    """Set up and return configured logger for the package."""
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(logging.DEBUG if DEBUG else logging.INFO)

    # Configure logging format
    formatter = logging.Formatter(LOG_FORMAT)

    # Add file handler if specified
    if FILE_HANDLER:
        file_handler = logging.FileHandler(FILE_HANDLER)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    # Add a console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger


# Initialize package logger
logger = setup_logger()
