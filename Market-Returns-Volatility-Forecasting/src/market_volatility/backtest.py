"""Expanding-origin, one-session-ahead forecasting and paired scoring."""

from __future__ import annotations

import math

import numpy as np
import pandas as pd
from scipy.stats import norm

from .models import ArchRefitModel, ar1_prediction, ewma_sigma, historical_sigma


def moving_block_ci(values, *, draws: int = 400, block: int = 10, seed: int = 2026):
    """95% bootstrap CI for average paired loss difference, conditional on sample."""
    x = np.asarray(values, dtype=float)
    x = x[np.isfinite(x)]
    if len(x) < max(30, block * 2):
        return (float("nan"), float("nan"))
    rng = np.random.default_rng(seed)
    starts = np.arange(len(x) - block + 1)
    means = np.empty(draws)
    for j in range(draws):
        picked = rng.choice(starts, size=math.ceil(len(x) / block), replace=True)
        indices = np.concatenate([np.arange(k, k + block) for k in picked])[:len(x)]
        means[j] = np.mean(x[indices])
    return tuple(float(v) for v in np.quantile(means, [0.025, 0.975]))


def backtest(returns: pd.Series, *, min_train: int = 504, test_fraction: float = 0.25,
             refit_every: int = 21, include_arch: bool = True):
    """All forecasts at t use only observations through the previous session."""
    r = returns.dropna().astype(float)
    if not r.index.is_unique or not r.index.is_monotonic_increasing:
        raise ValueError("Return timestamps must be unique and increasing")
    if not np.isfinite(r.to_numpy()).all():
        raise ValueError("Returns must be finite")
    if not 0.05 <= test_fraction <= 0.5:
        raise ValueError("test_fraction must be in [0.05, 0.5]")
    first = max(min_train, math.floor(len(r) * (1.0 - test_fraction)))
    if len(r) - first < 30:
        raise ValueError("Require at least 30 genuine out-of-sample sessions")
    arch_models = {}
    arch_status = "disabled by flag"
    if include_arch:
        try:
            import arch  # noqa: F401

            arch_models = {
                name: ArchRefitModel(name, refit_every=refit_every, min_obs=min_train)
                for name in ("ARCH(1)", "GARCH(1,1)")
            }
            arch_status = "enabled"
        except ImportError:
            arch_status = "arch package unavailable; models omitted"
    errors = []
    volatility_rows, return_rows = [], []
    for i in range(first, len(r)):
        past = r.iloc[:i]
        observed = float(r.iloc[i])
        origin = str(r.index[i - 1].date())
        target = str(r.index[i].date())
        scales = {
            "Historical 21d": historical_sigma(past),
            "EWMA 0.94": ewma_sigma(past),
        }
        for name, model in arch_models.items():
            try:
                scales[name] = model.forecast(past)
            except (ValueError, RuntimeError, FloatingPointError, np.linalg.LinAlgError) as exc:
                errors.append({"target_date": target, "model": name, "error": str(exc)})
                scales[name] = float("nan")
        for name, sigma in scales.items():
            if not np.isfinite(sigma) or sigma <= 0:
                continue
            variance = max(sigma ** 2, 1e-10)
            volatility_rows.append({
                "origin_date": origin, "target_date": target,
                "model": name, "pred_sigma_daily_pct": sigma,
                "pred_variance_pct2": variance,
                "observed_log_return_pct": observed,
                "observed_abs_return_pct": abs(observed),
                "observed_squared_return_pct2": observed ** 2,
                "interval_lower_pct": -norm.ppf(0.975) * sigma,
                "interval_upper_pct": norm.ppf(0.975) * sigma,
                "var_5pct_return_threshold": norm.ppf(0.05) * sigma,
            })
        predictions = {
            "Zero return": 0.0,
            "Expanding mean": float(past.mean()),
            "AR(1) expanding OLS": ar1_prediction(past),
        }
        for name, predicted in predictions.items():
            return_rows.append({
                "origin_date": origin, "target_date": target,
                "model": name, "pred_return_pct": predicted,
                "observed_log_return_pct": observed,
            })
    vol = pd.DataFrame(volatility_rows)
    ret = pd.DataFrame(return_rows)
    if vol.empty or ret.empty:
        raise RuntimeError("No valid forecasts produced")
    return vol, ret, {
        "first_test_date": str(r.index[first].date()),
        "last_test_date": str(r.index[-1].date()),
        "train_observations_at_first_origin": first,
        "out_of_sample_sessions": int(len(r) - first),
        "evaluation_horizon": "one next observed trading session",
        "arch_status": arch_status,
        "arch_fit_counts": {k: v.fit_count for k, v in arch_models.items()},
        "model_errors": errors[:100],
        "model_error_count": len(errors),
        "bootstrap_seed": 2026,
        "forward_information_policy": "No forecast uses observation from target date or later.",
    }


def score_volatility(forecasts: pd.DataFrame) -> pd.DataFrame:
    """Squared next-day return is a noisy, unbiased variance target under zero mean."""
    names = forecasts["model"].unique()
    pivot = forecasts.pivot(index="target_date", columns="model",
                            values="pred_variance_pct2")
    realized = forecasts.drop_duplicates("target_date").set_index(
        "target_date"
    )["observed_squared_return_pct2"]
    benchmark = pivot["Historical 21d"] if "Historical 21d" in pivot else None
    rows = []
    for name in names:
        subset = forecasts.loc[forecasts["model"] == name].copy()
        variance = subset["pred_variance_pct2"].to_numpy()
        rv = subset["observed_squared_return_pct2"].to_numpy()
        sigma = subset["pred_sigma_daily_pct"].to_numpy()
        observed = subset["observed_log_return_pct"].to_numpy()
        qlike = np.log(variance) + rv / variance
        inside = (observed >= subset["interval_lower_pct"].to_numpy()) & (
            observed <= subset["interval_upper_pct"].to_numpy()
        )
        var_breach = observed < subset["var_5pct_return_threshold"].to_numpy()
        aligned = pivot[name].dropna().index.intersection(benchmark.dropna().index)
        if benchmark is not None and len(aligned):
            model_loss = np.log(pivot.loc[aligned, name]) + (
                realized.loc[aligned] / pivot.loc[aligned, name]
            )
            baseline_loss = np.log(benchmark.loc[aligned]) + (
                realized.loc[aligned] / benchmark.loc[aligned]
            )
            low, high = moving_block_ci((model_loss - baseline_loss).to_numpy())
        else:
            low, high = (float("nan"), float("nan"))
        rows.append({
            "model": name, "n_forecasts": len(subset),
            "qlike_lower_better": float(np.mean(qlike)),
            "mse_variance_pct4": float(np.mean((variance - rv) ** 2)),
            "mae_sigma_vs_abs_return_pct": float(np.mean(np.abs(sigma - np.abs(observed)))),
            "normal_interval_95_coverage": float(np.mean(inside)),
            "normal_var_5pct_breach_rate": float(np.mean(var_breach)),
            "paired_qlike_diff_vs_hist_ci_low": low,
            "paired_qlike_diff_vs_hist_ci_high": high,
        })
    return pd.DataFrame(rows).sort_values("qlike_lower_better").reset_index(drop=True)


def score_returns(forecasts: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for name, sub in forecasts.groupby("model", sort=False):
        pred, obs = sub["pred_return_pct"], sub["observed_log_return_pct"]
        direction = float("nan")
        if (pred != 0).any():
            direction = float(np.mean(np.sign(pred) == np.sign(obs)))
        rows.append({
            "model": name, "n_forecasts": int(len(sub)),
            "mae_return_pct": float(np.mean(np.abs(pred - obs))),
            "rmse_return_pct": float(np.sqrt(np.mean((pred - obs) ** 2))),
            "directional_accuracy_nonzero_forecast": direction,
        })
    return pd.DataFrame(rows).sort_values("rmse_return_pct").reset_index(drop=True)
