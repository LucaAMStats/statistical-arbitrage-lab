"""Run a basic pairs-trading research workflow from the command line."""
from pathlib import Path
import pandas as pd
from data import download_prices
from pairs import screen_pairs, fit_pair
from backtest import backtest_pair

TICKERS = ["KO", "PEP", "XOM", "CVX", "V", "MA", "HD", "LOW", "JPM", "BAC"]

def main():
    prices = download_prices(TICKERS, start="2017-01-01")
    # Chronological split: discover candidates on training data only.
    split = int(len(prices) * 0.70)
    train, test = prices.iloc[:split], prices.iloc[split:]
    candidates = screen_pairs(train, min_correlation=0.50, max_pvalue=0.10)
    Path("outputs").mkdir(exist_ok=True)
    candidates.to_csv("outputs/pair_screen.csv", index=False)
    if candidates.empty:
        print("No pairs passed the current training-sample screen.")
        return
    best = candidates.iloc[0]
    a, b = best["asset_1"], best["asset_2"]
    fitted = fit_pair(train, a, b)
    results, metrics = backtest_pair(
        test, a, b, fitted["intercept"], fitted["hedge_ratio"],
        lookback=60, entry_z=2.0, exit_z=0.5, stop_z=4.0, cost_bps=5.0
    )
    results.to_csv("outputs/backtest.csv")
    pd.Series(metrics).to_csv("outputs/metrics.csv", header=["value"])
    print(f"Selected pair: {a} / {b}")
    print(pd.Series(metrics).to_string())
    print("Saved outputs to ./outputs/")

if __name__ == "__main__":
    main()
