from datetime import datetime, timezone

# In-memory data store
_items: dict[int, dict] = {}
_id_counter = 1


def _next_id() -> int:
    global _id_counter
    cid = _id_counter
    _id_counter += 1
    return cid


def get_all() -> list[dict]:
    return list(_items.values())


def get_one(item_id: int) -> dict | None:
    return _items.get(item_id)


def create(name: str, description: str = "", status: str = "active") -> dict:
    item = {
        "id": _next_id(),
        "name": name,
        "description": description,
        "status": status,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": None,
    }
    _items[item["id"]] = item
    return item


def update(item_id: int, name: str | None = None, description: str | None = None, status: str | None = None) -> dict | None:
    item = _items.get(item_id)
    if item is None:
        return None
    if name is not None:
        item["name"] = name
    if description is not None:
        item["description"] = description
    if status is not None:
        item["status"] = status
    item["updated_at"] = datetime.now(timezone.utc).isoformat()
    return item


def delete(item_id: int) -> dict | None:
    return _items.pop(item_id, None)
