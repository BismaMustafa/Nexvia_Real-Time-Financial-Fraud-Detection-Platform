import pandas as pd
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset

def check_data_drift():
    df = pd.read_parquet("data/transactions.parquet")
    
    # Split into Reference (baseline) & Current (production window)
    reference = df.iloc[:10000][["amount", "user_avg_amount", "amount_to_avg_ratio"]]
    current = df.iloc[10000:][["amount", "user_avg_amount", "amount_to_avg_ratio"]]
    
    report = Report(metrics=[DataDriftPreset()])
    report.run(reference_data=reference, current_data=current)
    
    report.save_html("monitoring/data_drift_report.html")
    print("Evidently Data Drift report generated -> monitoring/data_drift_report.html")
    
    # Extract drift flag logic
    result = report.as_dict()
    dataset_drift = result["metrics"][0]["result"]["dataset_drift"]
    
    if dataset_drift:
        print("⚠️ Data Drift detected! Triggering automatic model retraining pipeline...")
        # os.system("python models/train_xgboost.py")
    else:
        print("✅ No significant drift detected. Model is stable.")

if __name__ == "__main__":
    check_data_drift()