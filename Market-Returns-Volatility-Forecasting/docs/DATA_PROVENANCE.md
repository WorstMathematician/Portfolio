# Data sourcing, authorization, and limitations

## Primary public data

Yahoo Finance history, via the open-source yfinance Python library:

- Provider interface: https://finance.yahoo.com/quote/SPY/history/
- Download library: https://ranaroussi.github.io/yfinance/reference/api/yfinance.download.html
- Adjusted close explanation: https://help.yahoo.com/kb/SLN28256.html

Default security: SPY, an exchange-traded fund tracking US equities. Change the symbol as a **new, separately evaluated dataset**, not to cherry-pick favorable performance. This study is not based on confidential fund, customer or employer information.

Acquisition requests daily bars with raw Open/High/Low/Close and provider Adj Close. Calculated return labels use Adj Close and no further adjustment. Dividend and split event metadata are retained. Source retrieval requires internet connectivity and may be throttled or break if the unofficial Yahoo interface changes. Provider terms and rights to downstream redistribution should be checked; raw bars and generated outputs are intentionally not committed.

## Integrity boundaries

The code verifies structural properties and records anomalies, but **does not independently verify prices** against exchange settlement feeds. It cannot confirm that a missing weekday is a missing exchange session without a holiday calendar, or that a sudden price change is incorrect without independent evidence. The lack of such confirmation must not be described as a clean-data certification.

Suspicious adjusted returns, nontrivial price-adjustment ratios, split events and dividends should be inspected manually. Record source metadata, acquisition date, exact requested time window, exported market timezone, relevant correction decisions and any provider changes for empirical writeups.

## Fallback policy

There is **no automatic synthetic-data fallback**. Failed yfinance retrieval stops the online run. Offline CSV execution requires a specific source label and preserves it as *user-supplied, not independently verified*; results can only be called genuine observations once the CSV's origins have been validated outside this software.

Synthetic data exist only in deterministic tests. The repo contains no bundled real-market dataset or claimed empirical scores from the development environment. Do not copy synthetic fixtures into public dashboards or hiring materials as measured historical results.

## Reproduction and review

After every run inspect:

- provenance.json: source string, requested dates, acquisition UTC timestamp, file hash, quality audit;
- prices.csv: retained source snapshot (not version controlled);
- evaluation.json: chronological boundaries, fit counts and model failures;
- forecasts and score CSVs: all reported numbers should be reproducible from the same saved snapshot.

Re-acquiring the same window may yield revised prices or adjustment factors. Archive a permitted provider export separately when strong long-run reproducibility is required.

This project is **not a trading system** and does not demonstrate a stable strategy, investment alpha, or calibrated regulated risk model.
