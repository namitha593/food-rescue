PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS providers (
    provider_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    provider_type TEXT CHECK(provider_type IN ('restaurant','store','bakery','caterer','other')) DEFAULT 'other',
    address TEXT,
    city TEXT NOT NULL,
    contact_phone TEXT,
    contact_email TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS receivers (
    receiver_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    receiver_type TEXT CHECK(receiver_type IN ('ngo','individual','shelter','community','other')) DEFAULT 'ngo',
    city TEXT NOT NULL,
    contact_phone TEXT,
    contact_email TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS food_listings (
    food_id TEXT PRIMARY KEY,
    food_name TEXT NOT NULL,
    quantity INTEGER NOT NULL CHECK(quantity >= 0),
    expiry_date DATE NOT NULL,
    provider_id TEXT NOT NULL,
    provider_type TEXT,
    location TEXT,
    food_type TEXT,
    meal_type TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (provider_id) REFERENCES providers(provider_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS claims (
    claim_id TEXT PRIMARY KEY,
    food_id TEXT NOT NULL,
    receiver_id TEXT NOT NULL,
    status TEXT NOT NULL CHECK(status IN ('pending','approved','completed','canceled')),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    quantity_claimed INTEGER NOT NULL CHECK(quantity_claimed >= 0),
    FOREIGN KEY (food_id) REFERENCES food_listings(food_id) ON DELETE CASCADE,
    FOREIGN KEY (receiver_id) REFERENCES receivers(receiver_id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_food_provider ON food_listings(provider_id);
CREATE INDEX IF NOT EXISTS idx_food_city ON food_listings(location);
CREATE INDEX IF NOT EXISTS idx_claims_food ON claims(food_id);
CREATE INDEX IF NOT EXISTS idx_claims_receiver ON claims(receiver_id);
CREATE INDEX IF NOT EXISTS idx_claims_status ON claims(status);
