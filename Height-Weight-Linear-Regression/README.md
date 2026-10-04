# Height-Weight Linear Regression

## Project overview

This project demonstrates simple linear regression for predicting weight from height. It now separates two distinct uses of the notebook:

1. **Original-data analysis** — reruns the analysis on the original CSV when that file is supplied locally.
2. **Synthetic demonstration** — runs the same analysis workflow on independently chosen illustrative data so the notebook remains executable without the original dataset.

The synthetic demonstration is **not** a reproduction or validation of the historical results reported for the original 10,000-row dataset.

## Result provenance

The repository currently does not include the original 10,000-row CSV. The numerical results below are retained as **historical empirical results recorded by the original project** and cannot be independently reproduced from the repository alone until the original CSV is supplied.

### Historical original-data results

- Observations: 10,000
- Mean height: 66.3676 inches
- Mean weight: 161.4404 pounds
- Estimated intercept: -350.737192
- Estimated slope: 7.717288
- R-squared: 0.8552
- Residual Sum of Squares: 1,492,934.8396
- Standard error of regression: 12.2198
- 95% confidence interval for slope: 7.655028 to 7.779547
- Slope p-value: < 0.001

These values should be interpreted as results from the original analysis, not as values produced by the notebook's default synthetic mode.

## Running the notebook

### Synthetic demonstration

Open `Project_3_Linear_Regression.ipynb` and leave:

```python
DATA_MODE = "synthetic"
```

The notebook will generate an illustrative height-weight dataset using parameters that are intentionally independent of the historical fitted coefficients above. Results produced in this mode describe only that synthetic dataset.

### Original-data analysis

1. Place the original CSV at `data/weight-height.csv` (or change `CSV_PATH` in the notebook).
2. Set:

```python
DATA_MODE = "original"
```

3. Run all cells.

The loader accepts common height/weight column names, including `Height` / `Weight` and `Height_Inches` / `Weight_Pounds`, validates numeric values, and then runs the same regression workflow.

See `data/README.md` for the expected input format.

## Analytical workflow

The notebook demonstrates:

- data loading and validation
- exploratory summaries
- scatter plotting
- manual least-squares coefficient calculation
- OLS fitting with `statsmodels`
- R-squared and residual standard error
- confidence intervals and p-values
- regression-line visualization
- residual diagnostics
- interpretation with explicit source labeling

## Files

- `Project_3_Linear_Regression.ipynb`: runnable original/synthetic analysis workflow
- `REPORT_SUMMARY.md`: interpretation and provenance of the historical project results
- `data/README.md`: instructions for supplying the original CSV

## Portfolio framing

This project demonstrates linear regression and, importantly, reproducibility discipline: historical empirical results are kept separate from a runnable synthetic example when the source dataset is not distributed with the repository.
