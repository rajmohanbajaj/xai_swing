import os
import matplotlib.pyplot as plt
import pandas as pd

def plot_equity(trades: pd.DataFrame, out_path: str):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    plt.figure()
    trades["equity"].plot(title="Equity Curve")
    plt.xlabel("Date"); plt.ylabel("Equity")
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()
