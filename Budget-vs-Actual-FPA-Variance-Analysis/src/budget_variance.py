from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'data' / 'raw'
OUT = ROOT / 'outputs'


def find_file():
    files = sorted(list(RAW.glob('*.xlsx')) + list(RAW.glob('*.xls')) + list(RAW.glob('*.csv')))
    if not files:
        raise FileNotFoundError('Place the Kaggle dataset in data/raw before running this script.')
    return files[0]


def main():
    path = find_file()
    df = pd.read_excel(path) if path.suffix.lower() in {'.xlsx', '.xls'} else pd.read_csv(path)
    df.columns = [str(c).strip() for c in df.columns]

    scenario_col = 'Expenses' if 'Expenses' in df.columns else df.columns[0]
    month_col = 'Month' if 'Month' in df.columns else df.columns[1]
    value_cols = [c for c in df.columns if c not in {scenario_col, month_col}]

    long = df.melt(id_vars=[scenario_col, month_col], value_vars=value_cols, var_name='account', value_name='amount')
    long['scenario'] = long[scenario_col].astype(str).str.strip().str.title()
    long['month'] = long[month_col]
    long['amount'] = pd.to_numeric(long['amount'], errors='coerce')

    pivot = long.pivot_table(index=['month', 'account'], columns='scenario', values='amount', aggfunc='sum').reset_index()
    for col in ['Budget', 'Actual']:
        if col not in pivot.columns:
            raise ValueError(f'Missing {col} scenario in dataset.')

    pivot['variance'] = pivot['Actual'] - pivot['Budget']
    pivot['variance_pct'] = np.where(pivot['Budget'] != 0, pivot['variance'] / pivot['Budget'], np.nan)
    pivot['variance_type'] = np.where(pivot['variance'] > 0, 'Unfavorable', 'Favorable')
    pivot['material_variance'] = pivot['variance_pct'].abs() >= 0.10

    monthly = pivot.groupby('month', as_index=False).agg(budget=('Budget', 'sum'), actual=('Actual', 'sum'), variance=('variance', 'sum'))
    monthly['variance_pct'] = monthly['variance'] / monthly['budget']

    account = pivot.groupby('account', as_index=False).agg(budget=('Budget', 'sum'), actual=('Actual', 'sum'), variance=('variance', 'sum'))
    account['variance_pct'] = account['variance'] / account['budget']

    OUT.mkdir(parents=True, exist_ok=True)
    pivot.to_csv(OUT / 'budget_actual_detail.csv', index=False)
    monthly.to_csv(OUT / 'monthly_variance_summary.csv', index=False)
    account.to_csv(OUT / 'account_variance_summary.csv', index=False)
    print('Wrote budget variance outputs to', OUT)


if __name__ == '__main__':
    main()
