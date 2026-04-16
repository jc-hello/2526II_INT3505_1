from fastapi import FastAPI, Query
from models import Book
from schemas.page_based import PageBasedResponse

app = FastAPI(title="Pagination Demo: Page-based", description="Page-based pagination strategy demo for API /books")

# Mock data for books
db_books = [
    Book(id=i, title=f"Programming Book {i}", author=f"Author {i % 5}", status="available")
    for i in range(1, 101)
]

@app.get("/books", response_model=PageBasedResponse[Book], tags=["Books"])
def get_books(
    page: int = Query(1, ge=1, description="Current page number (starting from 1)"),
    size: int = Query(20, ge=1, le=50, description="Number of items per page")
):
    """
    2. Page-based Pagination
    - Retrieve books based on page number and page size.
    """
    offset = (page - 1) * size
    items = db_books[offset : offset + size]
    total_pages = (len(db_books) + size - 1) // size
    
    return PageBasedResponse(
        items=items,
        total=len(db_books),
        page=page,
        size=size,
        total_pages=total_pages
    )
