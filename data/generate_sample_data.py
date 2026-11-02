import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_fraud_data(n_rows=20000):
    np.random.seed(42)
    now = datetime.utcnow()
    
    user_ids = [f"USER_{i:04d}" for i in range(1, 501)]
    device_ids = [f"DEV_{i:04d}" for i in range(1, 250)]
    merchant_ids = [f"MERCH_{i:03d}" for i in range(1, 80)]
    
    rows = []
    for i in range(n_rows):
        uid = np.random.choice(user_ids)
        dev = np.random.choice(device_ids)
        merch = np.random.choice(merchant_ids)
        amt = np.random.exponential(scale=65.0) + 5.0
        
        # Inject heavy imbalance (~0.8% fraud)
        is_fraud = 0
        if np.random.rand() < 0.008:
            is_fraud = 1
            amt *= np.random.uniform(5.0, 15.0)  # Fraud spike
            
        timestamp = now - timedelta(minutes=np.random.randint(0, 10000))
        
        rows.append({
            "transaction_id": f"TX_{i:07d}",
            "user_id": uid,
            "device_id": dev,
            "merchant_id": merch,
            "amount": round(float(amt), 2),
            "timestamp": timestamp,
            "is_fraud": is_fraud
        })
        
    df = pd.DataFrame(rows).sort_values("timestamp").reset_index(drop=True)
    
    # Feature Engineering: User avg amount, rolling velocity
    user_stats = df.groupby("user_id")["amount"].agg(user_avg_amount="mean").reset_index()
    df = df.merge(user_stats, on="user_id", how="left")
    df["amount_to_avg_ratio"] = df["amount"] / (df["user_avg_amount"] + 1e-5)
    
    df.to_parquet("data/transactions.parquet")
    print(f"Generated {len(df)} transactions. Fraud rate: {df['is_fraud'].mean()*100:.2f}%")

if __name__ == "__main__":
    import os
    os.makedirs("data", exist_ok=True)
    generate_fraud_data()