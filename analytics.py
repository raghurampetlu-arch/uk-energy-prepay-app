import sqlite3
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def predict_days_remaining(current_balance, historical_readings=None):
    """
    Data Science Predictive Engine:
    Calculates energy burn rate using synthetic linear trends adjusted for UK winter/summer seasonality.
    """
    if historical_readings is None:
        np.random.seed(42)
        base_burn = np.random.normal(loc=3.50, scale=0.75, size=30) # Average £3.50 a day
        
        current_month = datetime.now().month
        season_factor = 1.4 if current_month in [11, 12, 1, 2, 3] else 0.8
        real_burn = base_burn * season_factor
    else:
        real_burn = np.array(historical_readings)
        
    df = pd.DataFrame(real_burn, columns=['daily_spend'])
    mean_burn_rate = df['daily_spend'].mean()
    
    if mean_burn_rate <= 0:
        mean_burn_rate = 3.50
        
    days_remaining = current_balance / mean_burn_rate
    depletion_date = datetime.now() + timedelta(days=float(days_remaining))
    
    return {
        "average_daily_burn_gbp": round(mean_burn_rate, 2),
        "estimated_days_left": round(days_remaining, 1),
        "predicted_depletion_date": depletion_date.strftime("%d %B %Y")
    }

def generate_spending_chart():
    """
    Data Visualization Engine:
    Queries the transaction database and renders a custom Matplotlib trend line.
    """
    print("[ANALYTICS ENGINE]: Querying database transactional matrices...")
    conn = sqlite3.connect("energy_app.db")
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT date(timestamp), SUM(amount_gbp) 
            FROM transactions 
            GROUP BY date(timestamp) 
            ORDER BY date(timestamp) ASC 
            LIMIT 10
        """)
        records = cursor.fetchall()
        
        # Fallback safeguard if the database is brand new
        if not records:
            print("[ANALYTICS ENGINE]: Database empty. Synthesizing visual trendlines...")
            dates = ["2026-09-20", "2026-09-21", "2026-09-22", "2026-09-23", "2026-09-24", "2026-09-25", "2026-09-26"]
            amounts = [20.0, 15.0, 30.0, 10.0, 25.0, 20.0, 40.0]
        else:
            dates = [row[0] for row in records]
            amounts = [row[1] for row in records]

        plt.figure(figsize=(6, 4.5), facecolor="#2A244E")
        ax = plt.axes()
        ax.set_facecolor("#1E1A3A")
        
        plt.plot(dates, amounts, color="cyan", marker="o", linewidth=2.5, markersize=6, label="Top-Up Spending")
        plt.fill_between(dates, amounts, color="cyan", alpha=0.15)
        
        plt.title("UK Smart Meter Spending Velocity", color="white", fontsize=12, fontweight="bold", pad=15)
        plt.xlabel("Settlement Date", color="#B3B0CD", fontsize=10, labelpad=10)
        plt.ylabel("Total Expenditure (£)", color="#B3B0CD", fontsize=10, labelpad=10)
        
        ax.tick_params(colors="white", labelsize=9)
        ax.spines['bottom'].color = '#B3B0CD'
        ax.spines['left'].color = '#B3B0CD'
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        plt.grid(True, linestyle="--", alpha=0.1, color="white")
        plt.xticks(rotation=25)
        plt.tight_layout()
        
        print("[ANALYTICS ENGINE]: Displaying graphical data window canvas...")
        plt.show()
        return True
        
    except Exception as e:
        print(f"[ANALYTICS ERROR]: Failed calculating charts: {e}")
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    # Test our prediction algorithm using a sample £45 balance profile
    prediction = predict_days_remaining(45.00)
    print("\n--- DATA SCIENCE PREDICTIVE RADAR ACTIVE ---")
    print(f"Average Household Burn Rate: £{prediction['average_daily_burn_gbp']}/day")
    print(f"Predicted Utility Lifespan: {prediction['estimated_days_left']} Days")
    print(f"Target Depletion Date: {prediction['predicted_depletion_date']}\n")
