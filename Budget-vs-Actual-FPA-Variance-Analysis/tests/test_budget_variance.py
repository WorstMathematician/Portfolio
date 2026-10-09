"""Synthetic regression cases: never interpreted as original published results."""
import csv
import importlib.util
from pathlib import Path

import pytest

MODULE = Path(__file__).resolve().parents[1] / "src" / "budget_variance.py"
spec = importlib.util.spec_from_file_location("budget_variance_portfolio", MODULE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def pair(month, budget, actual):
    return [
        {"Expenses": "Budget", "Month": month, "Operations": budget},
        {"Expenses": "Actual", "Month": month, "Operations": actual},
    ]


def test_ordinary_expense_variance():
    detail = mod.validate_and_pair(pair("Jan", 100, 112), ["Operations"])
    kpi = mod.calculate_kpis(detail)
    assert kpi["net_variance"] == 12
    assert kpi["net_variance_pct"] == pytest.approx(.12)
    assert kpi["material_variance_rate"] == 1
    assert detail[0]["variance_type"] == "Unfavorable"


def test_opposing_variances_not_hidden_by_net_adherence():
    rows = [
        {"Expenses": "Budget", "Month": "Jan", "A": 100, "B": 100},
        {"Expenses": "Actual", "Month": "Jan", "A": 150, "B": 50},
    ]
    k = mod.calculate_kpis(mod.validate_and_pair(rows, ["A", "B"]))
    assert k["net_variance"] == 0
    assert k["aggregate_budget_adherence"] == 1
    assert k["weighted_absolute_budget_error"] == pytest.approx(.5)
    assert k["material_variance_rate"] == 1
    assert k["forecast_accuracy"] is None


def test_materiality_boundary_and_zero_budget():
    rows = [
        {"Expenses": "Budget", "Month": "Jan", "A": 100, "B": 0, "C": 0},
        {"Expenses": "Actual", "Month": "Jan", "A": 110, "B": 5, "C": 0},
    ]
    detail = mod.validate_and_pair(rows, ["A", "B", "C"])
    assert sum(r["material_variance"] for r in detail) == 2
    assert detail[1]["variance_pct"] is None
    assert detail[1]["material_variance"] is True
    assert detail[2]["material_variance"] is False
    assert mod.calculate_kpis(detail)["zero_budget_line_count"] == 2


def test_aggregation_is_account_and_month_consistent():
    rows = pair("Jan", 100, 110) + pair("Feb", 200, 180)
    detail = mod.validate_and_pair(rows, ["Operations"])
    k = mod.calculate_kpis(detail)
    assert k["total_budget"] == 300
    assert k["total_actual"] == 290
    assert k["net_variance"] == -10
    assert k["gross_absolute_variance"] == 30
    assert k["average_monthly_absolute_net_variance_pct"] == pytest.approx(.1)
    assert sum(r["variance"] for r in mod.summarize(detail, "account")) == -10
    assert sum(r["variance"] for r in mod.summarize(detail, "month")) == -10


@pytest.mark.parametrize("rows", [
    pair("Jan", "", 4),
    pair("Jan", -1, 4),
    pair("Jan", float("nan"), 4),
    pair("Jan", 10, 4) + pair("Jan", 10, 4),
    [{"Expenses": "Forecast", "Month": "Jan", "Operations": 10}] +
    [{"Expenses": "Actual", "Month": "Jan", "Operations": 10}],
    [{"Expenses": "Budget", "Month": "Jan", "Operations": 10}],
])
def test_invalid_inputs_rejected(rows):
    with pytest.raises(ValueError):
        mod.validate_and_pair(rows, ["Operations"])


def test_pipeline_emits_scorecard_and_summary(tmp_path):
    source = tmp_path / "demo.csv"
    with source.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=["Expenses", "Month", "Operations"])
        writer.writeheader()
        writer.writerows(pair("Jan", 100, 105))
    output = tmp_path / "generated"
    mod.run(source, output)
    assert len(list(output.iterdir())) == 6
    assert "aggregate_budget_adherence" in (output / "kpi_scorecard.csv").read_text()
    assert "Forecast accuracy: unavailable" in (output / "executive_summary.md").read_text()
