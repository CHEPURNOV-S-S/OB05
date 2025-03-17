# /logging/debug_logger.py

import logging
from logging.handlers import RotatingFileHandler
from .logging_config import LoggingConfig
from .interfaces import ILogger

class DebugLogger(ILogger):
    def __init__(self):
        self.logger = logging.getLogger("DebugLogger")
        self.logger.setLevel(LoggingConfig.LEVEL)

        formatter = logging.Formatter(LoggingConfig.FORMAT)

        if LoggingConfig.LOG_TO_CONSOLE:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

        if LoggingConfig.LOG_TO_FILE:
            file_handler = RotatingFileHandler(
                LoggingConfig.FILENAME,
                maxBytes=LoggingConfig.MAX_BYTES,
                backupCount=LoggingConfig.BACKUP_COUNT,
                encoding='utf-8'
            )
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def debug(self, message: str) -> None:
        self.logger.debug(message)

    def info(self, message: str) -> None:
        self.logger.info(message)

    def warning(self, message: str) -> None:
        self.logger.warning(message)

    def error(self, message: str) -> None:
        self.logger.error(message)

    def critical(self, message: str) -> None:
        self.logger.critical(message)