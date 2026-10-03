# Caffeine Hypothesis Test

## Project overview

This project demonstrates a two-sided one-sample **t-test** using 50 illustrative caffeine-content values and an illustrative benchmark mean of 120 mg.

The repository does **not** document where the 50 values came from, and it does not document a company, product, label, or external source for the 120 mg benchmark. For that reason, the project is presented as a reproducible statistical demonstration rather than as an empirical validation of a real company's caffeine claim.

See [`DATA_PROVENANCE.md`](DATA_PROVENANCE.md) for the provenance status and the conditions required before giving the analysis an empirical or quality-control interpretation.

## What the repository supports

The repository supports these statements:

- The notebook contains 50 fixed numeric observations expressed in milligrams.
- The sample mean is 120.58 mg.
- The sample standard deviation is approximately 2.9972 mg.
- With a two-sided one-sample t-test against 120 mg at `alpha = 0.05`, the test statistic is approximately 1.3683 with 49 degrees of freedom.
- The two-sided p-value is approximately 0.1774, so the analysis fails to reject the null hypothesis at the 5% significance level.
- A 95% confidence interval for the mean is approximately 119.7282 mg to 121.4318 mg.

The repository does **not** support treating the observations as verified measurements from a named population, treating 120 mg as a documented company's advertised value, or treating a population standard deviation of 15 mg as known.

## Questions answered

- How is a one-sample t-test performed when the population standard deviation is not known?
- How far is the sample mean from an illustrative benchmark of 120 mg relative to the sample uncertainty?
- What do the t-statistic, confidence interval, and p-value imply for this illustrative dataset?
- What limitations must be disclosed before interpreting a statistical result as evidence about a real product or company?

## Method

- Test type: Two-sided one-sample t-test
- Sample size: 50
- Benchmark mean: 120 mg (illustrative; no external provenance documented)
- Sample mean: 120.5800 mg
- Sample standard deviation: 2.9972 mg
- Degrees of freedom: 49
- t-statistic: 1.3683
- Two-tailed critical t-value at `alpha = 0.05`: plus or minus 2.0096
- P-value: 0.1774
- 95% confidence interval: [119.7282, 121.4318] mg
- Decision: Fail to reject the null hypothesis

Failing to reject the null hypothesis does not prove that the true mean equals 120 mg. It means only that this illustrative sample does not provide sufficient evidence of a difference at the chosen significance level.

## Files

- `Project-2.ipynb`: runnable notebook containing the data, one-sample t-test, confidence interval, histogram, assumptions, and limitations.
- `REPORT_SUMMARY.md`: concise written interpretation of the analysis.
- `DATA_PROVENANCE.md`: provenance record explaining what is and is not known about the inputs.

## Portfolio framing

This project demonstrates inferential statistics, transparent assumption handling, uncertainty quantification, Python-based statistical analysis, data visualization, and responsible communication of limitations.

It should be described as an **illustrative statistical analysis** unless and until the dataset and benchmark are replaced with verifiable empirical inputs and their sources are documented.
