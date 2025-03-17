# config.py
class LoggingConfig:
    LEVEL = "INFO"  # Уровни: DEBUG/INFO/WARNING/ERROR/CRITICAL
    LOG_TO_CONSOLE = True
    LOG_TO_FILE = True
    FILENAME = "debug.log"
    FORMAT = "[%(asctime)s] [%(levelname)s] %(message)s"
    MAX_BYTES = 1024 * 1024  # 1MB
    BACKUP_COUNT = 5  # Количество backup-файлов