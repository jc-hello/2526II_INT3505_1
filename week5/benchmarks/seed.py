import sqlite3
import random
import time

DB_NAME = "benchmark.db"
TOTAL_RECORDS = 100_000

def seed_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Drop table if it already exists
    cursor.execute("DROP TABLE IF EXISTS books")
    
    # Create table
    cursor.execute("""
        CREATE TABLE books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            price REAL NOT NULL
        )
    """)
    
    print(f"Start seeding {TOTAL_RECORDS} rows for pagination benchmarking...")
    start_time = time.time()
    
    # Prepare sample data
    authors = ["John Doe", "Jane Smith", "Bob Martin", "Martin Fowler", "Robert C. Martin"]
    
    # Insert in batches for better performance
    batch_size = 10000
    for i in range(0, TOTAL_RECORDS, batch_size):
        records = [
            (f"Book #{j}", random.choice(authors), round(random.uniform(10.0, 100.0), 2))
            for j in range(i + 1, i + batch_size + 1)
        ]
        cursor.executemany(
            "INSERT INTO books (title, author, price) VALUES (?, ?, ?)",
            records
        )
        conn.commit()
        print(f" -> Inserted {i + batch_size} rows...")
        
    print(f"Completed in {time.time() - start_time:.2f} seconds.")
    conn.close()

if __name__ == "__main__":
    seed_database()
