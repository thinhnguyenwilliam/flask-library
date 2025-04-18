from flask import Blueprint, request, jsonify, current_app,g
import uuid
import time
from app.services.user_service import create_user, get_users
import logging

# Set up logging
#logging.basicConfig(level=logging.INFO)  # Could also use DEBUG, WARNING, ERROR, CRITICAL
#logger = logging.getLogger(__name__)

user_bp = Blueprint("users", __name__)
@user_bp.route("/", methods=["GET"])
def list_users():
    current_app.logger.info("GET /users - Fetching all users")
    #return jsonify(get_users())
    #logger.info("GET /users - Fetching all users hihi")
    return "Hello, Flask Logging!"

@user_bp.route("/", methods=["POST"])
def add_user():
    data = request.get_json()
    return jsonify(create_user(data)),201
