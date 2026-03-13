from flask import Blueprint, jsonify, make_response
from datetime import datetime, timezone
import sys

system_bp = Blueprint("system", __name__)

# Cache-Control TTL for system endpoints (seconds)
_HEALTH_CACHE_TTL = 10
_STATUS_CACHE_TTL = 30

# Track application start time
_APPLICATION_START_TIME = datetime.now(timezone.utc)


@system_bp.route("/health", methods=["GET"])
def health_check():
    """Check if the application is running and healthy (cached for 10 s)."""
    health_status = {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "service": "Items API",
        "version": "1.0.0"
    }
    
    response = make_response(jsonify(health_status), 200)
    response.headers["Cache-Control"] = f"public, max-age={_HEALTH_CACHE_TTL}"
    return response


@system_bp.route("/status", methods=["GET"])
def system_status():
    """Get detailed system status and runtime information (cached for 30 s)."""
    current_time = datetime.now(timezone.utc)
    uptime_seconds = (current_time - _APPLICATION_START_TIME).total_seconds()
    
    status_info = {
        "status": "operational",
        "uptime_seconds": round(uptime_seconds, 2),
        "uptime_formatted": _format_uptime(uptime_seconds),
        "started_at": _APPLICATION_START_TIME.isoformat(),
        "current_time": current_time.isoformat(),
        "python_version": sys.version,
        "environment": {
            "platform": sys.platform,
            "python_implementation": sys.implementation.name,
        }
    }
    
    response = make_response(jsonify(status_info), 200)
    response.headers["Cache-Control"] = f"public, max-age={_STATUS_CACHE_TTL}"
    return response


@system_bp.route("/ping", methods=["GET"])
def ping():
    """Simple ping endpoint for connectivity checks (cached for 5 s)."""
    response = make_response(jsonify({"message": "pong"}), 200)
    response.headers["Cache-Control"] = "public, max-age=5"
    return response


@system_bp.route("/version", methods=["GET"])
def get_api_version():
    """Get API version information (cached for 1 hour)."""
    version_info = {
        "api_version": "1.0.0",
        "api_name": "Items API",
        "build_date": "2026-03-12",
        "endpoints": {
            "auth": "/auth",
            "items": "/items",
            "system": "/system",
            "docs": "/docs"
        }
    }
    
    response = make_response(jsonify(version_info), 200)
    response.headers["Cache-Control"] = "public, max-age=3600"
    return response


def _format_uptime(seconds: float) -> str:
    """Format uptime seconds into a human-readable string."""
    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    
    parts = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    parts.append(f"{secs}s")
    
    return " ".join(parts)
