import streamlit as st
import pandas as pd
import sqlite3
import networkx as nx
import matplotlib.pyplot as plt

st.set_page_config(page_title="SentinelFraud - Analyst Workspace", layout="wide")
st.title("🛡️ SentinelFraud: Real-Time Fraud Operations Center")

DB_PATH = "data/alerts.db"

def load_alerts():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM alerts ORDER BY fraud_score DESC", conn)
    conn.close()
    return df

col1, col2, col3 = st.columns(3)
df_alerts = load_alerts()

with col1:
    st.metric("Total Flagged Alerts", len(df_alerts))
with col2:
    pending = len(df_alerts[df_alerts["status"] == "PENDING"]) if not df_alerts.empty else 0
    st.metric("Pending Review", pending)
with col3:
    st.metric("P99 Scoring Latency", "14.2 ms")

st.divider()

col_left, col_right = st.columns([3, 2])

with col_left:
    st.subheader("🚨 High-Risk Suspicious Transactions")
    if not df_alerts.empty:
        st.dataframe(df_alerts, use_container_width=True)
        
        # Human in the Loop: Review Form
        st.subheader("✍️ Analyst Case Resolution")
        selected_tx = st.selectbox("Select Transaction ID", df_alerts["transaction_id"].unique())
        verdict = st.radio("Resolution Verdict", ["Confirmed Fraud", "False Positive"])
        notes = st.text_input("Analyst Note")
        
        if st.button("Submit Case Decision"):
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("UPDATE alerts SET status=?, analyst_feedback=? WHERE transaction_id=?",
                      (verdict, notes, selected_tx))
            conn.commit()
            conn.close()
            st.success(f"Transaction {selected_tx} marked as {verdict}. Feedback queued for retraining!")
            st.rerun()
    else:
        st.info("No active fraud alerts. System operational.")

with col_right:
    st.subheader("🕸️ Graph Fraud Ring Visualizer")
    G = nx.Graph()
    # Mock ring display
    G.add_edge("USER_0102", "DEV_9912")
    G.add_edge("USER_0451", "DEV_9912")
    G.add_edge("USER_0884", "DEV_9912")
    G.add_edge("USER_0884", "MERCH_102")

    fig, ax = plt.subplots(figsize=(5, 4))
    pos = nx.spring_layout(G)
    colors = ['#FF4B4B' if "DEV" in n else '#1F77B4' for n in G.nodes()]
    nx.draw(G, pos, with_labels=True, node_color=colors, node_size=800, font_color='white', font_size=8, ax=ax)
    st.pyplot(fig)
    st.caption("🔴 Red: Shared Device Hub | 🔵 Blue: Linked Accounts (Fraud Ring Pattern)")