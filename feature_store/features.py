from datetime import timedelta
from feast import Entity, Field, FeatureView, FileSource
from feast.types import Float32, String

source = FileSource(
    name="tx_source",
    path="data/transactions.parquet",
    timestamp_field="timestamp"
)

user_entity = Entity(name="user_id", value_type=String, description="Account holder ID")

user_tx_features = FeatureView(
    name="user_transaction_features",
    entities=[user_entity],
    ttl=timedelta(days=30),
    schema=[
        Field(name="user_avg_amount", dtype=Float32),
        Field(name="amount_to_avg_ratio", dtype=Float32)
    ],
    online=True,
    source=source
)