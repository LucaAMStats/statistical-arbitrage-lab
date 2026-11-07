"""Single-pair mean-reversion backtest with lagged positions and simple costs."""
from __future__ import annotations
import numpy as np
import pandas as pd

def backtest_pair(prices: pd.DataFrame, asset_1: str, asset_2: str,
                  intercept: float, hedge_ratio: float,
                  lookback: int = 60, entry_z: float = 2.0,
                  exit_z: float = 0.5, stop_z: float = 4.0,
                  cost_bps: float = 5.0) -> tuple[pd.DataFrame, dict]:
    """Positions are formed at t and applied to returns at t+1.

    Spread is log(P1) - intercept - beta*log(P2). The portfolio return is
    approximated as a beta-weighted pair return, normalised by gross exposure.
    Costs are charged on changes in the signed position.
    """
    px = prices[[asset_1, asset_2]].dropna()
    logp = np.log(px)
    spread = logp[asset_1] - intercept - hedge_ratio * logp[asset_2]
    mean = spread.rolling(lookback, min_periods=lookback).mean()
    std = spread.rolling(lookback, min_periods=lookback).std()
    z = (spread - mean) / std.replace(0, np.nan)

    signal = pd.Series(0.0, index=px.index)
    state = 0.0
    for i, value in enumerate(z):
        if not np.isfinite(value):
            signal.iloc[i] = 0.0
            continue
        if state == 0:
            if value >= entry_z: state = -1.0
            elif value <= -entry_z: state = 1.0
        elif abs(value) <= exit_z or abs(value) >= stop_z:
            state = 0.0
        signal.iloc[i] = state

    # Long spread = long asset_1 / short beta units of asset_2.
    r1 = px[asset_1].pct_change()
    r2 = px[asset_2].pct_change()
    gross = 1.0 + abs(hedge_ratio)
    pair_return = (r1 - hedge_ratio * r2) / gross
    position = signal.shift(1).fillna(0.0)
    turnover = position.diff().abs().fillna(position.abs())
    costs = turnover * (cost_bps / 10_000)
    strategy_return = position * pair_return - costs
    equity = (1.0 + strategy_return.fillna(0.0)).cumprod()
    drawdown = equity / equity.cummax() - 1.0

    out = pd.DataFrame({"spread": spread, "zscore": z, "signal": signal,
                        "position_applied": position, "pair_return": pair_return,
                        "turnover": turnover, "cost": costs,
                        "strategy_return": strategy_return, "equity": equity,
                        "drawdown": drawdown})
    returns = strategy_return.dropna()
    ann_vol = returns.std() * np.sqrt(252) if len(returns) > 1 else np.nan
    sharpe = (returns.mean() * 252 / ann_vol) if ann_vol and ann_vol > 0 else np.nan
    years = len(returns) / 252
    cagr = equity.iloc[-1] ** (1 / years) - 1 if years > 0 and equity.iloc[-1] > 0 else np.nan
    metrics = {"total_return": float(equity.iloc[-1] - 1),
               "cagr": float(cagr), "annualised_volatility": float(ann_vol),
               "sharpe_annualised": float(sharpe),
               "max_drawdown": float(drawdown.min()),
               "observations": int(len(returns)),
               "turnover_sum": float(turnover.sum())}
    return out, metrics
