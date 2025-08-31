from .config import Config
from .explain import fit_surrogate_and_explain

if __name__ == "__main__":
    cfg = Config()
    out = fit_surrogate_and_explain(
        cfg.trades_csv,
        getattr(cfg, "features", ["close_norm","volume","sma10","sma20","sma50","sma200",
                                  "ema20","ema50","adx","rsi14","macd","macd_sig",
                                  "stoch_k","stoch_d","bb_bw","vol_roll","ret1"]),
        cfg.explanations_csv,
        use_shap=cfg.use_shap,
        use_lime=cfg.use_lime,
        top_k=cfg.top_k_features
    )
    print(f"Explanations saved to: {cfg.explanations_csv}")
