import logging
import sys
from logging import Logger
from logging.handlers import TimedRotatingFileHandler
from typing import Optional

from config.settings import test_settings


def get_console_handler(
    log_format: Optional[str] = test_settings.LOGGER_FORMATTER,
) -> logging.StreamHandler:
    """
    Get handler for console output

    Parameters
    ----------
    log_format : Optional[str], optional
        Logging format, by default test_settings.LOGGER_FORMATTER

    Returns
    -------
    logging.StreamHandler
        StreamHandler
    """
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter(log_format))
    return console_handler


def get_file_handler(
    log_file: Optional[str] = test_settings.LOGGER_FILE,
    log_format: Optional[str] = test_settings.LOGGER_FORMATTER,
) -> TimedRotatingFileHandler:
    """
    Get handler for file output

    Parameters
    ----------
    log_file : Optional[str], optional
        Logging file, by default test_settings.LOGGER_FILE
    log_format : Optional[str], optional
        Logging format, by default test_settings.LOGGER_FORMATTER

    Returns
    -------
    TimedRotatingFileHandler
        File handler for logging
    """
    file_handler = TimedRotatingFileHandler(log_file, when="midnight")
    file_handler.setFormatter(logging.Formatter(log_format))
    return file_handler


def get_logger(
    logger_name: str,
    log_format: Optional[str] = test_settings.LOGGER_FORMATTER,
    level: Optional[str] = test_settings.LOGGER_LEVEL,
    log_file: Optional[str] = test_settings.LOGGER_FILE,
) -> Logger:
    """
    Get child logger.

    Put the following command into any
      module where logging is required:
    ```
    logger = get_logger(__name__)
    ```

    Parameters
    ----------
    logger_name : str
        Name of the logger
    log_format : Optional[str], optional
        Logging format, by default test_settings.LOGGER_FORMATTER
    level : Optional[str], optional
        Logging level, by default test_settings.LOGGER_LEVEL
    log_file : Optional[str], optional
        Logging file, by default test_settings.LOGGER_FILE

    Returns
    -------
    Logger
        Logger

    Raises
    ------
    KeyError
        If logging level is chosen incorrecly.
    """
    logger = logging.getLogger(logger_name)

    match level:
        case "DEBUG":
            level = logging.DEBUG
        case "INFO":
            level = logging.INFO
        case "WARNING":
            level = logging.WARNING
        case "ERROR":
            level = logging.ERROR
        case "CRITICAL":
            level = logging.CRITICAL
        case _:
            raise KeyError("Logging level is selected incorrectly!")

    logger.setLevel(level)
    logger.addHandler(get_console_handler(log_format=log_format))
    if log_file is not None:
        logger.addHandler(get_file_handler(log_file=log_file, log_format=log_format))
    logger.propagate = False
    return logger
