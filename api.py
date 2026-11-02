from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import uvicorn

# FastAPI app initialize karna
app = FastAPI(title="Real-Time Fraud Detection API", description="Predicts fraudulent transactions")

# User se aane wale data ka structure define karna (Pydantic Model)
class Transaction(BaseModel):
    TransactionAmt: float
    card1_mean_amt: float
    amt_vs_mean: float
    card1_freq: int
    hour_of_day: float

@app.post("/predict")
def predict_fraud(data: Transaction):
    # API data ko DataFrame mein convert karna
    input_data = pd.DataFrame([data.model_dump()])
    
    # Note: Production mein yahan hum MLflow se saved XGBoost/GNN model load karte hain.
    # Abhi API test karne ke liye hum ek rule-based logic laga rahe hain:
    # Agar user apni normal average spending se 3 guna (3x) zyada badi transaction kare, toh usay fraud flag karein
    is_fraud = bool(data.amt_vs_mean > 3.0)
    risk_score = 0.85 if is_fraud else 0.12
    
    return {
        "status": "success",
        "prediction": "Fraudulent" if is_fraud else "Legitimate",
        "risk_probability": risk_score,
        "input_features": data.model_dump()
    }

@app.get("/")
def home():
    return {"message": "Fraud Detection API is running. Go to /docs to test it."}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)