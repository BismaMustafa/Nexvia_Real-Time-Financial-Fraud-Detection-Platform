import json
import time
import pandas as pd
from kafka import KafkaProducer

def stream_transactions():
    producer = KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    df = pd.read_parquet("data/transactions.parquet")
    print("Starting transaction replay into Kafka topic 'transactions'...")
    
    for _, row in df.iterrows():
        tx_dict = {
            "transaction_id": row["transaction_id"],
            "user_id": row["user_id"],
            "device_id": row["device_id"],
            "merchant_id": row["merchant_id"],
            "amount": float(row["amount"]),
            "timestamp": str(row["timestamp"])
        }
        producer.send('transactions', value=tx_dict)
        time.sleep(0.1) # Simulate real-time stream

if __name__ == "__main__":
    stream_transactions()