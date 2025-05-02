"""Logger setup for the package.

This module configures logging for the package-level operations.
"""
from horizon_report import setup_logger

# module level logger configuration
debug = True
file_handler = None
logger_name = __name__

# Initialize package logger
logger = setup_logger(debug, file_handler, logger_name)
