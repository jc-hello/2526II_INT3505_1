from fastapi import FastAPI, Query
from models import Book
from schemas.offset_limit import OffsetLimitResponse

app = FastAPI(title="Pagination Demo: Offset/Limit", description="Offset/Limit pagination strategy demo for API /books")

# Mock data for books
db_books = [
    Book(id=i, title=f"Programming Book {i}", author=f"Author {i % 5}", status="available")
    for i in range(1, 101)
]

@app.get("/books", response_model=OffsetLimitResponse[Book], tags=["Books"])
def get_books(
    offset: int = Query(0, ge=0, description="Start position"),
    limit: int = Query(20, ge=1, le=50, description="Maximum number of items to return")
):
    """
    1. Offset/Limit Pagination
    - Retrieve books based on skipped rows (offset) and fetched rows (limit).
    """
    items = db_books[offset : offset + limit]
    return OffsetLimitResponse(
        items=items,
        total=len(db_books),
        offset=offset,
        limit=limit
    )
