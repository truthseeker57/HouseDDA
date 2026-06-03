
SCHEMA = """

CREATE TABLE IF NOT EXISTS seen_listings(
    zpid TEXT PRIMARY KEY,
    last_price INTEGER NOT NULL
    );

CREATE TABLE IF NOT EXISTS search_runs(
    id INTEGER PRIMARY KEY,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    listings_found INTEGER DEFAULT 0,
    listings_sent INTEGER DEFAULT 0,
    error TEXT
);

"""