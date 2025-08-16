import sqlite3
import pandas as pd
from pathlib import Path

# Path to your database
DB_PATH = Path(__file__).resolve().parent.parent / "data" / "food.db"

def run_query(query: str, params: tuple = (), as_df: bool = True):
    """Run SELECT queries and return results as Pandas DataFrame (default) or list of dicts."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(query, params).fetchall()
        if as_df:
            return pd.DataFrame(rows)  # DataFrame with column names
        return [dict(row) for row in rows]

def run_action(query: str, params: tuple = ()):
    """Run INSERT/UPDATE/DELETE queries."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(query, params)
        conn.commit()

# Providers
def list_providers(city=None):
    query = "SELECT * FROM providers"
    params = ()
    if city:
        query += " WHERE city = ?"
        params = (city,)
    return run_query(query, params)

# Receivers
def list_receivers(city=None):
    query = "SELECT * FROM receivers"
    params = ()
    if city:
        query += " WHERE city = ?"
        params = (city,)
    return run_query(query, params)

# Food Listings
def list_food_listings(only_available=False):
    query = "SELECT * FROM food_listings"
    params = ()
    if only_available:
        query += " WHERE status = 'available'"
    return run_query(query, params)

# Utility Functions
def get_total_food_quantity():
    df = run_query("SELECT COALESCE(SUM(quantity), 0) AS total FROM food_listings")
    if df.empty:
        return 0
    return int(df.iloc[0, 0])

def get_provider_types_by_quantity():
    return run_query("""
    SELECT provider_type, SUM(quantity) AS total_quantity
    FROM food_listings
    JOIN providers USING(provider_id)
    GROUP BY provider_type
    """)
