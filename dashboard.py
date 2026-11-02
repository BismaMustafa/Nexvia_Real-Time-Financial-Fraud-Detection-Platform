import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import requests
import time
import random
from datetime import datetime

st.set_page_config(page_title="SecureNet Fraud AI", page_icon="🛡️", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #0f172a; color: #cbd5e1; }
    .card { background-color: #1e293b; padding: 20px; border-radius: 10px; border: 1px solid #334155; margin-bottom: 20px; }
    .scan-box { text-align: center; padding: 40px; background-color: #0f172a; border-radius: 15px; border: 2px solid #3b82f6; }
    .success-text { color: #10b981; font-size: 24px; font-weight: bold; }
    .alert-text { color: #ef4444; font-size: 24px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- DYNAMIC SESSION STATE ---
if 'view' not in st.session_state: st.session_state.view = 'dashboard'
if 'txn_history' not in st.session_state:
    st.session_state.txn_history = [{"Txn ID": "#98421-FX", "Amount": "$1,240.00", "Risk": 8, "Status": "Review"}]
if 'time_data' not in st.session_state:
    st.session_state.time_data = [f"{i}:00" for i in range(8, 16)]
if 'vol_data' not in st.session_state:
    st.session_state.vol_data = [120, 150, 110, 220, 180, 260, 210, 290]
if 'anomaly_data' not in st.session_state:
    st.session_state.anomaly_data = [10, 15, 8, 45, 12]

# --- SIDEBAR ---
with st.sidebar:
    st.title("🛡️ SecureNet AI")
    st.divider()
    amount = st.number_input("Amount ($)", value=1240.0)
    mean_amt = st.number_input("Avg Spend ($)", value=800.0)
    freq = st.slider("24h Frequency", 1, 20, 2)
    hour = st.slider("Hour of Day", 0, 23, 11)
    
    if st.button("🔍 Analyze Transaction", use_container_width=True, type="primary"):
        st.session_state.payload = {"TransactionAmt": amount, "card1_mean_amt": mean_amt, "amt_vs_mean": amount/mean_amt if mean_amt>0 else 0, "card1_freq": freq, "hour_of_day": hour}
        st.session_state.current_amt = amount
        st.session_state.view = 'scanning'
        st.rerun()

# --- SCANNING VIEW ---
if st.session_state.view == 'scanning':
    st.markdown("<div class='scan-box'>", unsafe_allow_html=True)
    txn_id = f"#{random.randint(10000, 99999)}-AI"
    st.subheader(f"🔄 TRANSACTION ANALYSIS: {txn_id}")
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    for i, step in enumerate(["Scanning Database...", "Analyzing IP...", "Behavioral Check...", "Velocity Check..."]):
        status_text.markdown(f"**{step}**")
        progress_bar.progress((i + 1) * 25)
        time.sleep(0.5)
        
    try:
        response = requests.post("http://localhost:30000/predict", json=st.session_state.payload)
        if response.status_code == 200:
            pred = response.json().get("prediction")
            st.divider()
            
            if pred == "Fraudulent":
                st.markdown("<p class='alert-text'>❌ FRAUD DETECTED</p>", unsafe_allow_html=True)
                st.session_state.txn_history.insert(0, {"Txn ID": txn_id, "Amount": f"${st.session_state.current_amt}", "Risk": random.randint(90, 99), "Status": "Blocked"})
                st.session_state.anomaly_data[-1] += 25  # Bar chart ko update karega
            else:
                st.markdown("<p class='success-text'>✅ TRANSACTION SAFE</p>", unsafe_allow_html=True)
                st.session_state.txn_history.insert(0, {"Txn ID": txn_id, "Amount": f"${st.session_state.current_amt}", "Risk": random.randint(1, 15), "Status": "Passed"})
            
            # SLIDING WINDOW UPDATE
            st.session_state.time_data.append(datetime.now().strftime("%H:%M:%S"))
            st.session_state.vol_data.append(random.randint(300, 500))
            st.session_state.time_data = st.session_state.time_data[-8:]
            st.session_state.vol_data = st.session_state.vol_data[-8:]
            
        else: st.warning("API Failed.")
    except Exception as e: st.error(f"Error: {e}")
        
    if st.button("⬅️ Back to Dashboard"):
        st.session_state.view = 'dashboard'
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# --- DASHBOARD VIEW ---
elif st.session_state.view == 'dashboard':
    st.title("Real-Time Monitor")
    
    # ROW 1
    r1c1, r1c2 = st.columns([1.5, 1])
    with r1c1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("📈 Live Transaction Volume")
        fig_line = go.Figure(go.Scatter(x=st.session_state.time_data, y=st.session_state.vol_data, mode='lines+markers', line=dict(color='#3b82f6', width=3)))
        fig_line.update_layout(height=250, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(t=10, b=10, l=10, r=10))
        st.plotly_chart(fig_line, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with r1c2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("📋 Live Transactions")
        st.dataframe(pd.DataFrame(st.session_state.txn_history), hide_index=True, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    # ROW 2 (Restored Charts)
    r2c1, r2c2 = st.columns(2)
    with r2c1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("🍩 Transaction Types")
        fig_donut = px.pie(values=[56.5, 26.5, 10.0, 7.0], names=['E-commerce', 'Wire', 'POS', 'Crypto'], hole=0.6, color_discrete_sequence=['#3b82f6', '#ef4444', '#10b981', '#f59e0b'])
        fig_donut.update_layout(height=250, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(t=10, b=10, l=10, r=10))
        st.plotly_chart(fig_donut, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with r2c2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("📊 User Behavior Anomaly")
        fig_bar = go.Figure(data=[go.Bar(x=['Mon', 'Tue', 'Wed', 'Thu', 'Fri'], y=st.session_state.anomaly_data, marker_color='#10b981')])
        fig_bar.update_layout(height=250, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(t=10, b=10, l=10, r=10))
        st.plotly_chart(fig_bar, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)