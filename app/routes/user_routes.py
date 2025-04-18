from flask import Blueprint, request, jsonify
from app.services.user_service import create_user, get_users

user_bp = Blueprint("users", __name__)

@user_bp.route("/", methods=["GET"])
def list_users():
    #return jsonify(get_users())
    return "hello ngay moi he he bankai"

@user_bp.route("/", methods=["POST"])
def add_user():
    data = request.json
    return jsonify(create_user(data))
