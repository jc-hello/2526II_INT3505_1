# CONTEXT.md: API Design Context

## 1. Introduction
This week's project is an API demo designed to illustrate modern Web API design principles related to data modeling and pagination:
1. **Data Modeling & Resource Design:** Build a resource tree that reflects the true semantics of the business domain.
2. **Pagination Strategies:** Implement and compare pagination strategies (Offset/Limit, Page-based, Cursor-based) on search and list endpoints.

## 2. Domain Context
The system focuses on a **basic library management** domain.
Core actions include:
* The library manages its catalog of books.
* Readers register as members.
* Readers borrow and return books.

## 3. Core Domain Models
Instead of mapping 1:1 to all database tables (database-centric), the API resource model is designed from a consumer-centric perspective around three core resources:

* **`Users` (Readers/Members):** Represents people who use the library service. Data focuses on identity and membership status.
* **`Books`:** Represents physical books that can be borrowed. Includes metadata (title, author) and availability status (available or currently borrowed).
* **`Loans` (Borrowing Transactions):** Represents a borrowing agreement where one `User` borrows one `Book`, including borrow/return times, loan status, and related details.

