import sqlite3

ANALYTICS_DB = "analytics_warehouse.db"

def initialize_warehouse():
    """Creates an industry-standard analytical Star Schema database."""
    conn = sqlite3.connect(ANALYTICS_DB)
    cursor = conn.cursor()
    
    # 1. Dimension Table: Tracks unique UK user profiles
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dim_users (
        user_key INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT UNIQUE,
        first_seen_location TEXT,
        preferred_device TEXT
    );
    """)

    # 2. Dimension Table: Tracks clean utility/mobile service categorizations
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dim_services (
        service_key INTEGER PRIMARY KEY AUTOINCREMENT,
        service_type TEXT,
        supplier_name TEXT,
        UNIQUE(service_type, supplier_name)
    );
    """)

    # 3. Central Fact Table: Stores raw numerical transaction metrics
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS fact_transactions (
        fact_id INTEGER PRIMARY KEY AUTOINCREMENT,
        transaction_id TEXT UNIQUE,
        timestamp TEXT,
        user_key INTEGER,
        service_key INTEGER,
        amount REAL,
        status TEXT,
        FOREIGN KEY(user_key) REFERENCES dim_users(user_key),
        FOREIGN KEY(service_key) REFERENCES dim_services(service_key)
    );
    """)
    
    conn.commit()
    conn.close()
    print("🏛️ [WAREHOUSE]: Analytics Star Schema initialized successfully.")

if __name__ == "__main__":
    initialize_warehouse()
