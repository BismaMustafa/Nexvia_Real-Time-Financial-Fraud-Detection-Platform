def blend_scores(xgb_prob: float, gnn_risk: float, alpha: float = 0.65) -> float:
    """
    Combines tabular features risk with relational graph fraud-ring risk.
    """
    final_score = (alpha * xgb_prob) + ((1.0 - alpha) * gnn_risk)
    return round(float(final_score), 4)