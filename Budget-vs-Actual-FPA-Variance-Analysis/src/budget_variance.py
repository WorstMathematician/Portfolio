"""Reproducible expense budget-to-actual reporting; no historical inputs are bundled.

CSV input: Expenses,Month,<one or more expense account columns>.
Excel input uses the same layout and requires openpyxl.
Amounts must be finite, nonnegative expense values. Missing values are errors.
"""
import argparse
import csv
import math
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
THRESHOLD = 0.10


def read_source(path):
    path = Path(path)
    if path.suffix.lower() == ".csv":
        with path.open(newline="", encoding="utf-8-sig") as stream:
            reader = csv.DictReader(stream)
            if not reader.fieldnames:
                raise ValueError("Input has no header")
            headers = reader.fieldnames
            rows = list(reader)
    elif path.suffix.lower() in (".xlsx", ".xlsm"):
        try:
            from openpyxl import load_workbook
        except ImportError as exc:
            raise RuntimeError("Install openpyxl to read Excel input") from exc
        workbook = load_workbook(path, data_only=True, read_only=True)
        sheet = workbook.active
        raw = list(sheet.values)
        workbook.close()
        if not raw:
            raise ValueError("Input workbook is empty")
        headers = list(raw[0])
        rows = [dict(zip(headers, values)) for values in raw[1:]]
    else:
        raise ValueError("Input must be CSV, XLSX, or XLSM")
    if any(h is None or not str(h).strip() for h in headers):
        raise ValueError("Empty column name")
    names = [str(h).strip() for h in headers]
    if len(set(names)) != len(names):
        raise ValueError("Duplicate column names")
    if "Expenses" not in names or "Month" not in names:
        raise ValueError("Required columns: Expenses and Month")
    accounts = [name for name in names if name not in ("Expenses", "Month")]
    if not accounts:
        raise ValueError("At least one expense account is required")
    clean = []
    for line_no, row in enumerate(rows, start=2):
        clean.append({str(key).strip(): value for key, value in row.items()})
    return clean, accounts


def validate_and_pair(rows, accounts):
    """Return sorted account-month pairs; reject rather than silently aggregate."""
    seen = {}
    months = set()
    for line_no, row in enumerate(rows, start=2):
        scenario = str(row.get("Expenses") or "").strip().casefold()
        month = str(row.get("Month") or "").strip()
        if scenario not in ("budget", "actual"):
            raise ValueError(f"Row {line_no}: unexpected scenario {scenario!r}")
        if not month:
            raise ValueError(f"Row {line_no}: missing month")
        key = (month, scenario)
        if key in seen:
            raise ValueError(f"Row {line_no}: duplicate month/scenario {key}")
        values = {}
        for account in accounts:
            original = row.get(account)
            if original is None or isinstance(original, str) and not original.strip():
                raise ValueError(f"Row {line_no}: missing amount for {account}")
            try:
                amount = float(original)
            except (TypeError, ValueError) as exc:
                raise ValueError(f"Row {line_no}: invalid amount for {account}") from exc
            if not math.isfinite(amount) or amount < 0:
                raise ValueError(f"Row {line_no}: expense amounts must be finite and nonnegative")
            values[account] = amount
        seen[key] = values
        months.add(month)
    if not seen:
        raise ValueError("No observations")
    detail = []
    for month in sorted(months):
        if (month, "budget") not in seen or (month, "actual") not in seen:
            raise ValueError(f"Month {month}: missing budget or actual scenario")
        for account in accounts:
            budget = seen[(month, "budget")][account]
            actual = seen[(month, "actual")][account]
            difference = actual - budget
            pct = difference / budget if budget else None
            detail.append(dict(month=month, account=account, budget=budget,
                               actual=actual, variance=difference, variance_pct=pct,
                               variance_type=("Unfavorable" if difference > 0 else
                                              "Favorable" if difference < 0 else "On budget"),
                               material_variance=(abs(pct) >= THRESHOLD if pct is not None
                                                  else actual != 0),
                               zero_budget=(budget == 0)))
    return detail


def summarize(detail, field):
    groups = defaultdict(list)
    for row in detail:
        groups[row[field]].append(row)
    return [dict(**{field: name},
                 budget=sum(r["budget"] for r in group),
                 actual=sum(r["actual"] for r in group),
                 variance=sum(r["variance"] for r in group),
                 variance_pct=(sum(r["variance"] for r in group) /
                               sum(r["budget"] for r in group)
                               if sum(r["budget"] for r in group) else None))
            for name, group in sorted(groups.items())]


def calculate_kpis(detail):
    """Budget adherence is NOT forecast accuracy. No forecasts or horizons are supplied."""
    if not detail:
        raise ValueError("No validated detail records")
    budget = sum(r["budget"] for r in detail)
    actual = sum(r["actual"] for r in detail)
    if budget <= 0:
        raise ValueError("Total budget must be positive for percentage KPIs")
    variance = actual - budget
    gross_error = sum(abs(r["variance"]) for r in detail)
    monthly = summarize(detail, "month")
    valid_months = [r for r in monthly if r["variance_pct"] is not None]
    monthly_mae = (sum(abs(r["variance_pct"]) for r in valid_months) /
                   len(valid_months)) if valid_months else None
    largest = max(valid_months, key=lambda r: abs(r["variance_pct"])) if valid_months else None
    material = sum(r["material_variance"] for r in detail)
    zero = sum(r["zero_budget"] for r in detail)
    return {
        "total_budget": budget, "total_actual": actual,
        "net_variance": variance, "net_variance_pct": variance / budget,
        "aggregate_budget_adherence": 1 - abs(variance) / budget,
        "gross_absolute_variance": gross_error,
        "weighted_absolute_budget_error": gross_error / budget,
        "unfavorable_variance_exposure": sum(max(r["variance"], 0) for r in detail) / budget,
        "material_variance_count": material,
        "material_variance_rate": material / len(detail),
        "zero_budget_line_count": zero,
        "average_monthly_absolute_net_variance_pct": monthly_mae,
        "largest_monthly_net_variance": largest["variance_pct"] if largest else None,
        "largest_month": largest["month"] if largest else "",
        "forecast_accuracy": None,
    }


DEFINITIONS = {
    "total_budget": "Sum of validated expense budgets.",
    "total_actual": "Sum of validated actual expenses.",
    "net_variance": "Actual minus budget; positive means unfavorable for expenses.",
    "net_variance_pct": "Net variance divided by total budget.",
    "aggregate_budget_adherence": "1 - abs(net variance) / total budget; offsets can conceal errors; not forecast accuracy.",
    "gross_absolute_variance": "Sum of absolute account-month dollar differences, before offsetting.",
    "weighted_absolute_budget_error": "Sum of absolute account-month differences / total budget; analogous to WAPE on budget, not independently measured forecasts.",
    "unfavorable_variance_exposure": "Sum of positive account-month variances / total budget.",
    "material_variance_count": "Number of account-month lines with abs(variance/budget) >= 10%; any nonzero actual on zero budget is material.",
    "material_variance_rate": "Material account-month lines divided by all account-month lines.",
    "zero_budget_line_count": "Number of account-month pairs with zero budget, including zero actual.",
    "average_monthly_absolute_net_variance_pct": "Unweighted mean of abs(monthly NET variance / monthly budget), omitting zero-budget months.",
    "largest_monthly_net_variance": "Signed monthly NET variance ratio with largest absolute value among nonzero-budget months.",
    "largest_month": "Month corresponding to largest monthly net variance ratio.",
    "forecast_accuracy": "Not available: forecast vintages, prediction horizons, and forecast-versus-realized observations are absent.",
}


def write_csv(path, rows, columns):
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def render_summary(kpis):
    def fmt(value):
        return "Not available" if value is None else f"{value:,.2f}"
    return ("# Executive Summary (generated from validated input)\n\n"
            f"Total budget: {fmt(kpis['total_budget'])}; total actual: {fmt(kpis['total_actual'])}.\n\n"
            f"Expense net variance (actual - budget): {fmt(kpis['net_variance'])} "
            f"({kpis['net_variance_pct']:.1%}).\n\n"
            f"Aggregate budget adherence: {kpis['aggregate_budget_adherence']:.1%}; "
            f"gross absolute budget error: {kpis['weighted_absolute_budget_error']:.1%}. "
            "The former is sensitive to offsetting errors. Neither is a verified rolling-forecast "
            "accuracy measure.\n\n"
            f"Material account-month pairs: {kpis['material_variance_count']} "
            f"({kpis['material_variance_rate']:.1%}), using a 10% line threshold. "
            f"Zero-budget pairs: {kpis['zero_budget_line_count']}.\n\n"
            "Forecast accuracy: unavailable without time-stamped forecasts and evaluation horizons.\n")


def run(input_path, output_dir):
    rows, accounts = read_source(input_path)
    detail = validate_and_pair(rows, accounts)
    monthly = summarize(detail, "month")
    account = summarize(detail, "account")
    kpis = calculate_kpis(detail)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(output_dir / "budget_actual_detail.csv", detail, list(detail[0]))
    write_csv(output_dir / "monthly_variance_summary.csv", monthly, list(monthly[0]))
    write_csv(output_dir / "account_variance_summary.csv", account, list(account[0]))
    write_csv(output_dir / "kpi_scorecard.csv",
              [dict(kpi=key, value=value, definition=DEFINITIONS[key])
               for key, value in kpis.items()],
              ["kpi", "value", "definition"])
    (output_dir / "kpi_scorecard.md").write_text(
        "# Generated KPI scorecard\n\n| KPI | Value | Definition |\n|---|---:|---|\n" +
        "".join(f"| {key} | {value if value is not None else 'N/A'} | {DEFINITIONS[key]} |\n"
                for key, value in kpis.items()), encoding="utf-8")
    (output_dir / "executive_summary.md").write_text(render_summary(kpis), encoding="utf-8")
    return kpis


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="Explicit source workbook or CSV")
    parser.add_argument("--output", type=Path, default=ROOT / "outputs" / "generated",
                        help="Separate generated outputs from historical published artifacts")
    args = parser.parse_args()
    run(args.input, args.output)
    print(f"Generated six validated report files in {args.output}")


if __name__ == "__main__":
    main()
