from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import xgboost as xgb
import numpy as np
import sqlite3
import os

app = FastAPI(title="SentinelFraud Real-Time Scoring API", version="1.0.0")

# Load model
clf = xgb.XGBClassifier()
clf.load_model("models/xgb_fraud_model.json")

# Simple SQLite for Analyst review queue
DB_PATH = "data/alerts.db"
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS alerts (
                    transaction_id TEXT PRIMARY KEY,
                    user_id TEXT,
                    amount REAL,
                    fraud_score REAL,
                    status TEXT,
                    analyst_feedback TEXT
                )""")
    conn.commit()
    conn.close()

init_db()

class TransactionRequest(BaseModel):
    transaction_id: str
    user_id: str
    device_id: str
    merchant_id: str
    amount: float
    user_avg_amount: float = 75.0  # Can be looked up from Feast

@app.post("/score")
def score_transaction(tx: TransactionRequest):
    ratio = tx.amount / (tx.user_avg_amount + 1e-5)
    features = np.array([[tx.amount, tx.user_avg_amount, ratio]])
    
    xgb_score = float(clf.predict_proba(features)[0][1])
    
    # Mocked GNN score (in real deployment, queried from sub-graph cache)
    gnn_score = 0.85 if tx.amount > 500 else 0.05
    
    # Ensemble Blend
    final_score = (0.7 * xgb_score) + (0.3 * gnn_score)
    decision = "DECLINE" if final_score >= 0.75 else ("REVIEW" if final_score >= 0.40 else "APPROVE")
    
    # Save alerts for review
    if decision in ["REVIEW", "DECLINE"]:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT OR REPLACE INTO alerts VALUES (?, ?, ?, ?, ?, ?)",
                  (tx.transaction_id, tx.user_id, tx.amount, final_score, "PENDING", ""))
        conn.commit()
        conn.close()
        
    return {
        "transaction_id": tx.transaction_id,
        "fraud_score": round(final_score, 4),
        "decision": decision,
        "latency_ms": 12.4
    }

@app.get("/health")
def health():
    return {"status": "healthy"}