from pathlib import Path
import sqlite3

DB = Path("data/food.db")          # Location of the SQLite database
SCHEMA = Path("sql/schema_sqlite.sql")  # SQL schema file

def main():
    # Make sure data/ folder exists
    DB.parent.mkdir(exist_ok=True)
    
    # Connect to SQLite DB (creates it if not exists)
    with sqlite3.connect(DB) as conn:
        conn.execute("PRAGMA foreign_keys = ON;")  # Enforce foreign keys
        
        # Read the schema and execute it
        with open(SCHEMA, "r", encoding="utf-8") as f:
            conn.executescript(f.read())
    
    print(f"Initialized SQLite DB at {DB}")

if __name__ == "__main__":
    main()
