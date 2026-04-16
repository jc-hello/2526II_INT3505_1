from fastapi import FastAPI, Query
from typing import Optional
from models import Book
from schemas.cursor_based import CursorBasedResponse

app = FastAPI(title="Pagination Demo: Cursor-based", description="Cursor-based pagination strategy demo for API /books")

# Mock data for books
db_books = [
    Book(id=i, title=f"Programming Book {i}", author=f"Author {i % 5}", status="available")
    for i in range(1, 101)
]

@app.get("/books", response_model=CursorBasedResponse[Book], tags=["Books"])
def get_books(
    cursor: Optional[int] = Query(None, description="ID of the last item from the previous page"),
    limit: int = Query(20, ge=1, le=50, description="Maximum number of items to return")
):
    """
    3. Cursor-based Pagination
    - Retrieve books using a cursor that points to the ID of the last known item.
    """
    start_index = 0
    if cursor is not None:
        # Find cursor position in the list
        for i, book in enumerate(db_books):
            if book.id == cursor:
                start_index = i + 1  # Return the item right after cursor
                break

    items = db_books[start_index : start_index + limit]
    
    # Check whether there is a next page
    has_next = (start_index + limit) < len(db_books)
    next_cursor = items[-1].id if items and has_next else None

    return CursorBasedResponse(
        items=items,
        next_cursor=next_cursor,
        has_next=has_next
    )
