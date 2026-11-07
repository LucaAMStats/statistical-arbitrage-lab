"""Pair screening using training-sample correlation and Engle-Granger tests."""
from __future__ import annotations
from itertools import combinations
import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.tsa.stattools import coint

def screen_pairs(prices: pd.DataFrame, min_correlation: float = 0.70,
                 max_pvalue: float = 0.05) -> pd.DataFrame:
    log_prices = np.log(prices.dropna(axis=1, how="any"))
    rows = []
    for a, b in combinations(log_prices.columns, 2):
        pair = log_prices[[a, b]].dropna()
        if len(pair) < 100:
            continue
        corr = pair[a].diff().corr(pair[b].diff())
        if pd.isna(corr) or corr < min_correlation:
            continue
        stat, pvalue, _ = coint(pair[a], pair[b])
        hedge = sm.OLS(pair[a], sm.add_constant(pair[b])).fit().params.iloc[1]
        rows.append({"asset_1": a, "asset_2": b, "return_corr": corr,
                     "coint_stat": stat, "pvalue": pvalue, "hedge_ratio": hedge,
                     "observations": len(pair)})
    result = pd.DataFrame(rows)
    if result.empty:
        return result
    return result.sort_values("pvalue").query("pvalue <= @max_pvalue").reset_index(drop=True)

def fit_pair(prices: pd.DataFrame, asset_1: str, asset_2: str) -> dict:
    pair = np.log(prices[[asset_1, asset_2]].dropna())
    model = sm.OLS(pair[asset_1], sm.add_constant(pair[asset_2])).fit()
    spread = pair[asset_1] - model.params.iloc[0] - model.params.iloc[1] * pair[asset_2]
    return {"intercept": float(model.params.iloc[0]),
            "hedge_ratio": float(model.params.iloc[1]), "spread": spread}
