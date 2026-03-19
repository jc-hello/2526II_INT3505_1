from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import datetime, timezone

auth_bp = Blueprint("auth", __name__)

# Cache-Control TTL for user profile (seconds)
_USER_PROFILE_CACHE_TTL = 300

# Mock user store – replace with a real DB in production
_USERS = {
    "admin": {"password": "password123", "email": "admin@example.com", "role": "admin", "created_at": "2026-01-01T00:00:00Z"},
    "user": {"password": "user123", "email": "user@example.com", "role": "user", "created_at": "2026-01-02T00:00:00Z"},
}


@auth_bp.route("/login", methods=["POST"])
def login():
    """Authenticate user and return a JWT access token."""
    data = request.get_json(silent=True) or {}
    username = data.get("username", "").strip()
    password = data.get("password", "")

    if not username or not password:
        return jsonify({"error": "username and password are required"}), 400

    user = _USERS.get(username)
    if not user or user.get("password") != password:
        return jsonify({"error": "invalid credentials"}), 401

    token = create_access_token(identity=username)
    return jsonify({"access_token": token, "username": username}), 200


@auth_bp.route("/register", methods=["POST"])
def register_user():
    """Register a new user account."""
    data = request.get_json(silent=True) or {}
    username = data.get("username", "").strip()
    password = data.get("password", "")
    email = data.get("email", "").strip()

    if not username or not password or not email:
        return jsonify({"error": "username, password, and email are required"}), 400

    if username in _USERS:
        return jsonify({"error": "username already exists"}), 409

    _USERS[username] = {
        "password": password,
        "email": email,
        "role": "user",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    token = create_access_token(identity=username)
    return jsonify({
        "message": "user registered successfully",
        "access_token": token,
        "username": username
    }), 201


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def get_current_user_profile():
    """Retrieve the currently authenticated user's profile (cached for 5 minutes)."""
    username = get_jwt_identity()
    user = _USERS.get(username)
    
    if not user:
        return jsonify({"error": "user not found"}), 404
    
    # Return user profile without password
    user_profile = {
        "username": username,
        "email": user.get("email"),
        "role": user.get("role"),
        "created_at": user.get("created_at"),
    }
    
    response = make_response(jsonify(user_profile), 200)
    response.headers["Cache-Control"] = f"private, max-age={_USER_PROFILE_CACHE_TTL}"
    return response


@auth_bp.route("/users", methods=["GET"])
@jwt_required()
def list_all_users():
    """List all registered users (admin only, cacheable)."""
    current_user = get_jwt_identity()
    user = _USERS.get(current_user)
    
    if not user or user.get("role") != "admin":
        return jsonify({"error": "admin access required"}), 403
    
    users_list = [
        {
            "username": username,
            "email": data.get("email"),
            "role": data.get("role"),
            "created_at": data.get("created_at"),
        }
        for username, data in _USERS.items()
    ]
    
    response = make_response(jsonify({"users": users_list, "total": len(users_list)}), 200)
    response.headers["Cache-Control"] = f"private, max-age={_USER_PROFILE_CACHE_TTL}"
    return response
