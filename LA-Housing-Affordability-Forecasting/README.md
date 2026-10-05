# LA Housing Affordability Forecasting

[← Back to portfolio](../README.md)

> **Purpose:** Analyze Los Angeles County housing affordability from 2015–2024 and model 2025 cost-burden risk using public rent and income data.

## Portfolio Snapshot

| Metric | Result |
|---|---:|
| Cleaned ZIP-year observations | 1,248 |
| Los Angeles County ZIP codes | 212 |
| 2024 observations above 30% burden | 76.4% |
| Final model | Logistic Regression |
| Test-year ROC-AUC | 0.9498 |
| Test-year F1 score | 0.9283 |

## Business & Policy Question

Housing affordability affects household stability, transportation access, savings, health care, and long-term economic mobility. This project turns public rent and income data into a geographic affordability-risk analysis that can support policy research, community planning, and resource prioritization.

## Questions Answered

- How did rent-to-income burden change across Los Angeles County ZIP codes from 2015 to 2024?
- Which ZIP codes experienced the highest affordability pressure?
- What share of ZIP-year observations exceeded the 30% cost-burden threshold?
- Can future burden risk be predicted using prior rent and income conditions?
- Which ZIP codes are most likely to remain cost-burdened in 2025?

## Data Sources

- ACS 5-year median household income, table B19013, at the ZCTA level for 2015–2024.
- Zillow Observed Rent Index ZIP-level rent data, aggregated from monthly to annual estimates.

## Modeling Approach

The project compares baseline and stricter feature specifications for predicting whether a ZIP-year observation is cost-burdened. The final model is a stricter logistic regression specification selected to balance predictive performance with lower leakage risk.

## Final Model Results

| Metric | Value |
|---|---:|
| Accuracy | 0.8915 |
| Precision | 0.9371 |
| Recall | 0.9198 |
| F1 score | 0.9283 |
| ROC-AUC | 0.9498 |
| Brier score | 0.0794 |

## Key Findings

- Mean burden remained above the 30% threshold throughout the study period.
- Mean burden rose from 35.9% in 2015 to a peak of 39.3% in 2018.
- By 2024, mean burden remained elevated at 36.7%.
- In 2024, 76.4% of ZIP-year observations were above the 30% threshold.
- High-risk 2025 ZIP codes included 90265, 90210, 90402, 90024, 90021, 90013, 90014, 90016, 90007, and 90017.

## Project Files

- [Report summary](REPORT_SUMMARY.md)
- [Data note](DATA_NOTE.md)
- [Analysis pipeline](src/housing_affordability_pipeline.py)
- [Key results](outputs/key_results.csv)
- [Model performance](outputs/model_performance.csv)
- [Top 2025 risk ZIPs](outputs/top_2025_risk_zips.md)

## Skills Demonstrated

Public-data integration · Feature engineering · Classification modeling · Leakage-aware model selection · Forecast interpretation · Policy-focused communication · Python · scikit-learn

## Next Development Steps

Future iterations can add a polished map/dashboard preview, model-calibration visualization, and expanded reproducibility documentation.
