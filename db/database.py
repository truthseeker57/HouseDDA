import sqlite3
from db.models import SCHEMA
from config import DATABASE_PATH

def init_db():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.executescript(SCHEMA)
    conn.commit()
    conn.close()
    
    
    
def get_last_price(zpid):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.execute(
        "SELECT last_price from seen_listings WHERE zpid = ?",
        (zpid,)
    )
    
    row = cursor.fetchone()
    conn.close()
    
    if row is None:
        return None
    return row[0]

def upsert_listing(zpid, price):
    conn = sqlite3.connect(DATABASE_PATH)
    conn.execute(
        """
        INSERT INTO seen_listings (zpid, last_price)
        VALUES(?, ?)
        ON CONFLICT(zpid) DO UPDATE SET last_price = excluded.last_price
        """,
        (zpid, price)
        )
    
    conn.commit()
    conn.close()