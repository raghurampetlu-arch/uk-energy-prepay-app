import sqlite3
import random

DB_NAME = "energy_app.db"

def initialize_database():
    """Builds the SQLite structure and injects mock UK energy accounts."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Prepayment Account Database Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customer_accounts (
        account_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_name TEXT NOT NULL,
        utility_type TEXT CHECK(utility_type IN ('Gas', 'Electricity')),
        card_number TEXT UNIQUE NOT NULL,
        supplier_name TEXT NOT NULL,
        current_balance REAL DEFAULT 0.0
    )""")
    
    # Transaction History Database Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        card_number TEXT,
        amount_paid REAL NOT NULL,
        vending_token TEXT,
        FOREIGN KEY(card_number) REFERENCES customer_accounts(card_number)
    )""")
    
    # Standard 19-digit UK Gas Card and 13-digit UK Electric Key formats
    mock_data = [
        ('John Doe', 'Gas', '9826123456789012345', 'British Gas', 15.50),
        ('Jane Smith', 'Electricity', '6502134567890', 'EDF Energy', 8.20)
    ]
    
    cursor.executemany("""
        INSERT OR IGNORE INTO customer_accounts (customer_name, utility_type, card_number, supplier_name, current_balance)
        VALUES (?, ?, ?, ?, ?)
    """, mock_data)
    
    conn.commit()
    conn.close()
    print("Database configured with baseline testing data profiles.")

if __name__ == "__main__":
    initialize_database()