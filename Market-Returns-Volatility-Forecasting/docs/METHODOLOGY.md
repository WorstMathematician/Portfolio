# Technical methodology and validation contract

## Research questions

Return forecasting and scale forecasting are distinct estimands. Every daily return is r[t] = 100 × log(AdjClose[t] / AdjClose[t-1]), in percent units. A volatility forecast is sigma[t|t-1] = sqrt(Var(r[t] | history through t-1)), also in daily percent return units.

An adjusted-close price index is not a directly executable, fee-inclusive investment series. Do not mix raw and adjusted closes when computing return labels.

## Data integrity

- Strictly increasing, unique date keys. Weekend dates in a daily US ETF series are rejected.
- Required OHLCV plus adjusted close are positive, finite and internally bounded; volume may be zero, never negative.
- Null mandatory values terminate execution; never forward-fill price/return labels automatically.
- Large absolute log returns over 20 percentage points are **flagged**, not automatically removed; check split adjustments, provider restatements, corporate actions and genuine crashes.
- Weekdays not present in the sample are reported as *potential gaps*, with exchange holidays included. No claim is made that every weekday should have a bar. Compare to an official XNYS session calendar before classifying missing trading sessions.
- Dividend and split events are counted, but Yahoo's corporate-action accuracy is not independently audited.
- Minimum sample size is enforced (default training at least 504 return observations). There is no interpolation or future-aware imputation.

## Descriptive diagnostics

- Unbiased sample standard deviation, mean, skew and excess kurtosis for returns.
- Rolling 21-return sample volatility times sqrt(252) for annualized display.
- Ljung-Box tests at lag 10 on returns and squared returns.
- ARCH-LM test at lag 10.
- Jarque-Bera normality test.
- Augmented Dickey-Fuller null: unit root; KPSS level-stationarity null: stationarity. These are complementary, sample-dependent diagnostics; p-value approximation bounds matter.
- Lag-one correlation for returns and squared returns.

Autocorrelation of squared returns indicates clustering, not necessarily market timing skill.

## Forecast models

For each origin, training includes only returns through the origin session and predicts the **next recorded trading session**:

1. Historical volatility: sample standard deviation of the previous 21 observed daily returns.
2. EWMA/RiskMetrics: start from sample variance of the first 30 available returns and recursively update v[t] = 0.94 v[t-1] + 0.06 r[t]^2. This is a fixed-parameter benchmark, not a fitted winner.
3. Optional ARCH(1): zero conditional mean with one lagged squared shock; Gaussian innovation.
4. Optional GARCH(1,1): zero conditional mean with one ARCH and one GARCH term; Gaussian innovation. Coefficients refit on expanding data every 21 origins. For intervening sessions they are fixed, but the conditional variance filter receives newly known observations. Nonconverged or nonpositive fits are recorded, not quietly converted into a baseline.

No model choice is tuned on the final test set. ARCH/GARCH are omitted transparently if the optional package is not installed. GARCH is not claimed to improve accuracy without actual scores.

Return forecast baselines (independently scored): always-zero, expanding historical mean and an intercept-inclusive OLS AR(1) fit on lagged training returns. A volatility-model forecast is not treated as a return forecast.

## Splitting and validation

Use strictly sequential daily return timestamps. Default testing begins at max(504, floor(0.75 × n_returns)); each session from there to the last available date forms one one-step-out-of-sample origin/target pair. Earliest session in the evaluation is never included in its own training sample. Adjusted-price transforms use only current and preceding closes; no standardization or feature scaling is fit using future labels.

The project uses expanding-origin evaluation, not a random split and not a shuffled cross-validation. Parameter refits may be costly. Each record contains origin_date and target_date for external leakage review.

## Performance and uncertainty

Let v[t] be predicted daily conditional variance in squared percent units and y[t] = r[t]^2 the noisy realized target.

- QLIKE = average of log(v[t]) + y[t] / v[t]. Lower is better.
- Variance MSE = mean((v[t] - y[t])^2).
- Sigma proxy absolute error = mean(abs(sqrt(v[t]) - abs(r[t]))); this is **not** direct observed sigma.
- Normal conditional-return interval: ±1.95996 × sqrt(v[t]) around zero; observed 95% interval coverage is computed.
- Normal 5% return threshold: -1.64485 × sqrt(v[t]); observed breach fraction is computed. This is not a validated portfolio Value-at-Risk system.
- Return metrics: MAE, RMSE; directional accuracy only when a nonzero directional forecast exists.

For each model with matched dates, compare daily QLIKE against the historical baseline. Use fixed-seed moving-block bootstrap (400 resamples, block length 10) to provide a percentile interval on **mean paired loss difference**. This does not remove model-selection bias, tail risk or dependence on the chosen block length. A CI crossing zero does not prove equality. Results across different test windows should not be casually compared.

## Known limitations

- Squared daily returns are particularly noisy volatility targets. Intraday realized variance and microstructure-cleaned data would give a stronger benchmark.
- No nested hyperparameter-selection split, structural-break detection, distributional model selection, or probability-integral-transform calibration.
- Parameter estimation uncertainty is not propagated into predictive bands; normal predictive bands ignore fat tails and may under-cover extremes.
- Nontrading dates and exchange interruptions require an authoritative market calendar for precise classification.
- Data may be backfilled, split-adjusted, revised or incomplete. Repeated downloads need not match bit-for-bit; manifests fingerprint saved CSV snapshots.
- Training cutoff varies with final sample length; adding history later changes the holdout definition. For precise comparisons, fix start/end and archive source hashes.
- The test period is a historical sample, not evidence of forward reliability.
