import logging

LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FORMAT = "%(asctime)s [%(levelname)s]: %(filename)s(%(funcName)s:%(lineno)s) >> %(message)s"
setup_loggers = {}


def setup_logger(debug, file_handler, logger_name, PROPAGATE=False) -> logging.Logger:
    """Set up and return the configured logger for the package."""
    global setup_loggers
    # so the same logger does not get setup multiple times
    if logger_name in setup_loggers.keys():
        print("XXXXXXlogger %s already created." % logger_name)
        return setup_loggers[logger_name]

    logger: logging.Logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG if debug else logging.INFO)

    # Configure logging format
    formatter = logging.Formatter(LOG_FORMAT)

    # Add a file handler if specified
    if file_handler:
        file_handler = logging.FileHandler(file_handler)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    # Add a console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    # stop logger propigation.
    logger.propagate = PROPAGATE

    setup_loggers[logger_name] = logger

    logger.debug(
        "Logger created: %s, debug: %s, file_handler: %s, logger_name: %s",
        logger, debug, file_handler, logger_name)
    # logger.debug("setup loggers: %s", setup_loggers)
    return logger
