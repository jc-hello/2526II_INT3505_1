# PLAN.md: Resource Design Methodology

This document describes the standardized process we used to move from business context (Domain Context) to an API Resource Tree, based on principles from James Higginbotham.

## Step 1: Identify Domain Entities
Instead of starting from the database schema, we start from key business nouns in the library domain:
- **Reader (`User`):** The person who borrows books.
- **Book (`Book`):** The asset being borrowed.
- **Loan (`Loan`/Borrowing):** The transaction between a reader and a book.
From this, we derive three root resources: `/users`, `/books`, `/loans`.

## Step 2: Define Boundaries and Relationships
Define how resources interact to determine URI structure (independent vs. nested):
- Books and users exist independently.
- A `Loan` must be associated with one `User` and one `Book`.
- Admins need to see full borrowing history (`/loans`), while readers need their own history (`/users/{id}/loans`).

## Step 3: Apply Shallow Routing
To avoid overly deep and hard-to-maintain URIs (anti-pattern: `/users/{userId}/loans/{loanId}/books/{bookId}`), we cap URI depth at level 2.
- Retrieve a specific user's loan list: `/users/{userId}/loans`.
- Interact with a specific loan directly: `/loans/{loanId}`.

## Step 4: Map Actions to HTTP Methods
Use nouns for endpoints, and let HTTP methods (GET, POST, PUT, PATCH, DELETE) represent actions.
- Avoid: `POST /borrowBook` or `POST /returnBook`.
- Use: `POST /loans` (create a loan) and `PATCH /loans/{id}` (update status to `returned`).