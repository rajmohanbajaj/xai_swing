from .config import Config
from .data import fetch_and_engineer
from .agent import load_agent
from .backtest import run_backtest
from .visualize import plot_equity
import os

if __name__ == "__main__":
    cfg = Config()
    bundle = fetch_and_engineer(cfg.ticker, cfg.start, cfg.end, cfg.cache_csv,
                                use_pct_returns=cfg.use_pct_returns)
    cfg.features = bundle.features

    model = load_agent(cfg.model_path)
    trades, totals = run_backtest(model, bundle.df, bundle.features, cfg, log_csv=cfg.trades_csv)
    print("Metrics:", totals)
    os.makedirs(cfg.plots_dir, exist_ok=True)
    plot_equity(trades, f"{cfg.plots_dir}/equity_curve.png")
    print(f"Trades saved to: {cfg.trades_csv}")
