import sqlite3

def verify_data_warehouse():
    """
    Connects to the analytics warehouse and runs reporting aggregates 
    to confirm data ingestion and data quality gates are operating properly.
    """
    db_path = "analytics_warehouse.db"
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("\n" + "="*50)
        print("🏛️  ANALYTICS WAREHOUSE INTEGRITY REPORT")
        print("="*50)
        
        # 1. Check Total Logged Volume
        cursor.execute("SELECT COUNT(*) FROM fact_transactions;")
        total_records = cursor.fetchone()[0]
        print(f"📈 Total Transactions Ingested: {total_records}")
        
        # 2. Check Unique Tracked Profiles
        cursor.execute("SELECT COUNT(*) FROM dim_users;")
        total_users = cursor.fetchone()[0]
        print(f"👥 Unique Customer Profiles Created: {total_users}")
        
        # 3. Revenue Business Summary Aggregations
        print("\n💰 Gross Financial Volumetrics (Grouped by UK Service Category):")
        cursor.execute("""
            SELECT s.service_type, COUNT(f.fact_id), SUM(f.amount)
            FROM fact_transactions f
            JOIN dim_services s ON f.service_key = s.service_key
            GROUP BY s.service_type;
        """)
        summary_rows = cursor.fetchall()
        
        if not summary_rows:
            print("   (No data found yet. Ensure your streamer or frontend app has submitted transactions!)")
        else:
            for row in summary_rows:
                service, orders, total_amount = row
                print(f" 🔹 {service:<15} | Orders Processed: {orders:<4} | Total Value: £{total_amount:,.2f}")
                
        # 4. Check Data Quality Constraints (Verifying No Non-UK data sneaked in)
        print("\n🛡️  Data Quality Validation Integrity Audit:")
        cursor.execute("""
            SELECT COUNT(*) FROM dim_services 
            WHERE service_type IN ('FASTag', 'UPI', 'Paytm');
        """)
        forbidden_services_count = cursor.fetchone()[0]
        
        if forbidden_services_count == 0:
            print(" ✅ SUCCESS: 0 non-UK regional payment methods found in catalog.")
        else:
            print(f" ⚠️ ALERT: Detected {forbidden_services_count} forbidden non-UK services in database.")
            
        conn.close()
        print("="*50 + "\n")
        
    except sqlite3.OperationalError:
        print(f"❌ ERROR: Could not find database file '{db_path}'.")
        print("   Please run your application or data_streamer.py first to create it.")

if __name__ == "__main__":
    verify_data_warehouse()
