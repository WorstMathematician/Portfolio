# Binomial Coin Flipping

## Project overview

This project uses Bayesian updating to estimate the probability of getting heads in a coin-flipping experiment. The analysis starts with a Beta prior, simulates observed coin-flip data, updates the posterior distribution, and visualizes how the posterior belief changes after observing data.

## Business and analytical value

Although the example is simple, it demonstrates an important statistical workflow used in analytics and decision-making: combine prior assumptions with observed evidence, update beliefs quantitatively, and communicate uncertainty using a probability distribution.

## Questions answered

- How can prior beliefs be represented mathematically?
- How does observed data update a probability estimate?
- What is the posterior estimate of the probability of heads?
- How does Bayesian updating reduce uncertainty after data is observed?

## Method

- Prior distribution: Beta(2, 2)
- Number of simulated flips: 100
- Observed heads: 69
- Observed tails: 31
- Posterior distribution: Beta(71, 33)
- Posterior mean: 0.683

## Files

- `Project_1_Binomial_Coin_Flipping.ipynb`: runnable notebook for the simulation, posterior update, and visualization.
- `REPORT_SUMMARY.md`: written summary of the PDF report.

## Portfolio framing

This project demonstrates Bayesian reasoning, probability modeling, simulation, visualization, and statistical interpretation.
