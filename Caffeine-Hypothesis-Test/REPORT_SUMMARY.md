# Report Summary - Caffeine Hypothesis Test

## Objective

Demonstrate a two-sided one-sample t-test for a mean using 50 illustrative caffeine-content values and an illustrative benchmark of 120 mg.

This report does not claim that the observations are verified measurements from a real company or product. The repository contains no source for the 50 values and no source establishing 120 mg as a company's advertised value. See `DATA_PROVENANCE.md` for details.

## Hypotheses

For the illustrative benchmark:

- Null hypothesis: the population mean is 120 mg.
- Alternative hypothesis: the population mean is different from 120 mg.

## Why a t-test is used

The previous version set `sigma = 15` and described it as a known population standard deviation, but the repository provides no source or justification for that value. Without a justified known population standard deviation, a one-sample t-test is the appropriate default because it estimates variability from the sample.

## Summary statistics

- Sample size: 50
- Sample mean: 120.5800 mg
- Sample standard deviation: 2.9972 mg
- Standard error: 0.4239 mg
- Degrees of freedom: 49
- t-statistic: 1.3683
- Critical value for a two-tailed test at `alpha = 0.05`: plus or minus 2.0096
- P-value: 0.1774
- 95% confidence interval for the mean: 119.7282 mg to 121.4318 mg
- Decision: Fail to reject the null hypothesis

## Visualization

The notebook includes a histogram of the illustrative caffeine values with reference lines for the sample mean and the 120 mg benchmark. The plot is descriptive only; it does not establish that the values came from a real sampling process.

## Interpretation

At the 5% significance level, the illustrative sample does not provide sufficient evidence that the mean differs from 120 mg. The 95% confidence interval also contains 120 mg.

This result should **not** be interpreted as showing that a company's caffeine-content claim is accurate or statistically validated. The provenance of the sample and benchmark is not established, independence of observations cannot be verified, and the analysis is therefore suitable only as a demonstration of statistical workflow unless verifiable empirical data are substituted.

Failing to reject the null hypothesis is not evidence that the null hypothesis is true; it indicates that the observed difference is not statistically significant under the stated model and significance level.

## Portfolio framing

The defensible portfolio value of this project is the workflow itself: identify the inferential question, choose a test that matches the available assumptions, estimate uncertainty, report the test statistic and confidence interval, visualize the sample, and clearly separate statistical demonstration from empirical claims.
