"""Interactive read-only dashboard for real-data model outputs."""

from pathlib import Path
import json

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Market Returns & Volatility", page_icon="📈", layout="wide")
st.title("Market Returns & Volatility Forecasting")
st.caption("Observed history | Out-of-sample forecasts | Explicitly hypothetical risks")
folder = Path(st.sidebar.text_input("Analysis outputs folder", "outputs/SPY")).expanduser()
files = ("features.csv", "volatility_forecasts.csv", "return_forecasts.csv",
         "volatility_scores.csv", "return_scores.csv", "provenance.json",
         "evaluation.json", "diagnostics.json")
if any(not (folder / file).is_file() for file in files):
    st.info("No data loaded. Run the pipeline as described in README.md.")
    st.code("python -m market_volatility.cli --symbol SPY --start 2010-01-01")
    st.stop()


@st.cache_data(show_spinner=False)
def read_results(location: str):
    base = Path(location)
    f = pd.read_csv(base / "features.csv", parse_dates=["Date"]).set_index("Date")
    v = pd.read_csv(base / "volatility_forecasts.csv", parse_dates=["target_date"])
    r = pd.read_csv(base / "return_forecasts.csv", parse_dates=["target_date"])
    vs = pd.read_csv(base / "volatility_scores.csv")
    rs = pd.read_csv(base / "return_scores.csv")
    meta = {key: json.loads((base / (key + ".json")).read_text())
            for key in ("provenance", "diagnostics", "evaluation")}
    return f, v, r, vs, rs, meta


features, forecast, return_forecast, scores, return_scores, info = read_results(str(folder.resolve()))
quality = info["provenance"]["quality"]
eval_info = info["evaluation"]
st.sidebar.write("Source:", info["provenance"]["source"])
st.sidebar.caption(
    quality["first_date"] + " – " + quality["last_date"]
    + " | Yahoo adjustments not independently audited"
)
if quality["abs_log_return_over_20pct_count"]:
    st.sidebar.warning("Extreme return candidates in provenance.json require review.")
model = st.sidebar.selectbox("Choose ex-ante volatility model", sorted(forecast["model"].unique()))
chosen = forecast.loc[forecast["model"] == model].sort_values("target_date")
min_day = features.index.min().date()
max_day = features.index.max().date()
start_day, end_day = st.sidebar.slider(
    "Display window", min_value=min_day, max_value=max_day,
    value=(max(min_day, (features.index.max() - pd.Timedelta(days=730)).date()), max_day),
)
window = features.loc[str(start_day):str(end_day)]
shown = chosen.loc[(chosen["target_date"] >= pd.Timestamp(start_day)) &
                   (chosen["target_date"] <= pd.Timestamp(end_day))]
history, evaluation, diagnostics, risks = st.tabs(
    ["Market history", "Forecast comparisons", "Statistical diagnostics", "Illustrative risk"]
)

with history:
    a, b, c = st.columns(3)
    a.metric("Observed price bars", f'{quality["rows"]:,}')
    b.metric("Latest adjusted close", f'{features["adjusted_close"].iloc[-1]:,.2f}')
    c.metric("Test observations", f'{eval_info["out_of_sample_sessions"]:,}')
    fig = go.Figure()
    fig.add_scatter(x=window.index, y=window["adjusted_close"],
                    name="Observed adjusted close", mode="lines")
    fig.update_layout(title="Observed daily adjusted prices", yaxis_title="Adjusted price")
    st.plotly_chart(fig, use_container_width=True)
    fig = go.Figure()
    fig.add_bar(x=window.index, y=window["log_return_pct"], name="Observed log returns")
    fig.update_layout(title="Observed log return distributions over time",
                      yaxis_title="Daily log return (%)")
    st.plotly_chart(fig, use_container_width=True)
    fig = go.Figure()
    fig.add_scatter(x=window.index, y=window["realized_21d_annualized_pct"],
                    mode="lines", name="Observed trailing 21-session volatility")
    fig.add_scatter(x=shown["target_date"],
                    y=shown["pred_sigma_daily_pct"] * np.sqrt(252),
                    mode="lines", name=f"{model} one-step forecast (annualized)")
    fig.update_layout(title="Trailing realized scale vs forecast scale", yaxis_title="Annualized (%)")
    st.plotly_chart(fig, use_container_width=True)

with evaluation:
    st.write(
        "Chronological out-of-sample evaluation from "
        + eval_info["first_test_date"] + " through " + eval_info["last_test_date"] + ". "
        "Squared daily returns are noisy proxies for conditional variance."
    )
    st.dataframe(scores, use_container_width=True, hide_index=True)
    fig = go.Figure()
    for name, subset in forecast.groupby("model"):
        fig.add_scatter(x=subset["target_date"], y=subset["pred_sigma_daily_pct"],
                        name=name, mode="lines")
    fig.update_layout(title="Competing one-session volatility forecasts",
                      yaxis_title="Ex-ante daily sigma (%)")
    st.plotly_chart(fig, use_container_width=True)
    fig = go.Figure()
    fig.add_scatter(x=shown["target_date"], y=shown["observed_log_return_pct"],
                    name="Observed subsequent return", mode="lines")
    fig.add_scatter(x=shown["target_date"], y=shown["interval_upper_pct"],
                    name="Normal 95% upper", line={"dash": "dot"})
    fig.add_scatter(x=shown["target_date"], y=shown["interval_lower_pct"],
                    name="Normal 95% lower", line={"dash": "dot"})
    fig.update_layout(title="Observed returns vs prior-session predictive intervals",
                      yaxis_title="Daily log return (%)")
    st.plotly_chart(fig, use_container_width=True)
    st.subheader("Return prediction (distinct task)")
    st.dataframe(return_scores, use_container_width=True, hide_index=True)
    st.caption("A zero-return forecast has no directional-accuracy statistic.")

with diagnostics:
    d = info["diagnostics"]
    selected = [
        "mean_daily_pct", "std_daily_pct", "skew", "excess_kurtosis",
        "return_lag1_autocorrelation", "squared_return_lag1_autocorrelation",
        "adf_p_value", "kpss_p_value", "ljung_box_return_lag10_p",
        "ljung_box_squared_return_lag10_p", "arch_lm_lag10_p", "jarque_bera_p",
    ]
    st.dataframe(pd.DataFrame({"Statistic": selected, "Value": [d[key] for key in selected]}),
                 hide_index=True, use_container_width=True)
    st.caption("ADF null: unit root; KPSS null: stationarity. Tests do not imply forecastability.")
    for filename in ("return_distribution.png", "autocorrelation.png",
                     "rolling_and_forecast_volatility.png"):
        graphic = folder / "figures" / filename
        if graphic.exists():
            st.image(str(graphic))
    st.write("Data quality audit:", quality)
    st.write("Optional ARCH/GARCH:", eval_info["arch_status"])
    if eval_info["model_error_count"]:
        st.warning("Model failures recorded in evaluation.json; do not ignore them.")

with risks:
    st.warning(
        "All dollar amounts are hypothetical, not a trading recommendation or validated VaR."
    )
    amount = st.number_input("Illustrative exposure in dollars", value=100000., min_value=100.,
                             step=1000.)
    multiples = st.slider("Assumed sigma shock multiple", 0.5, 5.0, 2.0, 0.5)
    last = chosen.iloc[-1]
    daily_sigma = float(last["pred_sigma_daily_pct"])
    st.metric("Last test-origin predicted daily scale", f"{daily_sigma:.3f}%")
    st.metric("Hypothetical absolute dollar move",
              f"USD {amount * multiples * daily_sigma / 100:,.0f}")
    st.metric("Backtest frequency below normal 5% threshold",
              f'{scores.loc[scores["model"] == model, "normal_var_5pct_breach_rate"].iloc[0]:.1%}')
    st.caption(
        "Hypothetical move = exposure x assumed sigma multiple x historical forecast sigma. "
        "The last origin is not live; normal bands neglect fat tails, liquidity and transaction costs."
    )
