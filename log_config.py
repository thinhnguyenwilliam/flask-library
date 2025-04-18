import os
import uuid
import logging
from datetime import datetime, timezone
from flask import has_request_context, request, g
from logging.handlers import RotatingFileHandler
from json_log_formatter import JSONFormatter

# Custom JSON Formatter for structured logs
class ProdJSONFormatter(JSONFormatter):
    def json_record(self, message, extra, record):
        extra['message'] = message
        extra['level'] = record.levelname
        extra['logger'] = record.name

        if has_request_context():
            extra['method'] = request.method
            extra['url'] = request.url
            extra['ip'] = getattr(g, 'log_ip', None)
            extra['path'] = getattr(g, 'log_path', None)
            extra['log_id'] = getattr(g, 'log_id', None)

        return extra

# Pretty console formatter for development
class DevConsoleFormatter(logging.Formatter):
    def format(self, record):
        time = datetime.fromtimestamp(record.created, tz=timezone.utc).strftime('%H:%M:%S')
        return f"[{time}] {record.levelname} [{record.module}] {record.getMessage()}"

# Logger setup function
def setup_logger(app, env='production'):
    log_dir = os.path.join(os.getcwd(), 'logs')
    os.makedirs(log_dir, exist_ok=True)

    level = logging.DEBUG if env == 'development' else logging.INFO
    app.logger.setLevel(level)

    # JSON file handler
    file_handler = RotatingFileHandler(
        os.path.join(log_dir, 'flask_app.log'),
        maxBytes=10 * 1024 * 1024,
        backupCount=5
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(ProdJSONFormatter())

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(DevConsoleFormatter() if env == 'development' else ProdJSONFormatter())

    # Clear old handlers
    if app.logger.hasHandlers():
        app.logger.handlers.clear()

    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)

    app.logger.info("Logger initialized ✅")

# Middleware to inject request-specific metadata
def inject_log_metadata(app):
    @app.before_request
    def attach_log_metadata():
        g.log_id = str(uuid.uuid4())
        g.log_path = request.path
        g.log_ip = request.remote_addr
