# Run Guide

Install dependencies:

```bash
pip install pandas numpy matplotlib scikit-learn jupyter openpyxl
```

Validate that the raw dataset files are present:

```bash
python scripts/validate_raw_files.py
```

Run each project from the repository root:

```bash
python Program-Finance-Control-Tower/src/program_finance.py
python Budget-vs-Actual-FPA-Variance-Analysis/src/budget_variance.py
python Defense-Contractor-Peer-Benchmarking/src/defense_benchmark.py
```

Each project writes outputs into its own outputs folder.
