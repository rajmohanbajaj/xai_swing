import numpy as np
import pandas as pd
from .env import TradingEnv

def sharpe_ratio(returns, rf=0.0, eps=1e-9):
    mu = np.mean(returns)
    sd = np.std(returns) + eps
    return (mu - rf) / sd * np.sqrt(252)

def max_drawdown(equity_curve):
    peak = -np.inf
    mdd = 0.0
    for v in equity_curve:
        peak = max(peak, v) if peak != -np.inf else v
        dd = (peak - v) / peak if peak > 0 else 0
        mdd = max(mdd, dd)
    return mdd

def run_backtest(model, df, features, cfg, log_csv: str = "artifacts/trades.csv"):
    env = TradingEnv(df, features, window=cfg.window,
                     commission_bps=cfg.commission_bps, slippage_bps=cfg.slippage_bps,
                     max_position=cfg.max_position)
    obs, _ = env.reset()
    done = False
    records = []
    t_index = df.index.tolist()

    while not done:
        action, _ = model.predict(obs, deterministic=True)
        obs, reward, done, _, info = env.step(int(action))
        date = t_index[env.t] if env.t < len(t_index) else t_index[-1]
        row = {"date": date, "reward": reward, "equity": info["equity"], "ret": info["ret"],
               "position": info["position"], "action": int(action)}
        # snapshot last-step features for explainability
        state_slice = df[cfg.features].iloc[env.t - cfg.window:env.t].copy()
        for c in cfg.features:
            row[f"{c}_t0"] = state_slice.iloc[-1][c]
        records.append(row)

    trades = pd.DataFrame(records).set_index("date")
    daily_ret = trades["equity"].pct_change().fillna(0.0)
    sr = sharpe_ratio(daily_ret.values)
    mdd = max_drawdown(trades["equity"].values)
    totals = {"cagr_like": trades["equity"].iloc[-1] - 1.0, "sharpe": sr, "max_dd": mdd}
    trades.to_csv(log_csv)
    return trades, totals
