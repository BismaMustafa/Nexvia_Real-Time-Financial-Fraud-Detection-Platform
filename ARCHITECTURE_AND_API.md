# 🏗️ Nexvia Platform - System Architecture & API Documentation

This document covers the complete system architecture, data flow, and REST API specification for the **Nexvia Real-Time Financial Fraud Detection Platform**.

---

## 1. System Architecture & Data Flow

Below is the communication flow between the Streamlit SOC UI and the FastAPI backend engine:

```text
+-------------------+      HTTP POST Request      +------------------------+
|  Streamlit UI     |  ----------------------->   | FastAPI Prediction     |
| (dashboard.py)    |    (<50ms Payload JSON)     | Engine (Port 30000)    |
|                   |                             |                        |
|  - SOC Dark UI    |      JSON Risk Response     |  - XGBoost Model       |
|  - Live Charts    |  <-----------------------   |  - GNN Anomaly Engine  |
+-------------------+                             +------------------------+
          |                                                    |
          v                                                    v
  [ High-Performance ]                              [ Local Kubernetes ]
  [  Real-Time View  ]                              [ Docker Microservice]



Data Flow Steps:
User Interaction: The SOC analyst or live stream triggers transactions on the Streamlit dashboard (dashboard.py).

API Request: The frontend packages transaction features (TransactionAmt, amt_vs_mean, hour_of_day, etc.) and sends an HTTP POST request to the backend.

Model Inference: FastAPI processes the request, running the features through XGBoost and GNN anomaly detection models in under 50 milliseconds.

Response & UI Update: The backend returns a JSON payload containing the risk score and classification (Legitimate or Fraudulent), instantly updating the SOC command center.

2. Complete API Documentation
The frontend dashboard connects seamlessly with our backend prediction engine via the following REST API endpoint:

Endpoint URL: http://localhost:30000/predict

HTTP Method: POST

Content-Type: application/json

Request Payload (Input Data Schema):
JSON
{
  "TransactionAmt": 1240.0,
  "card1_mean_amt": 800.0,
  "amt_vs_mean": 1.55,
  "card1_freq": 2,
  "hour_of_day": 11
}
Response Payload (Output Data Schema):
JSON
{
  "prediction": "Legitimate",
  "risk_score": 8,
  "status_code": 200
}





# Architecture diagram
<img width="1213" height="616" alt="fraud detection" src="https://github.com/user-attachments/assets/9b442398-be43-46f3-b589-40681f12ad55" />
