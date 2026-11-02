import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_recall_curve, auc, roc_auc_score, classification_report
import mlflow
import mlflow.xgboost

def train():
    mlflow.set_experiment("SentinelFraud_XGBoost")
    df = pd.read_parquet("data/transactions.parquet")
    
    features = ["amount", "user_avg_amount", "amount_to_avg_ratio"]
    X = df[features]
    y = df["is_fraud"]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, stratify=y, random_state=42)
    
    # Calculate scale_pos_weight for imbalance
    pos_weight = (len(y_train) - sum(y_train)) / (sum(y_train) + 1e-5)
    
    with mlflow.start_run():
        params = {
            "n_estimators": 150,
            "max_depth": 5,
            "learning_rate": 0.05,
            "scale_pos_weight": float(pos_weight),
            "eval_metric": "aucpr",
            "random_state": 42
        }
        
        clf = xgb.XGBClassifier(**params)
        clf.fit(X_train, y_train)
        
        preds_proba = clf.predict_proba(X_test)[:, 1]
        
        # PR-AUC Calculation
        precision, recall, _ = precision_recall_curve(y_test, preds_proba)
        pr_auc = auc(recall, precision)
        roc_auc = roc_auc_score(y_test, preds_proba)
        
        # Log params & metrics
        mlflow.log_params(params)
        mlflow.log_metric("pr_auc", pr_auc)
        mlflow.log_metric("roc_auc", roc_auc)
        
        clf.save_model("models/xgb_fraud_model.json")
        mlflow.xgboost.log_model(clf, artifact_path="model")
        
        print(f"Model Trained! Test PR-AUC: {pr_auc:.4f} | ROC-AUC: {roc_auc:.4f}")

if __name__ == "__main__":
    train()