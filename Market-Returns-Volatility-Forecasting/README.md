# Market Returns & Volatility Forecasting

**Financial time series | Statistical forecasting | Backtesting | Data quality | Interactive risk communication**

A reproducible, standalone Python research application that asks two distinct questions:

1. Can simple models predict the sign or magnitude of tomorrow's **log return**?
2. Can statistical models predict the next trading session's **conditional return variance** better than historical volatility?

The design prioritizes honest validation over favorable headline scores. **No empirical performance claims or charts are committed in advance.** Data must be acquired from a source or provided as a labeled, verifiable export. Historical results are generated locally and are excluded from version control.

[Portfolio homepage](../README.md) | [Methodology](docs/METHODOLOGY.md) | [Data limitations](docs/DATA_PROVENANCE.md)

## What this demonstrates

- Market-data acquisition with explicit source, acquisition time, requested range and SHA-256 fingerprint.
- Quality checks for missing fields, duplicate or nonmonotonic dates, weekend observations, invalid OHLC/volume, action columns, extreme adjusted returns, and possible date gaps.
- Split-and-dividend-adjusted daily prices from Yahoo Finance, and log/simple returns in percentage units.
- Distribution shape, extreme observations, autocorrelation, ARCH effects, rolling annualized volatility and ADF/KPSS stationarity diagnostics.
- Expanding-origin, one-trading-session-ahead predictions, refit schedules and no random time-series splitting.
- Historical 21-day and EWMA 0.94 scale forecasts. Optional ARCH(1) and GARCH(1,1) conditional-scale models.
- Independent zero-return, expanding-mean and autoregressive AR(1) return benchmarks.
- Held-out QLIKE, variance MSE, absolute-return proxy error, 95% normal-interval coverage, normal 5% risk-threshold exceedances, and paired moving-block uncertainty intervals.
- Interactive Streamlit read-only dashboard with a clearly labeled, hypothetical risk sensitivity calculator.

## Data source and acquisition

Default: daily **SPY** (SPDR S&P 500 ETF Trust) market history through [Yahoo Finance](https://finance.yahoo.com/quote/SPY/history/) using [yfinance](https://ranaroussi.github.io/yfinance/reference/api/yfinance.download.html). The request explicitly asks for **auto_adjust=False**, actions, a flat column index and **Adj Close**. Yahoo describes adjusted close as incorporating applicable splits and distributions:

https://help.yahoo.com/kb/SLN28256.html

SPY is an illustrative ETF, not an individual firm's operating result. This project's adjusted-price return is not an executable fund investment return: it ignores implementation frictions, borrowing costs, taxes and data revisions. Historical adjustment factors can be restated. yfinance uses an unofficial public-data endpoint; availability, schema and provider usage restrictions may change. See the provenance report saved with each run.

No data acquisition succeeded in the development environment because external market-data hosts were unreachable. **No observed market dataset and no backtest score is claimed in this repository contribution.** Run online to generate results; failures terminate without fabricating observations.

## Run locally

Requires Python 3.10 or newer. From this project directory:

    python -m venv .venv
    # Linux / macOS
    source .venv/bin/activate
    # Windows PowerShell
    # .venv\Scripts\Activate.ps1
    python -m pip install --upgrade pip
    python -m pip install -e ".[all,test]"

For a reproducible **fixed acquisition window**, specify both endpoints (end date is excluded):

    python -m market_volatility.cli --symbol SPY --start 2010-01-01 --end 2026-10-17 --output-dir outputs/SPY

Use a more current exclusive end date to update the sample. If the optional ARCH dependency is unavailable, models are omitted and the evaluation manifest records the reason; to explicitly use only baselines:

    python -m market_volatility.cli --symbol SPY --start 2010-01-01 --skip-arch

To work offline with a legitimate, properly labeled price export containing Date, Open, High, Low, Close, Adj Close and Volume:

    python -m market_volatility.cli --symbol SPY --input-csv path/to/provider_export.csv --source-label "My dated SPY provider export" --output-dir outputs/SPY

The CSV label is **not independent authenticity verification**; document original provider, download URL and export date. Do not assume that unadjusted Close is interchangeable with Adj Close.

To launch the analysis UI (no automatic download):

    streamlit run dashboard.py

Use the left sidebar to select the result folder and model. The UI intentionally shows a placeholder until actual output files exist.

## Reproducible output contract

All files are generated in the chosen output folder, which is gitignored:

| Output | Meaning |
| --- | --- |
| prices.csv, provenance.json | Source bars, acquisition and quality audit, SHA-256 |
| features.csv | Observed adjusted price, returns and trailing 21-session scale |
| diagnostics.json | ADF, KPSS, normality, serial dependence, ARCH diagnostics |
| volatility_forecasts.csv | Prediction origin and next target date, forecast variance/sigma, observed realization, predictive bands |
| volatility_scores.csv | Holdout error scores and paired uncertainty |
| return_forecasts.csv, return_scores.csv | Separate return prediction baselines and errors |
| evaluation.json | Chronology, fitting status, errors, model refit counts |
| figures/*.png | Observed distributions, ACFs, price and volatility comparison |

## Evaluation design

All model estimates are computed using **observations no later than the previous trading session**. Starting after at least 504 known returns (subject to the chosen split), each subsequent held-out session receives a one-step-ahead prediction. The initial cut is chronological: the later of 504 training observations or the first 75% of returns. ARCH/GARCH parameters are re-estimated every 21 origins on an expanding history, with the full known history re-filtered at each origin.

Volatility is expressed as **daily percent log-return sigma**, not annualized variance. For display only, standard deviation is annualized using sqrt(252). The realized target for volatility scoring is next-session squared log return, a very noisy proxy for conditional variance. QLIKE has a lower-is-better convention. Normal intervals and left-tail thresholds are **assumptions**, not probabilistic guarantees; coverage and breach rates are measured out of sample.

The paired QLIKE difference against the historical 21-day baseline receives a seeded, moving-block bootstrap interval. Small samples, heteroskedastic losses, overlapping market regimes and model-selection effects mean the interval must be interpreted cautiously. Return forecasts are evaluated separately with MAE, RMSE and directional accuracy where defined. The zero-return baseline cannot have directional accuracy.

See [Methodology](docs/METHODOLOGY.md) for equations, assumptions and threats to validity.

## Testing

    python -m pytest -q

Unit tests use synthetic **fixtures solely to verify software behavior** (input rejection, chronology, scoring, optional GARCH path). Fixture outputs are not empirical backtest results. A dedicated GitHub Actions workflow installs project dependencies and runs the tests offline. Repository-wide CI also compiles and lints Python source.

## Safety and limits

This is an **educational research demonstration, not financial advice**. No model is asserted to beat simple benchmarks before observed-data evaluation. Volatility forecasting does not imply predictable returns. Risk scenarios assume fixed linear exposure; they ignore slippage, transaction fees, leverage liquidation, taxes, volatility-regime breaks, jumps, market closures and tail dependence. Do not substitute the demo for independent risk validation or live-trading decisions.

## Architecture

    Market-Returns-Volatility-Forecasting/
    ├── dashboard.py                # Read-only Streamlit dashboard
    ├── pyproject.toml              # Local install and optional GARCH/UI extras
    ├── src/market_volatility/
    │   ├── data.py                 # Provider acquisition, quality checks, provenance
    │   ├── features.py             # Returns, diagnostics
    │   ├── models.py               # Baselines, ARCH/GARCH filtering
    │   ├── backtest.py             # Origin loop, scoring, block bootstrap
    │   ├── report.py               # Saved diagnostic figures
    │   └── cli.py                  # End-to-end runner
    ├── tests/test_pipeline.py      # Deterministic, synthetic test fixtures
    └── docs/                      # Methodology and provider limitations

This project is **independent of credit-card classification, property cash flow, and public-finance forecasting**.
