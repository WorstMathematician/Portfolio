<div align="center">

# Jeffrey Morales

### Finance Systems · Data Analytics · FP&A · Applied Statistics

A work-in-progress portfolio focused on turning financial and operational data into clear analysis, decision support, and reproducible reporting.

[Featured Projects](#featured-projects) · [Analytics & Statistics](#analytics--statistics) · [Repository Guide](docs/README.md) · [How to Run](docs/RUNNING_PROJECTS.md)

</div>

---

> **Portfolio status:** Active and evolving. Projects are refined as documentation, validation, reproducibility, and presentation improve. The goal is to show finished work clearly while keeping the analytical process transparent.

## Welcome

This repository is the central home for my portfolio projects across finance, forecasting, data analysis, statistical modeling, and automation. It is designed for quick review by hiring managers, collaborators, and anyone interested in how I approach a business or analytical problem.

Each featured project is organized around four questions:

1. **What problem is being solved?**
2. **What data and methods are used?**
3. **What result or decision does the analysis support?**
4. **Can the work be inspected and rerun responsibly?**

## Featured Projects

| Project | Focus | Selected evidence | Skills demonstrated |
|---|---|---|---|
| **[Program Finance Control Tower](Program-Finance-Control-Tower/README.md)** | Program finance & forecast review | 10 workstreams reviewed; 3 placed on the management watchlist | EAC, ETC, CPI, margin analysis, KPI design, executive reporting |
| **[Budget vs. Actual FP&A Variance Analysis](Budget-vs-Actual-FPA-Variance-Analysis/README.md)** | FP&A & management reporting | 97.5% forecast accuracy; net variance of -2.5% in the scenario dataset | Variance analysis, materiality, forecast review, management commentary |
| **[LA Housing Affordability Forecasting](LA-Housing-Affordability-Forecasting/README.md)** | Applied data science & public policy | 1,248 ZIP-year observations; final ROC-AUC 0.9498 | Public-data integration, feature engineering, classification, leakage-aware modeling |
| **[Defense Contractor Peer Benchmarking](Defense-Contractor-Peer-Benchmarking/README.md)** | Strategic finance & benchmarking | 100 companies in the latest-year benchmark; 36.1% top-five concentration | Peer benchmarking, CAGR analysis, market concentration, scenario planning |

## Finance & Decision Support

### Program Finance Control Tower
Transforms period-level cost data into a management control view for forecast review. The project calculates EAC, ETC, CPI, cost variance, projected margin, and watchlist status, then packages the results into decision-ready outputs.

**Start here:** [Project overview and results →](Program-Finance-Control-Tower/README.md)

### Budget vs. Actual FP&A Variance Analysis
Builds a monthly FP&A variance package from budget and actual expense data, highlighting material drivers, forecast accuracy, and areas requiring management follow-up.

**Start here:** [Project overview and results →](Budget-vs-Actual-FPA-Variance-Analysis/README.md)

### Defense Contractor Peer Benchmarking
Uses a scenario dataset to compare manufacturers by estimated category revenue, market concentration, geographic exposure, and multi-year growth. It then converts peer growth into downside, base, and upside planning references.

**Start here:** [Project overview and results →](Defense-Contractor-Peer-Benchmarking/README.md)

## Analytics & Statistics

### LA Housing Affordability Forecasting
Analyzes Los Angeles County affordability pressure from 2015–2024 and models 2025 cost-burden risk using public income and rent data.

**Start here:** [Project overview and results →](LA-Housing-Affordability-Forecasting/README.md)

### Height-Weight Linear Regression
A regression project with an explicit separation between historical empirical results and a runnable synthetic demonstration. The refactored notebook emphasizes reproducibility and honest result provenance.

**Explore:** [Height-Weight Linear Regression →](Height-Weight-Linear-Regression/README.md)

### Caffeine Hypothesis Test
A statistical inference project demonstrating one-sample hypothesis testing, decision rules, and communication of uncertainty.

**Explore:** [Caffeine Hypothesis Test →](Caffeine-Hypothesis-Test/README.md)

### Bayesian Coin Flipping
A compact Bayesian updating project using a Beta prior, simulated observations, and posterior inference to show how evidence changes probability estimates.

**Explore:** [Binomial Coin Flipping →](Binomial-Coin-Flipping/README.md)

## What This Portfolio Emphasizes

| Capability | How it appears in the portfolio |
|---|---|
| **Financial analysis** | Budget variance, program controls, forecast review, peer benchmarking |
| **Decision support** | KPI scorecards, management watchlists, executive summaries |
| **Data analysis** | Cleaning, reshaping, aggregation, diagnostics, reproducible pipelines |
| **Statistical modeling** | Regression, classification, hypothesis testing, Bayesian updating |
| **Communication** | Business framing, limitations, source notes, concise interpretation |
| **Reproducibility** | Data provenance notes, runnable code paths, automated repository validation |

## Repository Guide

Supporting documentation is indexed separately so the portfolio remains easy to scan.

- **[Documentation index](docs/README.md)** — repository-level supporting material
- **[Dataset notes](docs/DATASETS.md)** — source labels and scenario-data context
- **[Running the projects](docs/RUNNING_PROJECTS.md)** — local execution guidance
- **[KPI guide](docs/KPI_GUIDE.md)** — finance-project metrics and visualization intent
- **[Finance project index](docs/FINANCE_PROJECTS.md)** — overview of the finance-focused case studies

## Quality & Validation

The repository uses GitHub Actions to validate:

- Python compilation
- critical lint errors
- non-blocking style findings
- Jupyter notebook structure
- pytest tests when test files are present

Workflow: [`.github/workflows/portfolio-validation.yml`](.github/workflows/portfolio-validation.yml)

---

<div align="center">

### Thanks for visiting.

The best place to begin is the **[Featured Projects](#featured-projects)** section above.

</div>
