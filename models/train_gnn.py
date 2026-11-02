import torch
import torch.nn.functional as F
from torch_geometric.data import Data
from torch_geometric.nn import SAGEConv
import pandas as pd
import numpy as np

class FraudRingGNN(torch.nn.Module):
    def __init__(self, in_channels, hidden_channels):
        super().__init__()
        self.conv1 = SAGEConv(in_channels, hidden_channels)
        self.conv2 = SAGEConv(hidden_channels, 1)

    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index)
        x = F.relu(x)
        x = self.conv2(x, edge_index)
        return torch.sigmoid(x)

def build_graph_and_train():
    df = pd.read_parquet("data/transactions.parquet").head(5000)
    
    unique_users = df["user_id"].unique().tolist()
    unique_devs = df["device_id"].unique().tolist()
    
    user_map = {u: i for i, u in enumerate(unique_users)}
    dev_map = {d: i + len(unique_users) for i, d in enumerate(unique_devs)}
    
    src = [user_map[u] for u in df["user_id"]]
    dst = [dev_map[d] for d in df["device_id"]]
    
    # Undirected edges
    edge_index = torch.tensor([src + dst, dst + src], dtype=torch.long)
    
    num_nodes = len(unique_users) + len(unique_devs)
    # Simple feature vector: [out_degree, placeholder_amount]
    x = torch.ones((num_nodes, 4), dtype=torch.float)
    
    # Ground truth labels for user nodes
    labels = torch.zeros(num_nodes, 1)
    for _, row in df.iterrows():
        if row["is_fraud"] == 1:
            labels[user_map[row["user_id"]]] = 1.0

    data = Data(x=x, edge_index=edge_index, y=labels)
    
    model = FraudRingGNN(in_channels=4, hidden_channels=16)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
    
    # Positive weight for binary loss
    pos_weight = torch.tensor([10.0])
    criterion = torch.nn.BCEWithLogitsLoss(pos_weight=pos_weight)
    
    model.train()
    for epoch in range(40):
        optimizer.zero_grad()
        out = model(data.x, data.edge_index)
        loss = criterion(out[:len(unique_users)], data.y[:len(unique_users)])
        loss.backward()
        optimizer.step()
        
    torch.save(model.state_dict(), "models/gnn_fraud_ring.pt")
    print("GNN Fraud Ring Model successfully trained & saved.")

if __name__ == "__main__":
    build_graph_and_train()