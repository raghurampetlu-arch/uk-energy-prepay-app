import time
import random
import uuid
from datetime import datetime
from etl_pipeline import run_etl_processing

# A mix of correct UK data and invalid entries to showcase data quality checking
SERVICES = ["Gas", "Electricity", "Mobile", "Water", "Broadband", "FASTag"]
SUPPLIERS = ["British Gas", "O2", "EE", "Octopus Energy", "Vodafone", "Unknown India Vendor"]

if __name__ == "__main__":
    print("🚀 [STREAMER]: Initializing live transaction stream engine...")
    try:
        while True:
            # Generate random test configurations
            is_valid_uk_phone = random.choice(["07123456789", "+447987654321", "919876543210 (India)", "Invalid-Text-Input"])
            chosen_service = random.choice(SERVICES)
            
            payload = {
                "transaction_id": str(uuid.uuid4()),
                "timestamp": datetime.utcnow().isoformat(),
                "user_id": is_valid_uk_phone if chosen_service == "Mobile" else f"CARD-{random.randint(1000,9999)}",
                "service_type": chosen_service,
                "supplier_name": random.choice(SUPPLIERS),
                "amount": round(random.uniform(5.0, 100.0), 2),
                "status": "SUCCESS",
                "device_type": "Automated Stream Emulator",
                "location": random.choice(["London", "Manchester", "Birmingham", "Mumbai"])
            }
            
            # Pipe straight into your ETL processor
            run_etl_processing(payload)
            time.sleep(0.5) # Emulate a constant steady transactional ingestion load
    except KeyboardInterrupt:
        print("\n🛑 Stream stopped.")
