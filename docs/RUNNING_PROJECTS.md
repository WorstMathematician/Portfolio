# Running Portfolio Projects

[← Back to portfolio](../README.md)

## Base environment

A practical local environment for the Python-based projects includes:

```bash
pip install pandas numpy matplotlib scikit-learn jupyter openpyxl
```

Individual projects may require additional packages documented in their notebooks or source files.

## Finance projects

From the repository root:

```bash
python Program-Finance-Control-Tower/src/program_finance.py
python Budget-vs-Actual-FPA-Variance-Analysis/src/budget_variance.py
python Defense-Contractor-Peer-Benchmarking/src/defense_benchmark.py
```

Each finance project writes its outputs into its own `outputs/` directory.

## Notebook projects

Open the relevant `.ipynb` file in Jupyter or another compatible notebook environment and review the project README before running it.

For projects that distinguish original and synthetic data modes, follow the project-specific README rather than assuming that synthetic output reproduces historical empirical results.

## Repository validation

GitHub Actions validates Python compilation, critical lint errors, notebook structure, and pytest tests when tests are present.

## Market returns and volatility forecasting

This independent research project uses its own installable Python package and optional time-series/UI dependencies. From the repository root:

    cd Market-Returns-Volatility-Forecasting
    python -m venv .venv
    # Activate the virtual environment for your operating system
    python -m pip install -e ".[all,test]"
    python -m pytest -q
    python -m market_volatility.cli --symbol SPY --start 2010-01-01 --end 2026-10-17 --output-dir outputs/SPY
    streamlit run dashboard.py

The command downloads observed data when the provider is reachable; it does not generate synthetic scores if unavailable. The exclusive --end boundary should be updated intentionally for later samples. Consult [the full project README](../Market-Returns-Volatility-Forecasting/README.md) for offline provider CSV mode, model assumptions, audit files, and limitations.
