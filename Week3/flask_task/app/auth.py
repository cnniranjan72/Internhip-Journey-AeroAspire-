from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from datetime import timedelta

auth_bp = Blueprint("auth_bp", __name__, url_prefix="/api/v1/auth")

USERS = {
    "niranjan-admin": "pass123"
}


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    User login
    ---
    tags:
      - Authentication
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: Login
          required:
            - username
            - password
          properties:
            username:
              type: string
            password:
              type: string
    responses:
      200:
        description: Login successful, returns access token
      400:
        description: Missing username/password
      401:
        description: Invalid credentials
    """
    if not request.is_json:
        return jsonify({"error": "Missing JSON in request"}), 400

    username = request.json.get("username")
    password = request.json.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    normalized_username = username.lower()
    if USERS.get(normalized_username) != password:
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=normalized_username, expires_delta=timedelta(hours=1))
    return jsonify({"access_token": access_token}), 200
