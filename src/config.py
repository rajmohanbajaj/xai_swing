from dataclasses import dataclass

@dataclass
class Config:
    # Data
    ticker: str = "SPY"            # e.g., 'SPY' or ASX ETFs: 'VAS.AX', 'IOZ.AX'
    start: str = "2013-01-01"
    end: str   = "2025-08-01"
    cache_csv: str = "data/{ticker}.csv"

    # Features / window
    window: int = 20               # lookback days encoded into state
    use_pct_returns: bool = True

    # Trading costs (per side, in bps)
    commission_bps: float = 10.0   # 0.10% per side
    slippage_bps: float = 3.0      # 0.03% per side
    max_position: int = 1          # positions allowed in {-1,0,+1}

    # RL training
    total_timesteps: int = 150_000
    seed: int = 42
    model_path: str = "artifacts/model.zip"

    # Explainability
    use_shap: bool = True
    use_lime: bool = False
    top_k_features: int = 5

    # Outputs
    artifacts_dir: str = "artifacts"
    trades_csv: str = "artifacts/trades.csv"
    explanations_csv: str = "artifacts/explanations.csv"
    plots_dir: str = "artifacts/plots"
