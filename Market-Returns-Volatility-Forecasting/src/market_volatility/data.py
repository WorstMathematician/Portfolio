"""Price acquisition, strict input checks, and auditable provenance."""

from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

PRICE_COLUMNS = ("Open", "High", "Low", "Close", "Adj Close", "Volume")
ACTION_COLUMNS = ("Dividends", "Stock Splits")
SYMBOL_PATTERN = re.compile(r"^[A-Z0-9.^_-]{1,15}$")


def download_prices(symbol: str, start: str, end: str) -> pd.DataFrame:
    """Obtain daily Yahoo Finance observations through yfinance; no fallback data."""
    if not SYMBOL_PATTERN.fullmatch(symbol):
        raise ValueError("Symbol must contain 1-15 uppercase ticker characters")
    if pd.Timestamp(start) >= pd.Timestamp(end):
        raise ValueError("Start must precede end (exclusive)")
    import yfinance as yf

    raw = yf.download(
        symbol, start=start, end=end, interval="1d",
        auto_adjust=False, actions=True, progress=False, threads=False,
        multi_level_index=False, keepna=True, repair=False,
    )
    if raw is None or raw.empty:
        raise RuntimeError("Market data unavailable; no substitute data created")
    return raw


def validate_prices(raw: pd.DataFrame, *, min_rows: int = 400):
    """Reject corrupt inputs and retain nonfatal anomaly candidates for review."""
    if not isinstance(raw, pd.DataFrame) or raw.empty:
        raise ValueError("Empty price input")
    frame = raw.copy()
    if isinstance(frame.columns, pd.MultiIndex):
        raise ValueError("Expected one ticker and flat OHLCV columns")
    frame.index = pd.to_datetime(frame.index, errors="raise", utc=True).tz_localize(None).normalize()
    if frame.index.isna().any() or frame.index.has_duplicates or not frame.index.is_monotonic_increasing:
        raise ValueError("Invalid, duplicate, or unsorted trading dates")
    if (frame.index.dayofweek >= 5).any():
        raise ValueError("Weekend daily bars found in data")
    missing = [name for name in PRICE_COLUMNS if name not in frame.columns]
    if missing:
        raise ValueError("Missing required fields: " + ", ".join(missing))
    if frame[list(PRICE_COLUMNS)].isna().any().any():
        raise ValueError("Missing OHLCV/adjusted close; inspect provider before proceeding")
    for name in PRICE_COLUMNS + ACTION_COLUMNS:
        if name in frame:
            frame[name] = pd.to_numeric(frame[name], errors="raise")
    if not np.isfinite(frame[list(PRICE_COLUMNS)].to_numpy(dtype=float)).all():
        raise ValueError("Non-finite price/volume observations")
    if (frame[["Open", "High", "Low", "Close", "Adj Close"]] <= 0).any().any():
        raise ValueError("Prices must be strictly positive")
    if (frame["Volume"] < 0).any():
        raise ValueError("Volume cannot be negative")
    tolerance = 1e-7
    if ((frame["High"] + tolerance < frame[["Open", "Close", "Low"]].max(axis=1)) |
            (frame["Low"] - tolerance > frame[["Open", "Close", "High"]].min(axis=1))).any():
        raise ValueError("OHLC high/low bounds are inconsistent")
    for field in ACTION_COLUMNS:
        if field not in frame:
            frame[field] = 0.0
        if not np.isfinite(frame[field]).all() or (frame[field] < 0).any():
            raise ValueError("Corporate-action values invalid")
    if len(frame) < min_rows:
        raise ValueError(f"Insufficient daily bars ({len(frame)} < {min_rows})")
    returns = np.log(frame["Adj Close"]).diff() * 100.0
    extreme = returns.abs() > 20.0
    weekday_candidates = pd.bdate_range(frame.index.min(), frame.index.max()).difference(frame.index)
    day_gaps = frame.index.to_series().diff().dt.days.dropna()
    adjustment_ratio = frame["Adj Close"] / frame["Close"]
    diagnostics = {
        "rows": int(len(frame)),
        "first_date": frame.index.min().date().isoformat(),
        "last_date": frame.index.max().date().isoformat(),
        "weekdays_without_bars_including_holidays": int(len(weekday_candidates)),
        "largest_calendar_day_gap": int(day_gaps.max()) if len(day_gaps) else 0,
        "abs_log_return_over_20pct_count": int(extreme.sum()),
        "abs_log_return_over_20pct_dates": [str(d.date()) for d in returns.index[extreme][:50]],
        "dividend_event_count": int((frame["Dividends"] > 0).sum()),
        "split_event_count": int((frame["Stock Splits"] > 0).sum()),
        "adjusted_to_close_ratio_min": float(adjustment_ratio.min()),
        "adjusted_to_close_ratio_max": float(adjustment_ratio.max()),
        "action_warning": "Confirm vendor treatment of dividends, splits and restatements.",
        "gap_warning": "Weekday gaps include exchange holidays; not a market-calendar missing-session count.",
    }
    return frame, diagnostics


def load_price_csv(path: Path) -> pd.DataFrame:
    """Read a user-provided provider export without assuming it is authentic."""
    return pd.read_csv(path, index_col="Date", parse_dates=["Date"])


def write_acquisition(frame: pd.DataFrame, audit: dict, output: Path, *,
                      symbol: str, source: str, start: str, end: str) -> dict:
    output.mkdir(parents=True, exist_ok=True)
    path = output / "prices.csv"
    frame.rename_axis("Date").to_csv(path, index=True, float_format="%.12g")
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    manifest = {
        "symbol": symbol, "source": source,
        "requested_start_inclusive": start, "requested_end_exclusive": end,
        "acquired_utc": datetime.now(timezone.utc).isoformat(),
        "file_sha256": digest, "quality": audit,
        "price_basis": "Yahoo Adj Close (split and distribution adjusted) when online",
        "source_verified_externally": False,
    }
    (output / "provenance.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest
