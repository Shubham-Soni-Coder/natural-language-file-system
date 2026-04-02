import logging
from logging.handlers import RotatingFileHandler
from .Config import settings


def setup_logging():
    log_level_str = str(settings.LOG_LEVEL).upper()
    log_level = getattr(logging, log_level_str, logging.INFO)

    log_file_path = settings.LOG_FILE_PATH
    app_logger = logging.getLogger("AIFileManagerment")
    app_logger.setLevel(log_level)

    if not app_logger.handlers:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        console_handler.setFormatter(formatter)
        app_logger.addHandler(console_handler)

        file_handler = RotatingFileHandler(
            log_file_path, maxBytes=5 * 1024 * 1024, backupCount=5
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        app_logger.addHandler(file_handler)

        for logger_name, level in [
            ("uvicorn", logging.INFO),
            ("uvicorn.access", logging.INFO),
            ("sqlalchemy.engine", logging.WARNING),
        ]:
            target_logger = logging.getLogger(logger_name)
            target_logger.handlers = app_logger.handlers
            target_logger.setLevel(level)

    return app_logger

main_logger = setup_logging()

