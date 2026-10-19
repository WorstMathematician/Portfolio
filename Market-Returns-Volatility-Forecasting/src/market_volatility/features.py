"""Returns and descriptive time-series diagnostics (no fitted model selection)."""

from __future__ import annotations

import warnings

import numpy as np
import pandas as pd
from scipy.stats import jarque_bera, kurtosis, skew
from statsmodels.stats.diagnostic import acorr_ljungbox, het_arch
from statsmodels.tsa.stattools import adfuller, kpss


def make_features(prices: pd.DataFrame) -> pd.DataFrame:
    adjusted = prices["Adj Close"].astype(float)
    frame = pd.DataFrame(index=adjusted.index)
    frame["adjusted_close"] = adjusted
    frame["log_return_pct"] = 100.0 * np.log(adjusted / adjusted.shift(1))
    frame["simple_return_pct"] = 100.0 * adjusted.pct_change(fill_method=None)
    frame["realized_21d_annualized_pct"] = (
        frame["log_return_pct"].rolling(21, min_periods=21).std(ddof=1)
        * np.sqrt(252.0)
    )
    return frame


def describe_returns(returns: pd.Series) -> dict:
    """ADF null: unit root; KPSS null: level stationary. p-values are not proof."""
    r = returns.dropna().astype(float)
    if len(r) < 100:
        raise ValueError("Diagnostics require at least 100 returns")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        adf = adfuller(r, autolag="AIC")
        kpss_result = kpss(r, regression="c", nlags="auto")
        lb = acorr_ljungbox(r, lags=[10], return_df=True)
        lb2 = acorr_ljungbox(r ** 2, lags=[10], return_df=True)
        arch_lm = het_arch(r, nlags=10)
        normality = jarque_bera(r)
    return {
        "n": int(len(r)), "mean_daily_pct": float(r.mean()),
        "std_daily_pct": float(r.std(ddof=1)),
        "skew": float(skew(r, bias=False)),
        "excess_kurtosis": float(kurtosis(r, bias=False)),
        "adf_p_value": float(adf[1]), "kpss_p_value": float(kpss_result[1]),
        "ljung_box_return_lag10_p": float(lb["lb_pvalue"].iloc[-1]),
        "ljung_box_squared_return_lag10_p": float(lb2["lb_pvalue"].iloc[-1]),
        "arch_lm_lag10_p": float(arch_lm[1]),
        "jarque_bera_p": float(normality.pvalue),
        "return_lag1_autocorrelation": float(r.autocorr(1)),
        "squared_return_lag1_autocorrelation": float((r ** 2).autocorr(1)),
        "interpretation": "Diagnostics indicate sample patterns, not forecasting skill.",
    }
