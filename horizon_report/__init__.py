import logging

LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

set_up_loggers = {}


def setup_logger(debug, file_handler, logger_name) -> logging.Logger:
    """Set up and return the configured logger for the package."""
    global set_up_loggers
    # so the same logger does not get setup multiple times
    if logger_name in set_up_loggers.keys():
        return set_up_loggers[logger_name]

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

    set_up_loggers[logger_name] = logger
    return logger
