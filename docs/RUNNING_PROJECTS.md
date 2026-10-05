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
