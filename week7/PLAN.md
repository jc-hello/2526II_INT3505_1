# Week 7 Plan: Build a RESTful Backend API with OpenAPI and Swagger Codegen

## 1. Tooling and Architecture
- **Language & Framework:** Python - FastAPI
- **Code generation tool:** `fastapi-code-generator` (Python-native, Windows-compatible, and does not require Java).
- **High automation level:** Generates a complete HTTP server project (`main.py`, `routers/`, and Pydantic `models.py`) so the base structure does not need to be handwritten.
- **Database integration (SQLite):** After endpoint scaffolding is generated, use a plug-and-play approach by injecting DB access functions into generated router files.
- **Authentication:** Public-access API setup for demo purposes.

## 2. Structure Design (OpenAPI Spec)

### 2.1. Model Schema `Product`
Lean fields for core CRUD operations:
- `id` (integer) - Primary key
- `name` (string) - Product name
- `price` (number/float) - Price
- `stock_quantity` (integer) - Quantity in stock

### 2.2. API Resources (Resource Tree)
| Method | Path (URI) | Function (Tags: Product) | Input Parameters |
|:---:|---|---|---|
| `GET` | `/products` | Get product list | **Query:** `name` (partial match), `min_price`, `max_price` |
| `POST` | `/products` | Create product | **Body:** Product schema (without `id`) |
| `GET` | `/products/{productId}` | Get product details | **Path:** `productId` |
| `PUT` | `/products/{productId}` | Update product | **Path:** `productId`, **Body:** Product |
| `DELETE` | `/products/{productId}` | Delete product from DB | **Path:** `productId` |

### 2.3. Data Module Design (Plug-and-Play Architecture)
To support hands-on demos while preserving clean architecture, prepare these DB files:
- `database.py`: Connection engine and DB session setup (SQLite).
- `product_repo.py`: Data access logic functions (create/read/update/delete).
- **Plug-and-play principle:** Code generation creates empty routers. Developers inject prepared data module functions and import them into matching routes. The generated architecture remains stable while immediately supporting real DB operations.

## 3. Week 7 Implementation Roadmap
When executing `/create`, perform these phases:

- [ ] **Phase 1:** Design `swagger.yaml` to accurately describe the API tree in OpenAPI v3 format.
- [ ] **Phase 2:** Use the auto-codegen engine to convert YAML into a new FastAPI project structure.
- [ ] **Phase 3:** Set up SQLite and inject SQL/data-access logic into generated router service functions.
- [ ] **Phase 4:** Test endpoints and finalize `README.md` with package install and `uvicorn` run instructions.
