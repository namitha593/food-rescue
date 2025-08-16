# app/db.py
import sqlite3
from contextlib import contextmanager
from pathlib import Path

DB = Path("data/food.db")

@contextmanager
def get_conn():
    conn = sqlite3.connect(DB, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()

# -------- Providers ----------
def list_providers(city=None):
    sql = "SELECT * FROM providers"
    params = []
    if city:
        sql += " WHERE city = ?"
        params.append(city)
    with get_conn() as c:
        return c.execute(sql, params).fetchall()

# -------- Food Listings -------
def create_listing(food_id, food_name, quantity, expiry_date, provider_id, provider_type, location, food_type, meal_type):
    with get_conn() as c:
        c.execute("""INSERT INTO food_listings
            (food_id,food_name,quantity,expiry_date,provider_id,provider_type,location,food_type,meal_type)
            VALUES (?,?,?,?,?,?,?,?,?)""",
            (food_id,food_name,quantity,expiry_date,provider_id,provider_type,location,food_type,meal_type))

def update_listing(food_id, **fields):
    if not fields: return
    sets = ", ".join([f"{k}=?" for k in fields])
    vals = list(fields.values()) + [food_id]
    with get_conn() as c:
        c.execute(f"UPDATE food_listings SET {sets} WHERE food_id=?", vals)

def delete_listing(food_id):
    with get_conn() as c:
        c.execute("DELETE FROM food_listings WHERE food_id=?", (food_id,))

def get_listing(food_id):
    with get_conn() as c:
        return c.execute("SELECT * FROM food_listings WHERE food_id=?", (food_id,)).fetchone()

def list_listings(filters: dict = None):
    sql = "SELECT * FROM food_listings WHERE 1=1"
    params = []
    filters = filters or {}
    for col in ("provider_id","provider_type","location","food_type","meal_type"):
        val = filters.get(col)
        if val:
            sql += f" AND {col} = ?"
            params.append(val)
    with get_conn() as c:
        return c.execute(sql, params).fetchall()

# -------- Claims --------------
def create_claim(claim_id, food_id, receiver_id, status, timestamp, quantity_claimed):
    with get_conn() as c:
        c.execute("""INSERT INTO claims
            (claim_id,food_id,receiver_id,status,timestamp,quantity_claimed)
            VALUES (?,?,?,?,?,?)""",
            (claim_id,food_id,receiver_id,status,timestamp,quantity_claimed))

def update_claim(claim_id, **fields):
    if not fields: return
    sets = ", ".join([f"{k}=?" for k in fields])
    vals = list(fields.values()) + [claim_id]
    with get_conn() as c:
        c.execute(f"UPDATE claims SET {sets} WHERE claim_id=?", vals)

def delete_claim(claim_id):
    with get_conn() as c:
        c.execute("DELETE FROM claims WHERE claim_id=?", (claim_id,))

def list_claims(status=None):
    sql = "SELECT * FROM claims"
    params = []
    if status:
        sql += " WHERE status = ?"
        params.append(status)
    with get_conn() as c:
        return c.execute(sql, params).fetchall()
