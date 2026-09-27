import sqlite3
import re

ANALYTICS_DB = "analytics_warehouse.db"

def validate_uk_mobile(phone_number):
    """Returns True if the string matches a standard UK mobile configuration format."""
    if not phone_number:
        return False
    cleaned = re.sub(r'[\s\-() ]', '', str(phone_number))
    uk_pattern = r'^(?:(?:\+44|44)7\d{9}$|07\d{9})$'
    return bool(re.match(uk_pattern, cleaned))

def run_etl_processing(raw_payload):
    """
    Data Quality Gate: Filters out international entries 
    and loads clean records into the Analytics Warehouse.
    """
    service_type = raw_payload.get("service_type")
    identifier = raw_payload.get("user_id", "")
    
    # 1. Drop regional forbidden services completely
    forbidden_services = ["FASTag", "UPI", "Paytm"]
    if service_type in forbidden_services:
        print(f"❌ [DATA QUALITY REJECTION]: Dropped '{service_type}' transaction. Region not supported.")
        return False

    # 2. Reject if it's a mobile top-up but fails the UK phone format regex
    if service_type == "Mobile":
        if not validate_uk_mobile(identifier):
            print(f"❌ [DATA QUALITY REJECTION]: '{identifier}' failed UK mobile formatting boundaries.")
            return False

    # 3. If it passes validation, load it into the warehouse tables
    conn = sqlite3.connect(ANALYTICS_DB)
    cursor = conn.cursor()
    try:
        # Load User Dimension
        cursor.execute("""
            INSERT INTO dim_users (user_id, first_seen_location, preferred_device)
            VALUES (?, ?, ?) ON CONFLICT(user_id) DO UPDATE SET preferred_device=excluded.preferred_device
        """, (raw_payload["user_id"], raw_payload["location"], raw_payload["device_type"]))
        
        cursor.execute("SELECT user_key FROM dim_users WHERE user_id = ?", (raw_payload["user_id"],))
        user_key = cursor.fetchone()[0]

        # Load Service Dimension
        cursor.execute("""
            INSERT INTO dim_services (service_type, supplier_name)
            VALUES (?, ?) ON CONFLICT(service_type, supplier_name) DO NOTHING
        """, (raw_payload["service_type"], raw_payload["supplier_name"]))
        
        cursor.execute("SELECT service_key FROM dim_services WHERE service_type = ? AND supplier_name = ?", 
                       (raw_payload["service_type"], raw_payload["supplier_name"]))
        service_key = cursor.fetchone()[0]

        # Load into core Fact metrics table
        cursor.execute("""
            INSERT INTO fact_transactions (transaction_id, timestamp, user_key, service_key, amount, status)
            VALUES (?, ?, ?, ?, ?, ?) ON CONFLICT(transaction_id) DO NOTHING
        """, (raw_payload["transaction_id"], raw_payload["timestamp"], user_key, service_key, raw_payload["amount"], raw_payload["status"]))
        
        conn.commit()
        print(f"✅ [ETL PIPELINE]: Successfully processed and loaded UK {service_type} transaction.")
        return True
    except Exception as e:
        print(f"❌ [PIPELINE ERROR]: Failed loading data: {e}")
        return False
    finally:
        conn.close()
