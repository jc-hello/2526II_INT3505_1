# Demo of Pagination Strategies

This demo uses FastAPI to illustrate three different pagination strategies. Based on `RESOURCE_TREE.md`, the list endpoint is `GET /books`. Each strategy is implemented as an independent runnable FastAPI app.

Response schema definitions are kept separately in the `schemas` folder.

## Folder Structure

```
week_5/demo/
├── offset_limit_demo.py     # FastAPI demo for Offset/Limit pagination
├── page_based_demo.py       # FastAPI demo for Page-based pagination
├── cursor_based_demo.py     # FastAPI demo for Cursor-based pagination
├── models.py                # Shared data model (Book entity)
├── schemas/                 # Response schema definitions
│   ├── offset_limit.py      # Response schema for Offset/Limit
│   ├── page_based.py        # Response schema for Page-based
│   └── cursor_based.py      # Response schema for Cursor-based
└── README.md                # This guide
```

## Detailed Strategy Explanations

### 1. Offset / Limit Pagination
**Runner file:** `offset_limit_demo.py`
**Response schema file:** `schemas/offset_limit.py`
**API definition:** `GET /books?offset=0&limit=20`

* **How it works:** Skip `offset` records, then return the next `limit` records.
* **Response model:** Includes `items`, `total`, `offset`, and `limit`.
* **Pros:** Easy to understand and maps directly to SQL `OFFSET / LIMIT`.
* **Cons:** Performance degrades significantly at large `offset` values because the DB still scans skipped rows. Data consistency can drift if records are inserted/deleted between page requests.

### 2. Page-based Pagination (Page / Size)
**Runner file:** `page_based_demo.py`
**Response schema file:** `schemas/page_based.py`
**API definition:** `GET /books?page=1&size=20`

* **How it works:** Specify page number `page` and page size `size`. Internally this is usually converted to offset (`offset = (page - 1) * size`).
* **Response model:** Includes `items`, `total`, `page`, `size`, and `total_pages`.
* **Pros:** Friendly for page-number UI patterns (1, 2, 3, ...).
* **Cons:** Shares the same performance and consistency drawbacks as Offset/Limit.

### 3. Cursor-based Pagination (Next Token)
**Runner file:** `cursor_based_demo.py`
**Response schema file:** `schemas/cursor_based.py`
**API definition:** `GET /books?cursor=10&limit=20`

* **How it works:** Uses a unique, ordered value (for example `id` or `timestamp`) from the last item to fetch the next set (e.g., `WHERE id > cursor LIMIT ...`).
* **Response model:** Includes `items`, `next_cursor`, and `has_next`. `total` is optional and often omitted.
* **Pros:** Very fast even with millions of rows by leveraging DB indexes directly. Avoids duplicates or missing rows during concurrent inserts/deletes.
* **Cons:** Cannot jump directly to an arbitrary page; navigation is sequential. Requires a unique sortable column.


