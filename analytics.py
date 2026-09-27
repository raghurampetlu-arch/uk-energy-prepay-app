import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def predict_days_remaining(current_balance, historical_readings=None):
    """
    Data Science Predictive Engine:
    Calculates energy burn rate using synthetic linear trends adjusted for UK winter/summer seasonality.
    """
    # 1. Generate a baseline data matrix if no historical metrics are passed
    if historical_readings is None:
        # Mocking 30 days of standard UK household daily energy spend (in GBP)
        np.random.seed(42)
        base_burn = np.random.normal(loc=3.50, scale=0.75, size=30) # Average £3.50 a day
        
        # Apply a seasonal scaling factor (e.g., higher burn if it's winter)
        current_month = datetime.now().month
        season_factor = 1.4 if current_month in [11, 12, 1, 2, 3] else 0.8
        real_burn = base_burn * season_factor
    else:
        real_burn = np.array(historical_readings)
        
    # 2. Apply Pandas calculation tools to evaluate metrics
    df = pd.DataFrame(real_burn, columns=['daily_spend'])
    mean_burn_rate = df['daily_spend'].mean()
    
    # 3. Prevent mathematical division errors
    if mean_burn_rate <= 0:
        mean_burn_rate = 3.50
        
    # 4. Run the predictive calculation loop
    days_remaining = current_balance / mean_burn_rate
    depletion_date = datetime.now() + timedelta(days=float(days_remaining))
    
    return {
        "average_daily_burn_gbp": round(mean_burn_rate, 2),
        "estimated_days_left": round(days_remaining, 1),
        "predicted_depletion_date": depletion_date.strftime("%d %B %Y")
    }

if __name__ == "__main__":
    # Test our prediction algorithm using a sample £45 balance profile
    prediction = predict_days_remaining(45.00)
    print("\n--- DATA SCIENCE PREDICTIVE RADAR ACTIVE ---")
    print(f"Average Household Burn Rate: £{prediction['average_daily_burn_gbp']}/day")
    print(f"Predicted Utility Lifespan: {prediction['estimated_days_left']} Days")
    print(f"Target Depletion Date: {prediction['predicted_depletion_date']}\n")
