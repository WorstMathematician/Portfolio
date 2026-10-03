# Data Provenance and Assumptions

## Provenance status

As of October 3, 2026, the repository does not contain documentation establishing an external source for the 50 caffeine-content values used in `Project-2.ipynb`.

The repository also does not identify a company, product, product label, dataset, publication, measurement protocol, or other external source that establishes 120 mg as a real advertised caffeine-content claim.

Accordingly, this portfolio version treats both inputs as **illustrative**:

- The 50 hard-coded values are treated as illustrative/synthetic-or-unsourced observations for demonstrating the analysis. They are not presented as verified measurements.
- The 120 mg null mean is treated as an illustrative benchmark. It is not presented as a documented company claim.

This classification describes how the repository may defensibly use the inputs; it does not assert how the values were originally generated.

## Removed assumption: known population standard deviation

An earlier version of the notebook set `sigma = 15` and labeled it as a known population standard deviation. No supporting source or derivation for that value is present in the project files or the notebook's repository history.

Because a known population standard deviation cannot be justified from the repository, the analysis now uses a one-sample t-test and estimates variability with the sample standard deviation.

## Reproducibility versus external validity

The analysis is reproducible because the exact 50 values are embedded in the notebook. Reproducibility does not establish data provenance or external validity.

Without provenance, the repository cannot establish:

- how the observations were collected or generated;
- whether they represent independent observations;
- what product, company, batch, population, or time period they represent;
- whether the measurement units and procedures were independently verified; or
- whether the 120 mg benchmark corresponds to a real-world label or claim.

For those reasons, statistical results from the current values should not be generalized to a real product or company.

## Current statistical assumptions

The one-sample t-test is used as an illustrative inferential procedure. Its usual interpretation assumes that observations are independent and that the sampling distribution of the mean is adequately modeled by the t procedure. Because the sample provenance is unavailable, independence and the underlying sampling process cannot be verified here.

The notebook therefore reports the numerical result while explicitly limiting the conclusion to the illustrative dataset and benchmark.

## Requirements for empirical framing

Before this project is described as a real quality-control or company-claim analysis, document all of the following:

1. The source of the observations, including a stable citation or source file.
2. The product or population represented by the observations.
3. The data-collection or measurement procedure and relevant dates.
4. Why observations can reasonably be treated as independent.
5. The source for the benchmark or advertised claim being tested.
6. Any filtering, cleaning, exclusions, or transformations applied to the raw data.
7. If a Z-test is used, a defensible source establishing the population standard deviation as known in advance; otherwise retain the t-test.

After replacing the illustrative inputs, rerun the notebook and update `README.md`, `REPORT_SUMMARY.md`, and this provenance record with the empirical source information.
