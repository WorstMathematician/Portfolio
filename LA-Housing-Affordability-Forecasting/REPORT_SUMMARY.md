# Report Summary - LA Housing Affordability Forecasting

## Objective

Analyze how housing affordability changed across Los Angeles County ZIP code areas from 2015 to 2024 using the rent-to-income ratio, then forecast which ZIP codes are most likely to remain cost-burdened in 2025.

## Real-world context

Housing affordability affects how much income households have left for food, transportation, health care, education, and savings. This project uses the 30 percent rent-to-income threshold as a practical indicator of cost burden. The analysis treats affordability as a structural market issue, not as a reflection of individual failure.

## Data and preparation

The project combines two public data sources:

- ACS 5-year median household income data from table B19013 for 2015 through 2024.
- Zillow Observed Rent Index ZIP-level monthly rent data, aggregated into annual rent estimates.

After filtering and cleaning, the final dataset contained 1,248 ZIP-year observations across 212 Los Angeles County ZIP codes. Rent-to-income burden was calculated as annualized rent divided by median household income. A binary cost-burden flag was created for observations where rent-to-income burden was at least 30 percent.

## Descriptive results

Across the cleaned dataset:

- Mean rent-to-income burden: 37.5320 percent.
- Median rent-to-income burden: 34.3598 percent.
- Minimum burden: 21.0373 percent.
- Maximum burden: 121.9401 percent.
- Share of ZIP-year observations cost-burdened: 74.3590 percent.

Affordability worsened over the study period. The countywide mean burden was 35.9079 percent in 2015, rose to 39.2886 percent in 2018, and remained elevated through 2024. By 2024, the mean burden was 36.7495 percent and 76.4151 percent of ZIP-year observations were above the affordability threshold.

## Geographic findings

The most burdened ZIP codes in 2024 included:

- 90021: 102.1971 percent.
- 90014: 98.6615 percent.
- 90013: 90.6402 percent.
- 90007: 80.6317 percent.
- 90265: 76.3738 percent.
- 90210: 68.4472 percent.

The least burdened ZIP codes in 2024 included 91381, 90245, 90808, and 90807.

## Modeling approach

The predictive task was to classify whether a ZIP-year observation would be cost-burdened. The project compared Linear Regression, Logistic Regression, and Random Forest models using a time-based split:

- Training: 2017 through 2022.
- Validation: 2023.
- Testing: 2024.

The original feature set included lagged affordability variables, but those variables were highly target-adjacent. A stricter specification removed the highest-risk proxy features and retained lagged rent, lagged income, rolling rent and income averages, growth terms, year, and ZIP code identity.

## Final model selection

The original Random Forest achieved the strongest raw score, but the stricter Logistic Regression model was selected as the final model because it reduced leakage risk while maintaining strong performance.

Final Logistic Regression Strict performance on the 2024 test set:

- Accuracy: 0.8915.
- Precision: 0.9371.
- Recall: 0.9198.
- F1 score: 0.9283.
- ROC-AUC: 0.9498.
- Brier score: 0.0794.

## 2025 forecast

Using the stricter logistic regression model trained through 2024, the project generated 2025 ZIP-level risk forecasts for 197 ZIP codes. The highest-risk ZIP codes included 90265, 90210, 90402, 90024, 90021, 90013, 90014, 90016, 90007, and 90017.

## Limitations

- ACS small-area income estimates can be unstable.
- Zillow ZORI may not fully capture informal, subsidized, or lower-end rental markets.
- ZIP and ZCTA boundaries do not perfectly align.
- Rent-to-income ratios use separate area-level medians, not household-level matched records.
- ZIP code identity improves forecasting for known places but limits generalization to unseen areas.

## Conclusion

Housing affordability pressure in Los Angeles County was high and persistent from 2015 to 2024. Nearly three-quarters of ZIP-year observations exceeded the 30 percent cost-burden threshold. The stricter logistic regression model showed that future burden can be predicted effectively using historical rent and income conditions, while keeping the model more defensible against leakage risk.
