from .config import Config
from .data import fetch_and_engineer
from .agent import train_agent

if __name__ == "__main__":
    cfg = Config()
    bundle = fetch_and_engineer(cfg.ticker, cfg.start, cfg.end, cfg.cache_csv,
                                use_pct_returns=cfg.use_pct_returns)
    # stash features into cfg for reuse
    cfg.features = bundle.features  # dynamic add
    train_agent(bundle.df, bundle.features, cfg)
    print(f"Model saved to: {cfg.model_path}")
