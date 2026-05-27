# Report Summary - Caffeine Hypothesis Test

## Objective

Use Python to perform a one-sample Z-test evaluating whether the average caffeine content in a cup of coffee differs from a claimed population mean of 120 mg.

## Hypotheses

- Null hypothesis: the true mean caffeine content is 120 mg.
- Alternative hypothesis: the true mean caffeine content is different from 120 mg.

## Summary statistics

- Sample size: 50
- Sample mean: 120.5800 mg
- Population standard deviation: 15 mg
- Z-statistic: 0.2734
- Critical value for a two-tailed test at alpha = 0.05: plus or minus 1.9600
- P-value: 0.7845
- Decision: Fail to reject the null hypothesis

## Visualization

The report includes a histogram of the sample caffeine values with vertical reference lines for the sample mean and the claimed mean of 120 mg. The sample mean is close to the claimed mean, which visually supports the statistical decision.

## Interpretation

Because the p-value is much larger than 0.05 and the Z-statistic falls between the critical values of -1.9600 and 1.9600, the sample does not provide strong evidence that the true average caffeine content differs from 120 mg. Based on the sample, the company's caffeine-content claim appears statistically reasonable.

## Portfolio framing

This project demonstrates a standard statistical testing workflow: define hypotheses, compute a test statistic, compare against a rejection threshold, interpret the p-value, visualize the sample data, and communicate the conclusion clearly.
