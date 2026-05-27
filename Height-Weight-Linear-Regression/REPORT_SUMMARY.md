# Report Summary - Height-Weight Linear Regression

## Objective

Analyze a dataset of 10,000 individuals to estimate the linear relationship between height in inches and weight in pounds. The goal is to fit a regression line that predicts weight from height and evaluate how well height alone explains variation in weight.

## Dataset overview

- Observations: 10,000 individuals
- Predictor: Height in inches
- Response: Weight in pounds
- Mean height: 66.3676 inches
- Mean weight: 161.4404 pounds
- Height range: 54.2631 to 78.9987 inches
- Weight range: 64.7001 to 269.9897 pounds

## Model results

- Estimated intercept: -350.737192
- Estimated slope: 7.717288
- Residual Sum of Squares: 1,492,934.8396
- R-squared: 0.8552
- Standard error of regression: 12.2198
- 95 percent confidence interval for slope: 7.655028 to 7.779547
- Slope p-value: less than 0.001

## Interpretation

The estimated slope indicates that each additional inch of height is associated with an expected increase of about 7.72 pounds in weight. The R-squared value of 0.8552 means that height explains about 85.5 percent of the variation in weight in this dataset.

## Visualizations

The report includes a height-versus-weight scatter plot showing a strong positive linear pattern. It also includes a residual plot, where residuals appear roughly centered around zero without a strong systematic pattern. This supports the use of a simple linear model for this dataset.

## Conclusion

Height is a strong predictor of weight in this dataset, but it is not a complete explanation of weight. People with the same height can have different weights due to body composition, lifestyle, clothing, bone density, and other factors. A more comprehensive model could add additional predictors.

## Portfolio framing

This project demonstrates exploratory data analysis, manual regression calculations, model fitting with statistical software, interpretation of coefficients, R-squared, residual diagnostics, and clear communication of model limitations.
