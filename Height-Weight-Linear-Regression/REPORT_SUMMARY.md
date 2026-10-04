# Report Summary - Height-Weight Linear Regression

## Objective

Analyze the relationship between height in inches and weight in pounds using simple linear regression, while clearly distinguishing the original empirical analysis from the repository's runnable synthetic demonstration.

## Evidence status

The original project reports results from a 10,000-row height-weight dataset. That original CSV is **not currently included in this repository**. Therefore, the figures in the next section are treated as **historical empirical results recorded by the original project**, not as results that the current repository can independently reproduce on its own.

The notebook now provides a clean `DATA_MODE = "original"` path for rerunning the analysis when the original CSV is supplied locally.

## Historical original-data summary

- Observations: 10,000 individuals
- Predictor: Height in inches
- Response: Weight in pounds
- Mean height: 66.3676 inches
- Mean weight: 161.4404 pounds
- Height range: 54.2631 to 78.9987 inches
- Weight range: 64.7001 to 269.9897 pounds

### Historical model results

- Estimated intercept: -350.737192
- Estimated slope: 7.717288
- Residual Sum of Squares: 1,492,934.8396
- R-squared: 0.8552
- Standard error of regression: 12.2198
- 95% confidence interval for slope: 7.655028 to 7.779547
- Slope p-value: < 0.001

## Historical interpretation

For the original analysis, the reported slope indicates that each additional inch of height was associated with an expected increase of about 7.72 pounds in weight. The reported R-squared of 0.8552 indicates that height accounted for about 85.5% of the variation in weight in that dataset.

These statements describe the recorded original-data analysis only.

## Runnable synthetic demonstration

Because the original CSV is not distributed with the repository, the notebook defaults to a synthetic demonstration so the regression workflow can still be executed.

The synthetic generator now uses an independently selected illustrative data-generating process. It does **not** use the historical intercept, slope, residual standard deviation, means, R-squared, or other reported fitted quantities as generation targets.

Any coefficients, R-squared values, residual statistics, confidence intervals, plots, or p-values produced in `DATA_MODE = "synthetic"` describe only the generated demonstration dataset. They must not be presented as reproduction, verification, or confirmation of the historical original-data metrics.

## Original CSV rerun path

To independently rerun the empirical analysis when the source data are available:

1. Supply the CSV locally, by default at `data/weight-height.csv`.
2. Set `DATA_MODE = "original"` in the notebook.
3. Run all cells.
4. Compare the newly computed output with the historical figures above and document any differences.

The loader accepts common height/weight column labels and validates numeric observations before fitting the model.

## Model limitations

Height can be a useful predictor of weight, but it does not fully explain individual weight differences. Body composition, age, lifestyle, clothing, bone density, measurement practices, and other variables may matter. A simple bivariate model should not be interpreted causally.

## Portfolio framing

This project demonstrates exploratory data analysis, manual regression calculations, model fitting with statistical software, coefficient and R-squared interpretation, residual diagnostics, and reproducible reporting practices. The refactored structure also demonstrates an important analytical distinction: a synthetic example can illustrate a method without claiming to reproduce unavailable empirical evidence.
