import logging
from logging.handlers import RotatingFileHandler
import os
from datetime import datetime, timezone
import json_log_formatter


class CustomJSONFormatter(json_log_formatter.JSONFormatter):
    def json_record(self, message, extra, record):
        # Add custom fields
        extra['message'] = message
        extra['time'] = datetime.fromtimestamp(record.created, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
        extra['level'] = record.levelname
        extra['module'] = record.module
        return extra


def setup_logger(app):
    log_dir = os.path.join(os.getcwd(), 'logs')
    os.makedirs(log_dir, exist_ok=True)

    log_path = os.path.join(log_dir, 'flask_app.log')
    file_handler = RotatingFileHandler(
        log_path,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(logging.INFO)

    formatter = CustomJSONFormatter()
    file_handler.setFormatter(formatter)

    if app.logger.hasHandlers():
        app.logger.handlers.clear()

    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info("Logger initialized ✅")
