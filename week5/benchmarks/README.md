# Database Pagination: Offset vs Cursor ⏱️

This folder contains simulation and **benchmarking tools** that explain why large systems (Facebook, Twitter) avoid traditional Offset/Limit pagination in modern API design.

## 🛠 Demo Workflow (for Instructors/Students)

As a presenter, you only need these three steps:

### Step 1: Initialize the mock database
Generate 100,000 rows to make scan-speed differences visible.
```bash
python seed.py
```
*(This command creates a local `benchmark.db` SQLite file almost instantly via raw SQL queries.)*

### Step 2: Start the API server
Run the backend server that simulates DB queries:
```bash
uvicorn api:app --port 8001
```

### Step 3: Run the benchmark
Open a new terminal tab and send benchmark requests to the server:
```bash
python benchmark.py
```

---

## 🧠 Result Analysis (Presentation Script)

After running `benchmark.py`, a Markdown result table appears. Use it to explain the architecture clearly.

### 1. Strategy: No Pagination (`/books/no-page`)
Directly loads `100,000` rows from the database.
* **Drawback:** The server spends hundreds of milliseconds and extra CPU just to parse a huge data array, plus heavy RAM/network usage.
* **Impact:** Higher risk of backend failure from OOM (Out Of Memory) or client bandwidth bottlenecks.

### 2. Strategy: Offset/Limit (`/books/offset`)
When users scroll deep (for example, around row `95,000`), `OFFSET 95000 LIMIT 20` forces the database to **scan and discard** 95,000 rows before returning the final 20.
* **Impact:** Query time grows linearly, $\mathcal{O}(N)$, with page depth. Deeper pages become slower and waste significant disk I/O.

### 3. Strategy: Cursor Pagination (`/books/cursor`)
For the same checkpoint, the API asks the DB differently: *"Give me 20 rows with primary key `id` greater than the current checkpoint (`id > 95000`)"*.
* **Advantage:** Because `id` is indexed (B-Tree), the DB jumps directly to node `95000` in near-constant practical time, often modeled as $\mathcal{O}(\log n)$, without scanning discarded rows.
* **Benchmark Result:** Cursor pagination is typically **over 25x faster** than offset pagination and remains stable even as the dataset grows dramatically.
