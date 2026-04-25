"""Centralised application logger.

All logging goes through AppLogger so every line is consistently formatted
with a LogCode prefix: [INF-001] message text.

Setup:
    Call configure_logging() once at application startup (app/main.py).

Usage:
    AppLogger.info(LogCode.INF_CSV_LOADED, f"Imported {n} leads from {path.name}")
    AppLogger.raise_error(LogCode.ERR_FILE_NOT_FOUND, f"File not found: {path}")
"""

import logging

from app.utility.codes import LogCode

_logger = logging.getLogger("growth_agent")


def configure_logging(level: int = logging.INFO) -> None:
    """Configure the root logger. Call once at startup."""
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(
        "%(asctime)s %(levelname)-8s %(message)s",
        datefmt="%H:%M:%S"
    ))
    _logger.setLevel(level)
    _logger.addHandler(handler)
    _logger.propagate = False


class AppLogger:
    @staticmethod
    def debug(code: LogCode, message: str) -> None:
        _logger.debug("[%s] %s", code, message)

    @staticmethod
    def info(code: LogCode, message: str) -> None:
        _logger.info("[%s] %s", code, message)

    @staticmethod
    def warning(code: LogCode, message: str) -> None:
        _logger.warning("[%s] %s", code, message)

    @staticmethod
    def error(code: LogCode, message: str, *, exc_info: bool = False) -> None:
        _logger.error("[%s] %s", code, message, exc_info=exc_info)

    @staticmethod
    def raise_error(code: LogCode, detail: str = "") -> None:
        """Log at ERROR level and raise AppError in one call."""
        _logger.error("[%s] %s", code, detail)
        raise Exception(detail)
