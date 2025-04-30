import logging

LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


def setup_logger(debug, file_handler, logger_name) -> logging.Logger:
    """Set up and return the configured logger for the package."""
    logger: logging.Logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG if debug else logging.INFO)

    # Configure logging format
    formatter = logging.Formatter(LOG_FORMAT)

    # Add a file handler if specified
    if file_handler:
        file_handler = logging.FileHandler(file_handler)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    # Add a console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger
