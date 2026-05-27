# LA Housing Affordability Forecasting

## Project overview

This project analyzes housing affordability across Los Angeles County ZIP code areas from 2015 to 2024 and forecasts 2025 cost-burden risk. Affordability is measured with the rent-to-income ratio, where ZIP-year observations above 30 percent are treated as cost-burdened.

## Business and policy value

Housing affordability affects household stability, access to transportation, savings, health care, and long-term economic mobility. This project turns public rent and income data into a geographic affordability-risk analysis that can support policy research, community planning, and resource prioritization.

## Questions answered

- How did rent-to-income burden change across Los Angeles County ZIP codes from 2015 to 2024?
- Which ZIP codes experienced the highest affordability pressure?
- What share of ZIP-year observations exceeded the 30 percent cost-burden threshold?
- Can future cost-burden risk be predicted using prior rent and income conditions?
- Which ZIP codes are most likely to remain cost-burdened in 2025?

## Data sources

- ACS 5-year median household income data, table B19013, extracted at the ZCTA level for 2015 to 2024.
- Zillow Observed Rent Index ZIP-level rent data, aggregated from monthly values into annual rent estimates.

## Final cleaned dataset

- 1,248 ZIP-year observations after cleaning.
- 212 Los Angeles County ZIP codes.
- 74.3590 percent of ZIP-year observations exceeded the 30 percent cost-burden threshold.
- Mean rent-to-income burden: 37.5320 percent.
- Median rent-to-income burden: 34.3598 percent.

## Modeling approach

The project compares baseline and stricter model specifications for predicting whether a ZIP-year observation is cost-burdened. The final model is a stricter logistic regression model selected because it balances strong predictive performance with lower leakage risk.

## Final model result

- Final model: Logistic Regression, strict feature specification.
- Test year: 2024.
- Accuracy: 0.8915.
- Precision: 0.9371.
- Recall: 0.9198.
- F1 score: 0.9283.
- ROC-AUC: 0.9498.
- Brier score: 0.0794.

## Key findings

- Affordability pressure remained above the 30 percent threshold throughout the study period.
- Mean burden rose from 35.9079 percent in 2015 to a peak of 39.2886 percent in 2018.
- By 2024, the mean burden remained elevated at 36.7495 percent.
- In 2024, 76.4151 percent of ZIP-year observations were above the 30 percent threshold.
- High-risk ZIP codes for 2025 included 90265, 90210, 90402, 90024, 90021, 90013, 90014, 90016, 90007, and 90017.

## Files in this GitHub project

- `REPORT_SUMMARY.md`: written project summary.
- `DATA_NOTE.md`: notes on source files and large artifacts.
- `src/housing_affordability_pipeline.py`: reusable analysis pipeline skeleton.
- `outputs/key_results.csv`: dashboard-ready summary metrics.
- `outputs/model_performance.csv`: model comparison summary.
- `outputs/top_2025_risk_zips.csv`: highest predicted 2025 cost-burden risk ZIP codes.

## Portfolio framing

This project demonstrates public-data integration, geospatial affordability analysis, feature engineering, classification modeling, leakage-aware model selection, forecast interpretation, and policy-focused communication.
