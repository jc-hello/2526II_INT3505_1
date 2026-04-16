# Basic Backend Automation Guide - Week 7

This document records the required commands for automatic backend code generation (Codegen) with goals of pure Python tooling, high speed, and Windows compatibility.

## Step 1: Install the Tooling
Open a terminal and install the required Python packages:

```bash
# Code generation library
pip install fastapi-code-generator

# Install FastAPI and Uvicorn for running the web server
pip install fastapi uvicorn pydantic
```

## Step 2: Trigger Auto-Generation
Make sure your terminal is in the `week7` folder (which contains `openapi.yaml`). Run:

```bash
fastapi-codegen --input openapi.yaml --output ./server_app
```

## Step 3: Run the generated server (empty API)
To resolve imports correctly for generated files, run the server from the `week7` folder as a package module:

```bash
uvicorn server_app.main:app --port 8080 --reload
```

Open `http://localhost:8080/docs` in a browser to verify.

## Step 4: Turn It Into a Live System (SQLite Integration)

To persist real data, add a data access layer following clean architecture principles.

**4.1. Install ORM package:**
```bash
pip install sqlalchemy
```

**4.2. Initialize database engine (`database.py`):**
Create `server_app/database.py` to manage the local SQLite connection.
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./sqlite_demo.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

**4.3. Declare DB table mapping (`db_models.py`):**
Create `server_app/db_models.py` to map OpenAPI schema fields to a real database table.
```python
from sqlalchemy import Column, Integer, String, Float
from .database import Base

class DBProduct(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    price = Column(Float)
    stock_quantity = Column(Integer)
```

**4.4. Implement CRUD logic (`product_repo.py`):**
Create `server_app/product_repo.py`. This file wraps database operations (read/create/update/delete) as reusable Python functions.

**4.5. Inject data layer into generated code (`main.py`):**
Open `server_app/main.py`, add imports, and replace placeholder `pass` handlers with real implementations using dependency injection.

*Action 1: Initialize DB tables near the top of the file*
```python
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from .database import engine, get_db
from . import db_models, product_repo

# Create tables in SQLite
db_models.Base.metadata.create_all(bind=engine)
```

*Action 2: Replace `pass` in endpoints with repository calls*
```python
@app.post('/products', response_model=Product, status_code=status.HTTP_201_CREATED, tags=['Products'])
def create_product(body: ProductCreate, db: Session = Depends(get_db)) -> Product:
    return product_repo.create_product(db, body)

@app.get('/products', response_model=List[Product], tags=['Products'])
def get_products(
    name: str = None, min_price: float = None, max_price: float = None, db: Session = Depends(get_db)
) -> List[Product]:
    return product_repo.get_products(db, name, min_price, max_price)
```

**4.6. Run and verify:**
Start the server:
```bash
uvicorn server_app.main:app --port 8080 --reload
```
Open Swagger at `http://localhost:8080/docs` and call `POST /products`. You should see `sqlite_demo.db` created.