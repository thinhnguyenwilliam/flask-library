from flask import Blueprint, request, jsonify, current_app

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    current_app.logger.info(f"POST /auth/login - Data: {data}")

    # Dummy login logic
    if data.get("username") == "admin" and data.get("password") == "secret":
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401


@auth_bp.route("/status", methods=["GET"])
def status():
    current_app.logger.info("GET /auth/status - Checking login status")
    return "funny"
    #return jsonify({"status": "OK"})
