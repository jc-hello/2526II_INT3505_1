from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_bp = Blueprint("auth", __name__)

# Mock user store – replace with a real DB in production
_USERS = {
    "admin": "password123",
    "user": "user123",
}


@auth_bp.route("/login", methods=["POST"])
def login():
    """Authenticate and return a JWT access token."""
    data = request.get_json(silent=True) or {}
    username = data.get("username", "").strip()
    password = data.get("password", "")

    if not username or not password:
        return jsonify({"error": "username and password are required"}), 400

    if _USERS.get(username) != password:
        return jsonify({"error": "invalid credentials"}), 401

    token = create_access_token(identity=username)
    return jsonify({"access_token": token}), 200


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    """Return the currently authenticated user."""
    return jsonify({"user": get_jwt_identity()}), 200
