"""Only deterministic synthetic fixtures; test results never masquerade as market data."""

import sys
from pathlib import Path

import pytest

pd = pytest.importorskip("pandas")
np = pytest.importorskip("numpy")
pytest.importorskip("scipy")
pytest.importorskip("statsmodels")
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from market_volatility.backtest import backtest, moving_block_ci, score_returns, score_volatility
from market_volatility.data import validate_prices
from market_volatility.features import make_features
from market_volatility.models import ewma_sigma, historical_sigma


@pytest.fixture
def fixture_prices():
    dates = pd.bdate_range("2019-01-01", periods=735)
    rng = np.random.default_rng(1729)
    close = 100 * np.exp(np.cumsum(rng.normal(0.03, 0.9, len(dates)) / 100))
    frame = pd.DataFrame(index=dates)
    frame["Open"] = close
    frame["Close"] = close
    frame["High"] = close * 1.01
    frame["Low"] = close * 0.99
    frame["Adj Close"] = close * 0.98
    frame["Volume"] = 1000
    frame["Dividends"] = 0.
    frame["Stock Splits"] = 0.
    return frame


def test_quality_and_missing_fields(fixture_prices):
    clean, audit = validate_prices(fixture_prices)
    assert len(clean) == audit["rows"] == 735
    assert audit["split_event_count"] == 0
    with pytest.raises(ValueError, match="Missing"):
        validate_prices(fixture_prices.drop(columns=["Adj Close"]))
    duplicated = pd.concat([fixture_prices, fixture_prices.iloc[-1:]])
    with pytest.raises(ValueError, match="duplicate"):
        validate_prices(duplicated)
    weekend = fixture_prices.copy()
    last = weekend.index[-1]
    next_saturday = last + pd.Timedelta(days=(5 - last.dayofweek) % 7 or 7)
    weekend.index = weekend.index[:-1].append(pd.DatetimeIndex([next_saturday]))
    with pytest.raises(ValueError, match="Weekend"):
        validate_prices(weekend)
    missing = fixture_prices.copy()
    missing.iloc[3, missing.columns.get_loc("Adj Close")] = np.nan
    with pytest.raises(ValueError, match="Missing"):
        validate_prices(missing)


def test_returns_and_features(fixture_prices):
    data = make_features(fixture_prices)
    assert pd.isna(data["log_return_pct"].iloc[0])
    assert np.isclose(data["log_return_pct"].iloc[1],
                      100 * np.log(fixture_prices["Adj Close"].iloc[1] /
                                   fixture_prices["Adj Close"].iloc[0]))
    assert pd.notna(data["realized_21d_annualized_pct"].iloc[21])


def test_forecasts_do_not_observe_the_target(fixture_prices):
    r = make_features(fixture_prices)["log_return_pct"].dropna()
    old, old_returns, audit = backtest(r, min_train=252, test_fraction=.10,
                                     include_arch=False)
    new_r = r.copy()
    new_r.iloc[-1] += 40
    new, new_returns, _ = backtest(new_r, min_train=252, test_fraction=.10,
                                  include_arch=False)
    assert np.allclose(old.tail(2)["pred_sigma_daily_pct"],
                       new.tail(2)["pred_sigma_daily_pct"])
    assert np.allclose(old_returns.tail(3)["pred_return_pct"],
                       new_returns.tail(3)["pred_return_pct"])
    assert audit["out_of_sample_sessions"] >= 30


def test_scoring_and_reproducibility(fixture_prices):
    r = make_features(fixture_prices)["log_return_pct"].dropna()
    vol, ret, _ = backtest(r, min_train=252, include_arch=False)
    result = score_volatility(vol)
    assert set(result["model"]) == {"Historical 21d", "EWMA 0.94"}
    assert result["qlike_lower_better"].notna().all()
    assert result["normal_interval_95_coverage"].between(0, 1).all()
    assert len(score_returns(ret)) == 3
    assert moving_block_ci(np.arange(75.)) == moving_block_ci(np.arange(75.))


def test_scale_inputs():
    history = pd.Series(np.linspace(-2, 3, 100))
    assert historical_sigma(history, window=21) > 0
    assert ewma_sigma(history) > 0
    with pytest.raises(ValueError):
        ewma_sigma(history.iloc[:10])


def test_arch_one_step_if_installed(fixture_prices):
    pytest.importorskip("arch")
    from market_volatility.models import ArchRefitModel

    r = make_features(fixture_prices)["log_return_pct"].dropna()
    model = ArchRefitModel("GARCH(1,1)", min_obs=252, refit_every=21)
    assert model.forecast(r.iloc[:500]) > 0
    assert model.forecast(r.iloc[:501]) > 0
    assert model.fit_count == 1
