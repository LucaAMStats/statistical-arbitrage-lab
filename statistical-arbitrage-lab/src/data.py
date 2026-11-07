"""Historical price data helpers. Yahoo Finance is used for research/education only."""
from __future__ import annotations
import pandas as pd
import yfinance as yf

def download_prices(tickers: list[str], start: str = "2018-01-01",
                    end: str | None = None) -> pd.DataFrame:
    raw = yf.download(tickers, start=start, end=end, auto_adjust=True,
                      progress=False, group_by="column")
    if raw.empty:
        raise RuntimeError("No price data returned. Check tickers, dates and connection.")
    if isinstance(raw.columns, pd.MultiIndex):
        # yfinance layout varies by version; use adjusted close if present.
        level0 = raw.columns.get_level_values(0)
        field = "Close" if "Close" in level0 else level0[0]
        prices = raw[field]
    else:
        prices = raw[["Close"]].rename(columns={"Close": tickers[0]})
    prices = prices.sort_index().dropna(how="all")
    return prices.dropna(axis=1, how="all")
