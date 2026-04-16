# RESOURCE_TREE.md: API Resource Tree Design

Based on the method in `PLAN.md`, below is the endpoint design for the library management system.

## 1. Resource: Books (`/books`)
Represents the library book catalog.

- `GET /books`
  - **Description:** Retrieve the book list with search and pagination support.
  - **Query Params (Pagination Demo):**
    - Offset/Limit: `?offset=0&limit=20`
    - Page-based: `?page=1&size=20`
    - Cursor-based: `?cursor=last_id_here&limit=20`
  - **Query Params (Search):** `?q=book_title` or `?author=author_name`
- `GET /books/{bookId}`
  - **Description:** Retrieve details of one book.
- `POST /books`
  - **Description:** Add a new book (for Admin/Librarian).
- `PUT /books/{bookId}`
  - **Description:** Update all information of a book.
- `DELETE /books/{bookId}`
  - **Description:** Delete a book (or mark it as inactive).

## 2. Resource: Users (`/users`)
Represents readers/members.

- `GET /users`
  - **Description:** Retrieve member list (with pagination support similar to `/books`).
- `GET /users/{userId}`
  - **Description:** Retrieve details of one reader.
- `POST /users`
  - **Description:** Register a new member.

## 3. Resource: Loans (`/loans`)
Represents borrowing/return transactions.

- `GET /loans`
  - **Description:** Retrieve full borrowing history of the library (for Admin), with pagination support.
  - **Query Params (Filter):** `?status=active` (currently borrowed) or `?status=returned` (returned).
- `GET /loans/{loanId}`
  - **Description:** Retrieve details of one loan record.
- `POST /loans`
  - **Description:** Borrow a book (create a new loan transaction).
  - **Payload:** `{ "userId": "123", "bookId": "456" }`
- `PATCH /loans/{loanId}`
  - **Description:** Return a book (update loan status).
  - **Payload:** `{ "status": "returned", "returnedAt": "2026-03-26T10:00:00Z" }`

## 4. Sub-Resources (Relationships)
- `GET /users/{userId}/loans`
  - **Description:** Retrieve borrowed/borrowing books for one specific reader, with pagination support for heavy annual borrowing history.