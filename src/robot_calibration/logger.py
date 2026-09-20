import logging
import os

import colorlog


# Configure the global logging settings
handler = colorlog.StreamHandler()
formatter = colorlog.ColoredFormatter(
    "%(log_color)s%(levelname)-8s%(reset)s %(message)s",
    log_colors={
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bold_red",
    },
)
handler.setFormatter(formatter)


def _get_log_level_from_env():
    """Get the log level from an environment variable"""
    return os.getenv("LOG_LEVEL", "INFO").upper()


def get_logger(name: str) -> logging.Logger:
    logger = colorlog.getLogger(__name__)
    logger.addHandler(handler)
    logger.setLevel(_get_log_level_from_env())
    return logger
