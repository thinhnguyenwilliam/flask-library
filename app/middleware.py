from flask import request
import uuid
import time

def register_middlewares(app):
    @app.before_request
    def before_request_func():
        request.start_time = time.time()
        request.request_id = str(uuid.uuid4())

        app.logger.info(f"➡️ {request.method} {request.path} | ID: {request.request_id} | IP: {request.remote_addr}")

    @app.after_request
    def after_request_func(response):
        duration = time.time() - getattr(request, "start_time", time.time())
        request_id = getattr(request, "request_id", "N/A")
        app.logger.info(f"⬅️ {request.method} {request.path} | ID: {request_id} | Time: {duration:.3f}s | Status: {response.status_code}")
        response.headers["X-Request-ID"] = request_id  # Optional header
        return response
