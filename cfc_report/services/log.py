"""services relating to setting up logging"""
# Copyright (C) 2024  Nicolas Vaagen
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
import sys


def set_up_logger(logger_name=None, debug=False, file_handler=False) -> logging.Logger:
    """set up logger, including:
        console handler,
        file handler
    parameters:
        logger_name: name of logger to create, default __name__
        debug: set DEBUG logging levels, default is WARNING
        file_handler: should we set up a file handler?
    returns:
        created logger
    """
    if not logger_name:
        raise RuntimeError("No logger_name given")
    logger = logging.getLogger(logger_name)

    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s %(module)s %(message)s")

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    # set up logging to a file if wanted
    if file_handler:
        file_handler = logging.FileHandler(f"{logger_name}.log")
        # always have a verbose log file
        file_handler.setLevel(logging.DEBUG)
        logger.addHandler(file_handler)

    # set up console_handler
    if debug:
        logger.setLevel(logging.DEBUG)
        console_handler.setLevel(logging.DEBUG)
        logger.info("DEBUG is set.")
    else:
        logger.setLevel(logging.WARNING)
        console_handler.setLevel(logging.WARNING)
        logger.info("DEBUG not set")

    logger.addHandler(console_handler)

    # set up except hook for logging
    sys.excepthook = log_except_hook


#  === exception logging ===
# log unhandled exceptions to the log
def log_except_hook(exc_type, exc_value, traceback):
    """catch all the thrown exceptions and log them with level ERROR"""
    logging.error("Uncaught exception",
                  exc_info=(exc_type, exc_value, traceback))


def log_handled_exception(logger, exception: Exception) -> None:
    """log a handled exception, must be called manually"""
    logger.debug("Exception handled: %s", exception)
