# Report Summary - Binomial Coin Flipping

## Objective

Use Bayesian updating to estimate the probability of getting heads in a coin-flipping experiment using prior beliefs, observed data, and the Beta-Binomial model.

## Model setup

The analysis uses a Beta(2, 2) prior. This prior is centered at 0.5 and represents a mild initial belief that the coin may be fair while still allowing the observed data to move the estimate.

## Simulation results

- Number of flips: 100
- Assumed coin bias: 0.671
- Observed heads: 69
- Observed tails: 31
- Observed proportion of heads: 0.69

## Posterior update

Using the Beta-Binomial update rule:

- Prior: Beta(2, 2)
- Posterior: Beta(2 + 69, 2 + 31)
- Posterior: Beta(71, 33)
- Posterior mean: 0.683

## Interpretation

The posterior mean shifts from the prior center of 0.5 to about 0.683 after observing 69 heads in 100 simulated flips. This indicates evidence that the coin is biased toward heads in the simulated experiment. Additional flips would narrow the posterior distribution and increase confidence in the estimated probability.

## Portfolio framing

This project demonstrates Bayesian updating, probability modeling, simulation, posterior distribution analysis, and visual communication of uncertainty.
