"""Write reproducible static diagnostic graphics from observed data."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from statsmodels.graphics.tsaplots import plot_acf


def save_diagnostic_plots(features: pd.DataFrame, forecasts: pd.DataFrame,
                          output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    r = features["log_return_pct"].dropna()
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(features.index, features["adjusted_close"], linewidth=1)
    ax.set(title="Provider-adjusted close (observed)", xlabel="Session", ylabel="Adjusted price")
    fig.tight_layout()
    fig.savefig(output / "adjusted_price.png", dpi=140)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.hist(r, bins=65, density=True, alpha=0.75, label="Observed returns")
    ax.axvline(0, color="black", linewidth=0.7)
    ax.set(title="Observed daily log returns", xlabel="Log return (%)", ylabel="Density")
    fig.tight_layout()
    fig.savefig(output / "return_distribution.png", dpi=140)
    plt.close(fig)

    fig, axes = plt.subplots(2, 1, figsize=(10, 6))
    plot_acf(r, lags=30, ax=axes[0], title="Return autocorrelation")
    plot_acf(r ** 2, lags=30, ax=axes[1], title="Squared-return autocorrelation")
    fig.tight_layout()
    fig.savefig(output / "autocorrelation.png", dpi=140)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(features.index, features["realized_21d_annualized_pct"],
            label="Observed trailing 21d annualized volatility")
    benchmark = forecasts.loc[forecasts["model"] == "EWMA 0.94"].copy()
    if not benchmark.empty:
        ax.plot(pd.to_datetime(benchmark["target_date"]),
                benchmark["pred_sigma_daily_pct"] * np.sqrt(252),
                label="EWMA 1-step forecast (annualized)", linewidth=1)
    ax.legend()
    ax.set(title="Observed trailing volatility vs ex-ante scale", ylabel="Annualized (%)")
    fig.tight_layout()
    fig.savefig(output / "rolling_and_forecast_volatility.png", dpi=140)
    plt.close(fig)
