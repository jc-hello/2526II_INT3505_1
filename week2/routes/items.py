from flask import Blueprint, jsonify, request, make_response
from flask_jwt_extended import jwt_required

import models

items_bp = Blueprint("items", __name__)

# Cache-Control TTL for read operations (seconds)
_LIST_CACHE_TTL = 30
_ITEM_CACHE_TTL = 60


@items_bp.route("/", methods=["GET"])
@jwt_required()
def list_items():
    """Return all items with optional pagination (cached for 30 s)."""
    # Pagination parameters
    page = request.args.get("page", type=int, default=1)
    page_size = request.args.get("page_size", type=int, default=10)
    
    # Validate pagination parameters
    if page < 1:
        return jsonify({"error": "page must be >= 1"}), 400
    if page_size < 1 or page_size > 100:
        return jsonify({"error": "page_size must be between 1 and 100"}), 400
    
    all_items = models.get_all()
    total_items = len(all_items)
    total_pages = (total_items + page_size - 1) // page_size  # Ceiling division
    
    # Calculate pagination indices
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    paginated_items = all_items[start_index:end_index]
    
    result = {
        "items": paginated_items,
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total_items": total_items,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_previous": page > 1,
        }
    }
    
    response = make_response(jsonify(result), 200)
    response.headers["Cache-Control"] = f"public, max-age={_LIST_CACHE_TTL}"
    return response


@items_bp.route("/search", methods=["GET"])
@jwt_required()
def search_items():
    """Search and filter items by name or description (cached for 30 s)."""
    query = request.args.get("q", "").strip().lower()
    status = request.args.get("status", "").strip()
    
    if not query and not status:
        return jsonify({"error": "query parameter 'q' or 'status' is required"}), 400
    
    items = models.get_all()
    filtered_items = []
    
    for item in items:
        name_match = query in item.get("name", "").lower() if query else True
        desc_match = query in item.get("description", "").lower() if query else True
        status_match = item.get("status") == status if status else True
        
        if (name_match or desc_match) and status_match:
            filtered_items.append(item)
    
    response = make_response(jsonify({
        "items": filtered_items,
        "total": len(filtered_items),
        "query": query if query else None,
        "filters": {"status": status} if status else {}
    }), 200)
    response.headers["Cache-Control"] = f"public, max-age={_LIST_CACHE_TTL}"
    return response


@items_bp.route("/<int:item_id>", methods=["GET"])
@jwt_required()
def get_item(item_id: int):
    """Return a single item by ID (cached for 60 s)."""
    item = models.get_one(item_id)
    if item is None:
        return jsonify({"error": "item not found"}), 404
    response = make_response(jsonify(item), 200)
    response.headers["Cache-Control"] = f"public, max-age={_ITEM_CACHE_TTL}"
    return response


@items_bp.route("/", methods=["POST"])
@jwt_required()
def create_item():
    """Create a new item."""
    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()
    if not name:
        return jsonify({"error": "name is required"}), 400
    item = models.create(name, data.get("description", ""), data.get("status", "active"))
    return jsonify(item), 201


@items_bp.route("/<int:item_id>", methods=["PUT"])
@jwt_required()
def update_item(item_id: int):
    """Update an existing item."""
    data = request.get_json(silent=True) or {}
    item = models.update(item_id, data.get("name"), data.get("description"), data.get("status"))
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
