## Documentation Reading Guide

To understand the design mindset and business context before reviewing the code, read the documents in this order:

1. **[CONTEXT.md](./CONTEXT.md):** Read first. Understand the domain context of the library management system and its core entities (Users, Books, Loans).
2. **[PLAN.md](./PLAN.md):** Read second. Learn the 4-step methodology that transforms real business context into API design.
3. **[RESOURCE_TREE.md](./RESOURCE_TREE.md):** Read third. Review the final endpoint (URI) map.

## Demo Code Guide

While the resource architecture is described in detail in the Markdown files, the **code demo** focuses on practical implementation of three common pagination strategies. Data modeling is implemented in the main server app where database setup and ORM-based access already exist.

**Demo source code location:** [./demo](./demo)

Examples in `./demo` simulate query and response behavior for:
- **Offset/Limit Pagination** (common and easy to implement, but slower on large datasets).
- **Page-based Pagination** (UI-friendly).
- **Cursor-based Pagination** (very high performance, suitable for infinite scroll).

*Note: The demo code uses mock data to illustrate logic flow rather than connecting to a complex real database.*