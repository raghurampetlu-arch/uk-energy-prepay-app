import sqlite3
import random

DB_NAME = "app_database.db"

def initialize_database():
    """Initializes and updates the database schema for all utilities and mobile top-ups."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # 1. Create/Update the customer accounts table with expanded utility categories
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customer_accounts (
        account_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_name TEXT NOT NULL,
        utility_type TEXT CHECK(utility_type IN ('Gas', 'Electricity', 'Mobile', 'Water', 'Broadband')),
        card_number TEXT UNIQUE NOT NULL,
        supplier_name TEXT NOT NULL,
        phone_number TEXT,
        current_balance REAL DEFAULT 0.0
    );
    """)
    
    # 2. Create the transactions table to log all prepayments
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        card_number TEXT,
        amount_paid REAL NOT NULL,
        vending_token TEXT,
        FOREIGN KEY(card_number) REFERENCES customer_accounts(card_number)
    );
    """)
    
    conn.commit()
    conn.close()
    print("[DATABASE]: Core systems and Mobile Top-up modules initialized successfully.")


def register_new_account(name, utility_type, card_num, supplier, phone=None):
    """Registers any type of utility or mobile account into the system."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO customer_accounts (customer_name, utility_type, card_number, supplier_name, phone_number, current_balance)
            VALUES (?, ?, ?, ?, ?, 0.0)
        """, (name, utility_type, card_num, supplier, phone))
        conn.commit()
        return True
    except sqlite3.IntegrityError as e:
        print(f"[DATABASE ERROR]: Could not register account: {e}")
        return False
    finally:
        conn.close()


def process_service_topup(identifier, amount, is_mobile=False):
    """Handles balance updates and logs transactions."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    if is_mobile:
        cursor.execute("SELECT card_number, current_balance, supplier_name FROM customer_accounts WHERE phone_number = ?", (identifier,))
    else:
        cursor.execute("SELECT card_number, current_balance, supplier_name FROM customer_accounts WHERE card_number = ?", (identifier,))
        
    account = cursor.fetchone()
    
    if not account:
        conn.close()
        return {"status": "Error", "message": "Account or Phone Number not found."}
        
    card_number, current_balance, supplier_name = account
    new_balance = current_balance + float(amount)
    
    if is_mobile:
        cursor.execute("UPDATE customer_accounts SET current_balance = ? WHERE phone_number = ?", (new_balance, identifier))
    else:
        cursor.execute("UPDATE customer_accounts SET current_balance = ? WHERE card_number = ?", (new_balance, identifier))
    
    voucher_pin = f"PIN-{''.join(str(random.randint(0,9)) for _ in range(12))}"
    
    cursor.execute("""
        INSERT INTO transactions (card_number, amount_paid, vending_token)
        VALUES (?, ?, ?)
    """, (card_number, amount, voucher_pin))
    
    conn.commit()
    conn.close()
    
    return {
        "status": "Success",
        "new_balance": new_balance,
        "voucher_pin": voucher_pin,
        "supplier": supplier_name
    }

# 🚨 ALIAS: This explicitly maps the name the frontend is looking for
execute_topup = process_service_topup
