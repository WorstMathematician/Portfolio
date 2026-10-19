"""Leakage-safe conditional-scale models operating in percent return units."""

from __future__ import annotations

import numpy as np
import pandas as pd


def historical_sigma(history: pd.Series, window: int = 21) -> float:
    if len(history) < window:
        raise ValueError("Insufficient history for rolling scale forecast")
    return float(history.iloc[-window:].std(ddof=1))


def ewma_sigma(history: pd.Series, decay: float = 0.94) -> float:
    """RiskMetrics-style filter, warm start on first 30 known returns."""
    if not 0 < decay < 1 or len(history) < 31:
        raise ValueError("EWMA requires >=31 past returns and 0<decay<1")
    values = history.to_numpy(dtype=float)
    variance = float(np.var(values[:30], ddof=1))
    for observation in values[30:]:
        variance = decay * variance + (1.0 - decay) * observation ** 2
    return float(np.sqrt(max(variance, 1e-12)))


def ar1_prediction(history: pd.Series) -> float:
    """OLS AR(1) on training observations only; intercept is included."""
    if len(history) < 60:
        raise ValueError("Insufficient data for AR(1)")
    x = history.to_numpy(dtype=float)
    predictors = np.column_stack([np.ones(len(x) - 1), x[:-1]])
    coefficients, _, _, _ = np.linalg.lstsq(predictors, x[1:], rcond=None)
    return float(coefficients[0] + coefficients[1] * x[-1])


class ArchRefitModel:
    """Refit coefficients at set origins; filter all observations known at each origin."""

    def __init__(self, kind: str, *, refit_every: int = 21, min_obs: int = 504):
        if kind not in ("ARCH(1)", "GARCH(1,1)"):
            raise ValueError("Unknown ARCH specification")
        if refit_every < 1:
            raise ValueError("refit_every must be positive")
        self.kind = kind
        self.refit_every = refit_every
        self.min_obs = min_obs
        self.params = None
        self.last_fit_n = 0
        self.fit_count = 0

    def _model(self, series):
        from arch import arch_model

        settings = (
            dict(vol="ARCH", p=1, q=0) if self.kind == "ARCH(1)"
            else dict(vol="GARCH", p=1, q=1)
        )
        return arch_model(
            series, mean="Zero", dist="normal", rescale=False, **settings
        )

    def forecast(self, history: pd.Series) -> float:
        if len(history) < self.min_obs:
            return float("nan")
        if self.params is None or len(history) - self.last_fit_n >= self.refit_every:
            fitted = self._model(history).fit(disp="off", show_warning=False)
            if fitted.convergence_flag != 0:
                raise RuntimeError(f"{self.kind} optimizer did not converge")
            self.params = fitted.params.to_numpy(dtype=float)
            self.last_fit_n = len(history)
            self.fit_count += 1
        filtered = self._model(history).fix(self.params)
        variance = float(filtered.forecast(horizon=1).variance.iloc[-1, 0])
        if not np.isfinite(variance) or variance <= 0:
            raise RuntimeError(f"{self.kind} produced invalid conditional variance")
        return float(np.sqrt(variance))
