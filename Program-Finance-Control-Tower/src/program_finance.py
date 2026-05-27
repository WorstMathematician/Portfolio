from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'data' / 'raw'
OUT = ROOT / 'outputs'


def find_file():
    files = sorted(list(RAW.glob('*.csv')) + list(RAW.glob('*.xlsx')) + list(RAW.glob('*.xls')))
    if not files:
        raise FileNotFoundError('Place the Kaggle dataset in data/raw before running this script.')
    return files[0]


def clean_columns(df):
    df = df.copy()
    df.columns = [str(c).strip().lower().replace(' ', '_') for c in df.columns]
    return df


def pick(df, candidates):
    for c in candidates:
        if c in df.columns:
            return c
    for col in df.columns:
        for c in candidates:
            if c in col:
                return col
    return None


def main():
    path = find_file()
    df = pd.read_csv(path) if path.suffix.lower() == '.csv' else pd.read_excel(path)
    df = clean_columns(df)

    program_col = pick(df, ['dept_id', 'program_id', 'project_id', 'department'])
    period_col = pick(df, ['time_index', 'period', 'month'])
    budget_col = pick(df, ['budget_allocated', 'budget', 'planned_cost'])
    actual_col = pick(df, ['budget_consumed', 'actual_cost', 'spend', 'cost'])
    risk_col = pick(df, ['risk_score', 'risk'])

    if not all([program_col, period_col, budget_col, actual_col]):
        raise ValueError('Missing required fields for program finance analysis.')

    work = pd.DataFrame({
        'program_id': df[program_col].astype(str),
        'period_index': pd.to_numeric(df[period_col], errors='coerce'),
        'period_budget': pd.to_numeric(df[budget_col], errors='coerce'),
        'period_actual': pd.to_numeric(df[actual_col], errors='coerce'),
        'risk_score': pd.to_numeric(df[risk_col], errors='coerce') if risk_col else 0,
    }).dropna(subset=['program_id', 'period_budget', 'period_actual'])

    work = work[work['period_budget'] > 0].sort_values(['program_id', 'period_index'])
    grouped = work.groupby('program_id', group_keys=False)
    work['budget_at_completion'] = grouped['period_budget'].transform('sum')
    work['actual_cost_to_date'] = grouped['period_actual'].cumsum()
    work['planned_cost_to_date'] = grouped['period_budget'].cumsum()
    work['earned_value'] = work['planned_cost_to_date']
    work['elapsed_periods'] = grouped.cumcount() + 1
    work['total_periods'] = grouped['period_index'].transform('count')
    work['remaining_periods'] = (work['total_periods'] - work['elapsed_periods']).clip(lower=0)
    work['average_actual_burn'] = work['actual_cost_to_date'] / work['elapsed_periods']
    work['etc'] = work['average_actual_burn'] * work['remaining_periods']
    work['eac'] = work['actual_cost_to_date'] + work['etc']
    work['cpi'] = (work['earned_value'] / work['actual_cost_to_date']).replace([np.inf, -np.inf], np.nan).fillna(1)
    work['eac_variance'] = work['budget_at_completion'] - work['eac']
    work['eac_variance_pct'] = work['eac_variance'] / work['budget_at_completion']
    work['contract_value'] = work['budget_at_completion'] / 0.82
    work['margin_pct_at_completion'] = (work['contract_value'] - work['eac']) / work['contract_value']
    work['program_status'] = np.select(
        [(work['eac_variance_pct'] < -0.07) | (work['margin_pct_at_completion'] < 0.12) | (work['risk_score'] > 0.90),
         (work['eac_variance_pct'] < -0.03) | (work['margin_pct_at_completion'] < 0.18) | (work['risk_score'] > 0.75)],
        ['Red', 'Yellow'], default='Green')

    latest = work.groupby('program_id', as_index=False).tail(1)
    OUT.mkdir(parents=True, exist_ok=True)
    work.to_csv(OUT / 'program_finance_detail.csv', index=False)
    latest.to_csv(OUT / 'program_finance_snapshot.csv', index=False)
    print('Wrote program finance outputs to', OUT)


if __name__ == '__main__':
    main()
