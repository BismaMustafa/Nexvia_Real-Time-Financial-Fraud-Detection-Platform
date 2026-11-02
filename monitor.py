import pandas as pd
from scipy.stats import ks_2samp

print("Loading data for monitoring...")
# Ensure karein ke fraud_features.parquet aapke current folder ke is path par maujood ho
df = pd.read_parquet('D:/fraud_detection/feature_repo/feature_repo/data/fraud_features.parquet')

features = ['TransactionAmt', 'card1_mean_amt', 'amt_vs_mean', 'card1_freq', 'hour_of_day']

# Reference (purana) aur Current (naya) data alag karna
reference_data = df[features].iloc[:5000].dropna()
current_data = df[features].iloc[5000:10000].dropna()

print("\n--- Real-Time Data Drift Report ---")
drift_found = False

# Kolmogorov-Smirnov (KS) Test se har feature mein drift check karna
for feature in features:
    stat, p_value = ks_2samp(reference_data[feature], current_data[feature])
    
    # Agar p-value 0.05 se kam hai, toh data drift (changes) detect hua hai
    if p_value < 0.05:
        print(f"⚠️ Drift Detected in: {feature} (p-value: {p_value:.4f})")
        drift_found = True
    else:
        print(f"✅ Normal: {feature} (p-value: {p_value:.4f})")

if drift_found:
    print("\nWarning: Data change ho gaya hai, model ko dobara train karne ki zaroorat pad sakti hai!")
else:
    print("\nAll good! Data mein koi major drift nahi hai.")