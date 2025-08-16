import sqlite3
import csv
from pathlib import Path

DB = Path("data/food.db")
DATA = Path("data")
VALID_RECEIVER_TYPES = {"ngo", "individual", "shelter", "community", "other"}

def read_csv_dict(path):
    """Read CSV with UTF-8 BOM support and strip header whitespace."""
    with open(path, newline='', encoding="utf-8-sig") as f:
        rdr = csv.DictReader(f)
        rdr.fieldnames = [h.strip() for h in rdr.fieldnames]
        return list(rdr)

def clean_rows(rows, required_fields):
    """Remove rows where required fields are missing or empty."""
    cleaned = []
    for r in rows:
        r = {k: (v.strip() if isinstance(v, str) else v) for k, v in r.items()}
        if all(r.get(f) and str(r.get(f)).strip() != "" for f in required_fields):
            cleaned.append(r)
    return cleaned

def normalize_receiver_type(value):
    """Normalize and validate receiver_type."""
    if not value:
        return "other"
    val = str(value).strip().lower()
    return val if val in VALID_RECEIVER_TYPES else "other"

def bulk_load():
    with sqlite3.connect(DB) as conn:
        conn.execute("PRAGMA foreign_keys = ON;")

        # 1️⃣ Load providers
        providers = read_csv_dict(DATA / "providers_data.cleaned.csv")
        providers = clean_rows(providers, ["provider_id", "name"])
        conn.executemany("""
            INSERT OR REPLACE INTO providers
            (provider_id, name, provider_type, address, city, contact_phone, contact_email)
            VALUES (?, ?, ?, ?, ?, ?, ?)""",
            [(r.get("provider_id"), r.get("name"), r.get("provider_type"), r.get("address"),
              r.get("city"), r.get("contact_phone"), r.get("contact_email"))
             for r in providers])

        # Get valid provider_ids
        valid_provider_ids = {pid for (pid,) in conn.execute("SELECT provider_id FROM providers")}

        # 2️⃣ Load receivers
        receivers = read_csv_dict(DATA / "receivers_data.cleaned.csv")
        receivers = clean_rows(receivers, ["receiver_id", "name"])
        conn.executemany("""
            INSERT OR REPLACE INTO receivers
            (receiver_id, name, receiver_type, city, contact_phone, contact_email)
            VALUES (?, ?, ?, ?, ?, ?)""",
            [(r.get("receiver_id"), r.get("name"), normalize_receiver_type(r.get("receiver_type")),
              r.get("city"), r.get("contact_phone"), r.get("contact_email"))
             for r in receivers])

        # Get valid receiver_ids
        valid_receiver_ids = {rid for (rid,) in conn.execute("SELECT receiver_id FROM receivers")}

        # 3️⃣ Load food listings (only if provider_id exists)
        listings = read_csv_dict(DATA / "food_listings_data.cleaned.csv")
        listings = clean_rows(listings, ["food_id", "food_name", "expiry_date", "provider_id"])
        listings = [r for r in listings if r.get("provider_id") in valid_provider_ids]
        conn.executemany("""
            INSERT OR REPLACE INTO food_listings
            (food_id, food_name, quantity, expiry_date, provider_id, provider_type, location, food_type, meal_type)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            [(r.get("food_id"), r.get("food_name"), int(r.get("quantity", 0)), r.get("expiry_date"),
              r.get("provider_id"), r.get("provider_type"), r.get("location"), r.get("food_type"), r.get("meal_type"))
             for r in listings])

        # Get valid food_ids
        valid_food_ids = {fid for (fid,) in conn.execute("SELECT food_id FROM food_listings")}

        # 4️⃣ Load claims (only if food_id & receiver_id exist)
        claims = read_csv_dict(DATA / "claims_data.cleaned.csv")
        claims = clean_rows(claims, ["claim_id", "food_id", "receiver_id"])
        claims = [r for r in claims if r.get("food_id") in valid_food_ids and r.get("receiver_id") in valid_receiver_ids]
        conn.executemany("""
            INSERT OR REPLACE INTO claims
            (claim_id, food_id, receiver_id, status, timestamp, quantity_claimed)
            VALUES (?, ?, ?, ?, ?, ?)""",
            [(r.get("claim_id"), r.get("food_id"), r.get("receiver_id"), r.get("status", "").lower(),
              r.get("timestamp"), int(r.get("quantity_claimed", 0))) for r in claims])

    print("✅ Loaded cleaned CSVs into SQLite without foreign key errors.")

if __name__ == "__main__":
    bulk_load()
