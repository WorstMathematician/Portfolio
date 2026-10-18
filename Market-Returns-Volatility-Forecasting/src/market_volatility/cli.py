"""Command-line runner. Network failure is fatal, never converted to synthetic data."""

from __future__ import annotations

import argparse
import json
from datetime import date, timedelta
from pathlib import Path

from .backtest import backtest, score_returns, score_volatility
from .data import download_prices, load_price_csv, validate_prices, write_acquisition
from .features import describe_returns, make_features
from .report import save_diagnostic_plots


def build_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--symbol", default="SPY", help="One US-listed liquid asset, e.g. SPY")
    parser.add_argument("--start", default="2010-01-01")
    parser.add_argument("--end", default=(date.today() + timedelta(days=1)).isoformat(),
                        help="Exclusive end date")
    parser.add_argument("--input-csv", type=Path, help="Local OHLCV export with Date and Adj Close")
    parser.add_argument("--source-label", help="Mandatory provenance when using --input-csv")
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/SPY"))
    parser.add_argument("--min-train", type=int, default=504)
    parser.add_argument("--test-fraction", type=float, default=0.25)
    parser.add_argument("--refit-every", type=int, default=21)
    parser.add_argument("--skip-arch", action="store_true")
    return parser


def run(args):
    output = args.output_dir
    if args.input_csv:
        if not args.source_label:
            raise ValueError("--source-label is required with --input-csv")
        raw = load_price_csv(args.input_csv)
        source = "User-supplied CSV: " + args.source_label + " (not independently verified)"
    else:
        raw = download_prices(args.symbol, args.start, args.end)
        source = "Yahoo Finance daily history via yfinance"
    frame, audit = validate_prices(raw, min_rows=max(400, args.min_train + 31))
    manifest = write_acquisition(
        frame, audit, output, symbol=args.symbol, source=source,
        start=args.start, end=args.end,
    )
    features = make_features(frame)
    features.rename_axis("Date").to_csv(output / "features.csv")
    summary = describe_returns(features["log_return_pct"])
    returns = features["log_return_pct"].dropna()
    vol, ret, metadata = backtest(
        returns, min_train=args.min_train, test_fraction=args.test_fraction,
        refit_every=args.refit_every, include_arch=not args.skip_arch,
    )
    vol.to_csv(output / "volatility_forecasts.csv", index=False)
    ret.to_csv(output / "return_forecasts.csv", index=False)
    score_volatility(vol).to_csv(output / "volatility_scores.csv", index=False)
    score_returns(ret).to_csv(output / "return_scores.csv", index=False)
    (output / "diagnostics.json").write_text(json.dumps(summary, indent=2) + "\n")
    (output / "evaluation.json").write_text(json.dumps(metadata, indent=2) + "\n")
    save_diagnostic_plots(features, vol, output / "figures")
    print(json.dumps({
        "output_directory": str(output), "source": manifest["source"],
        "observations": audit["rows"],
        "out_of_sample_sessions": metadata["out_of_sample_sessions"],
        "arch_status": metadata["arch_status"],
        "model_error_count": metadata["model_error_count"],
        "scores_are_observed": True,
    }, indent=2))


def main():
    run(build_parser().parse_args())


if __name__ == "__main__":
    main()
