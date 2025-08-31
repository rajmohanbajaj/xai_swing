import os
import numpy as np
import pandas as pd
from xgboost import XGBClassifier
import shap
from lime.lime_tabular import LimeTabularExplainer

FAMILY_MAP = {
    "Trend": ["sma10","sma20","sma50","sma200","ema20","ema50"],
    "Momentum": ["rsi14","macd","macd_sig","stoch_k","stoch_d"],
    "Volatility": ["vol_roll","bb_bw"],
    "Volume": ["volume"],
    "Price": ["close","close_norm","ret1"]
}

def group_attributions(feature_names, shap_vals_row):
    family_scores = {}
    for fam, cols in FAMILY_MAP.items():
        score = 0.0
        for c in cols:
            if c in feature_names:
                idx = feature_names.index(c)
                score += abs(shap_vals_row[idx])
        family_scores[fam] = score
    total = sum(family_scores.values()) or 1.0
    for k in family_scores:
        family_scores[k] /= total
    return family_scores

def build_rationale(row, fam_scores, top_features, action_label):
    fam_sorted = sorted(fam_scores.items(), key=lambda x: x[1], reverse=True)
    fam_text = ", ".join([f"{k} {v:.0%}" for k,v in fam_sorted[:3]]) if fam_sorted else "signals mixed"
    tf_text = "; ".join([f"{name}({val:.3f})" for name,val in top_features]) if top_features else "—"
    action_str = {0:"SELL",1:"HOLD",2:"BUY"}.get(int(action_label), "ACT")
    return f"{action_str} because {fam_text}; key signals: {tf_text}"

def fit_surrogate_and_explain(trades_csv: str, features: list, out_csv: str,
                              use_shap=True, use_lime=False, top_k=5):
    trades = pd.read_csv(trades_csv, parse_dates=["date"]).set_index("date")
    
    # Find all feature columns that end with _t0
    X_cols = [col for col in trades.columns if col.endswith('_t0')]
    X = trades[X_cols].copy()
    y = trades["action"].astype(int)

    X = X.dropna().copy()
    y = y.loc[X.index]

    surrogate = XGBClassifier(
        n_estimators=200, max_depth=4, learning_rate=0.05,
        subsample=0.9, colsample_bytree=0.9, eval_metric="mlogloss"
    )
    surrogate.fit(X.values, y.values)

    rows = []
    feature_names = X_cols
    explainer_shap = None
    shap_vals = None
    if use_shap:
        explainer_shap = shap.TreeExplainer(surrogate)
        shap_vals = explainer_shap.shap_values(X.values)  # list per class for multiclass

    explainer_lime = None
    if use_lime:
        explainer_lime = LimeTabularExplainer(
            X.values, feature_names=feature_names,
            class_names=["SELL","HOLD","BUY"], discretize_continuous=False
        )

    for i, idx in enumerate(X.index):
        action = int(y.loc[idx])
        tf = []
        fam_scores = {}
        if use_shap and shap_vals is not None:
            sv = shap_vals[action][i] if isinstance(shap_vals, list) else shap_vals[i]
            # Ensure sv is a numpy array and get the top features
            sv = np.array(sv).flatten()
            # Ensure we don't exceed array bounds
            top_k_actual = min(top_k, len(sv))
            order = np.argsort(np.abs(sv))[::-1][:top_k_actual]
            tf = [(feature_names[j].replace("_t0",""), float(sv[j])) for j in order if j < len(feature_names)]
            fam_scores = group_attributions([c.replace("_t0","") for c in feature_names], sv)
        elif use_lime and explainer_lime is not None:
            exp = explainer_lime.explain_instance(X.values[i], surrogate.predict_proba, num_features=top_k, labels=[action])
            pairs = exp.as_list(label=action)
            tf = [(name, float(val)) for name, val in pairs]
            fam_scores = {k: 1.0/len(FAMILY_MAP) for k in FAMILY_MAP}  # fallback

        rationale = build_rationale(trades.loc[idx], fam_scores, tf, action)
        rows.append({
            "date": idx, "action": action, "rationale": rationale,
            "top_features": "; ".join([f"{n}:{v:.4f}" for n,v in tf])
        })

    out = pd.DataFrame(rows).set_index("date")
    os.makedirs(os.path.dirname(out_csv), exist_ok=True)
    out.to_csv(out_csv)
    return out
