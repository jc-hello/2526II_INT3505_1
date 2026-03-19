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
    """Return items with optional filtering, sorting, and pagination (cached for 30 s).

    Query params:
      - page        (int, default 1)
      - page_size   (int, default 10, max 100)
      - status      filter by exact status value (e.g. "active")
      - q           search substring in name or description (case-insensitive)
      - sort_by     field to sort by: "name" | "status" | "created_at" (default "created_at")
      - sort_order  "asc" | "desc" (default "desc")
    """
    # --- Pagination ---
    page = request.args.get("page", type=int, default=1)
    page_size = request.args.get("page_size", type=int, default=10)

    if page < 1:
        return jsonify({"error": "page must be >= 1"}), 400
    if page_size < 1 or page_size > 100:
        return jsonify({"error": "page_size must be between 1 and 100"}), 400

    # --- Filters ---
    status_filter = request.args.get("status", "").strip()
    query = request.args.get("q", "").strip().lower()

    # --- Sorting ---
    valid_sort_fields = {"name", "status", "created_at"}
    sort_by = request.args.get("sort_by", "created_at").strip()
    sort_order = request.args.get("sort_order", "desc").strip().lower()

    if sort_by not in valid_sort_fields:
        return jsonify({"error": f"sort_by must be one of {sorted(valid_sort_fields)}"}), 400
    if sort_order not in ("asc", "desc"):
        return jsonify({"error": "sort_order must be 'asc' or 'desc'"}), 400

    items = models.get_all()

    # Apply filters
    if status_filter:
        items = [i for i in items if i.get("status") == status_filter]
    if query:
        items = [
            i for i in items
            if query in i.get("name", "").lower() or query in i.get("description", "").lower()
        ]

    # Apply sorting
    items.sort(key=lambda i: i.get(sort_by) or "", reverse=(sort_order == "desc"))

    # Apply pagination
    total_items = len(items)
    total_pages = max(1, (total_items + page_size - 1) // page_size)
    start_index = (page - 1) * page_size
    paginated_items = items[start_index: start_index + page_size]

    result = {
        "items": paginated_items,
        "filters": {
            "status": status_filter or None,
            "q": query or None,
        },
        "sort": {"sort_by": sort_by, "sort_order": sort_order},
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total_items": total_items,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_previous": page > 1,
        },
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


@items_bp.route("/statistics", methods=["GET"])
@jwt_required()
def get_items_statistics():
    """Get aggregated statistics about items (cached for 60 s)."""
    all_items = models.get_all()
    
    # Calculate statistics
    total_items = len(all_items)
    status_breakdown = {}
    items_with_description = 0
    
    for item in all_items:
        # Count by status
        status = item.get("status", "unknown")
        status_breakdown[status] = status_breakdown.get(status, 0) + 1
        
        # Count items with descriptions
        if item.get("description"):
            items_with_description += 1
    
    statistics = {
        "total_items": total_items,
        "items_with_description": items_with_description,
        "items_without_description": total_items - items_with_description,
        "status_breakdown": status_breakdown,
        "completion_rate": round((items_with_description / total_items * 100), 2) if total_items > 0 else 0
    }
    
    response = make_response(jsonify(statistics), 200)
    response.headers["Cache-Control"] = f"public, max-age={_ITEM_CACHE_TTL}"
    return response


@items_bp.route("/analytics/recent", methods=["GET"])
@jwt_required()
def get_recent_items_analytics():
    """Get analytics for recently created items (cached for 30 s)."""
    limit = request.args.get("limit", type=int, default=5)
    
    if limit < 1 or limit > 50:
        return jsonify({"error": "limit must be between 1 and 50"}), 400
    
    all_items = models.get_all()
    
    # Sort by created_at (most recent first)
    sorted_items = sorted(
        all_items,
        key=lambda x: x.get("created_at", ""),
        reverse=True
    )
    
    recent_items = sorted_items[:limit]
    
    analytics = {
        "recent_items": recent_items,
        "count": len(recent_items),
        "total_items": len(all_items)
    }
    
    response = make_response(jsonify(analytics), 200)
    response.headers["Cache-Control"] = f"public, max-age={_LIST_CACHE_TTL}"
    return response
