# Statistical Arbitrage Lab

A portfolio-ready quantitative research project exploring **equity pairs trading** through cointegration, spread modelling and out-of-sample backtesting. The repository includes a GitHub Pages front end and a Python research pipeline.

> **Important:** This is an educational research framework, not investment advice or a live trading system. The website's chart and watchlist are explicitly illustrative. Actual results are only produced when you run the Python pipeline on historical data. Past statistical relationships may break down and do not imply future profitability.

## Project question

Can pairs of economically related equities exhibit a sufficiently stable long-run relationship that deviations in their relative price can be modelled and tested as a mean-reversion strategy after costs?

## Research workflow

1. **Data:** download adjusted daily prices for a defined liquid equity universe.
2. **Candidate generation:** calculate return correlation and test candidate log-price series for cointegration using the Engle–Granger two-step test.
3. **Hedge ratio:** estimate the training-window OLS relationship and construct the residual spread.
4. **Signal:** calculate a rolling spread z-score. Enter beyond ±2 standard deviations, exit near the mean, and apply a stop threshold.
5. **Backtest:** apply signals to next-period returns, deduct a configurable turnover cost and report return, volatility, Sharpe ratio and drawdown.
6. **Validation:** reserve a chronological holdout sample and investigate parameter sensitivity, structural breaks, borrow costs and execution assumptions.

## Repository structure

```text
statistical-arbitrage-lab/
├── index.html              # GitHub Pages research site
├── assets/
│   ├── style.css
│   └── site.js
├── src/
│   ├── data.py
│   ├── pairs.py
│   ├── backtest.py
│   └── run_research.py
├── data/                   # Place local datasets here (not committed by default)
├── requirements.txt
└── README.md
```

## Run locally

Requires Python 3.10+.

```bash
git clone https://github.com/YOUR-USERNAME/statistical-arbitrage-lab.git
cd statistical-arbitrage-lab
python -m venv .venv
# Windows:
.venv\\Scripts\\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
python src/run_research.py
```

The pipeline writes `outputs/pair_screen.csv`, `outputs/backtest.csv` and `outputs/metrics.csv`. Yahoo Finance data availability, ticker histories and package behaviour can change.

## Publish the website with GitHub Pages

1. Create a new public GitHub repository named `statistical-arbitrage-lab`.
2. Upload the contents of this folder to the repository root (so `index.html` is at the top level).
3. In the repository, open **Settings → Pages**.
4. Under **Build and deployment**, choose **Deploy from a branch**.
5. Select branch `main`, folder `/ (root)`, then **Save**.
6. GitHub will provide the published URL, usually `https://YOUR-USERNAME.github.io/statistical-arbitrage-lab/`.

Replace the two generic GitHub links in `index.html` with your repository URL after creating it.

## Methodological caveats to address before treating results seriously

- **Cointegration is not correlation.** Correlation of returns is used only as a rough pre-screen; it does not establish a stable long-run equilibrium.
- **Multiple testing:** screening many pairs inflates false positives. Consider false-discovery-rate control and an untouched final test period.
- **Look-ahead and selection bias:** candidate selection and hedge-ratio estimation must be confined to training data; use walk-forward refitting for a stronger design.
- **Parameter mining:** test robustness across entry/exit thresholds and lookback windows rather than reporting the best historical setting.
- **Structural breaks:** cointegration can disappear. Monitor rolling test statistics, hedge-ratio stability and spread half-life.
- **Costs and shorting:** the simple cost model is only a placeholder. Include bid/ask spread, market impact, borrow availability/fees, financing, dividends and execution timing.
- **Portfolio construction:** the sample backtest is one pair at a time and does not yet manage correlated pairs, gross/net exposure, leverage or capital allocation.
- **Inference:** Sharpe and CAGR estimates from short or selected samples are noisy. Include confidence intervals and benchmark comparisons.

## Suggested next extensions

1. Add sector membership and dollar-volume filters to the universe.
2. Compare Engle–Granger with Johansen tests and residual-based diagnostics.
3. Add rolling/walk-forward hedge ratios and structural-break detection.
4. Add half-life estimation and a pair rejection rule for slow or unstable spreads.
5. Build a portfolio backtester with exposure limits, borrow costs and pair-level attribution.
6. Add experiment tracking so every run records universe, dates, parameters and data timestamp.

## Disclaimer

For research and educational use only. This project is not a recommendation to buy or sell any security. No strategy is guaranteed to be profitable. Verify data, assumptions and implementation independently before any use with capital.
