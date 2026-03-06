from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

import models

items_bp = Blueprint("items", __name__)


@items_bp.route("/", methods=["GET"])
@jwt_required()
def list_items():
    """Return all items."""
    return jsonify(models.get_all()), 200


@items_bp.route("/<int:item_id>", methods=["GET"])
@jwt_required()
def get_item(item_id: int):
    """Return a single item by ID."""
    item = models.get_one(item_id)
    if item is None:
        return jsonify({"error": "item not found"}), 404
    return jsonify(item), 200


@items_bp.route("/", methods=["POST"])
@jwt_required()
def create_item():
    """Create a new item."""
    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()
    if not name:
        return jsonify({"error": "name is required"}), 400
    item = models.create(name, data.get("description", ""))
    return jsonify(item), 201


@items_bp.route("/<int:item_id>", methods=["PUT"])
@jwt_required()
def update_item(item_id: int):
    """Update an existing item."""
    data = request.get_json(silent=True) or {}
    item = models.update(item_id, data.get("name"), data.get("description"))
    if item is None:
        return jsonify({"error": "item not found"}), 404
    return jsonify(item), 200


@items_bp.route("/<int:item_id>", methods=["DELETE"])
@jwt_required()
def delete_item(item_id: int):
    """Delete an item."""
    item = models.delete(item_id)
    if item is None:
        return jsonify({"error": "item not found"}), 404
    return jsonify({"message": "item deleted"}), 200
