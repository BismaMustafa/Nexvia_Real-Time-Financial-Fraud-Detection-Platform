
# 🛡️ Nexvia Real-Time Financial Fraud Detection Platform

An enterprise-grade, real-time financial fraud detection and Security Operations Center (SOC) command center engineered for **Nexvia**. This platform integrates machine learning anomaly detection (XGBoost & GNN), a FastAPI scoring backend hosted on local Kubernetes, and a high-performance interactive Streamlit dark-mode dashboard.

---

## 🚀 Key Features
* **Real-Time Risk Scoring:** Analyzes transaction behavioral anomalies instantly (<50ms latency).
* **SOC Dark Command Center:** Features animated scanning states, sliding volume live charts, transaction type donuts, and behavioral anomaly threat tracking.
* **Kubernetes & FastAPI Backend:** Scalable microservice architecture handling live transaction requests.
* **Automated Threat Blocking:** Instantly flags, scores, and blocks high-risk fraudulent transactions before funds leave the account.

---

## 🛠️ Tech Stack
* **Core Logic:** Python, Pandas, NumPy, PyArrow
* **Machine Learning:** XGBoost, Graph Neural Networks (GNN)
* **Backend & Deployment:** FastAPI, Docker, Local Kubernetes (Minikube/Kind)
* **Frontend:** Streamlit, Plotly (Interactive SOC Dark UI)

---

## 📂 Project Structure
```text
Nexvia_Real-Time-Financial-Fraud-Detection-Platform/
├── dashboard.py         # Streamlit SOC Command Center UI
├── requirements.txt     # Python dependencies
├── .gitignore           # Excludes venv, model binaries, and caches
└── README.md            # Project Documentation
