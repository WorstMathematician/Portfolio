"""Auditable public-finance diagnostics. Historical actuals are NOT live forecasts.

Run: python -m src.pipeline --input data/annual_quarterly_totals.csv --output outputs
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from decimal import Decimal, InvalidOperation
import numpy as np
import pandas as pd

MONEY = ('allocation_usd', 'q1_usd', 'q2_usd', 'q3_usd', 'q4_usd', 'reported_ytd_usd')
QUARTERS = ('q1_usd', 'q2_usd', 'q3_usd', 'q4_usd')
SCOPE_LABELS = ('comprehensive', 'unclassified', 'ongoing')
MIN_COMPARABLE_QUARTERS = 24


def load_and_validate(path: str | Path, tolerance_usd: Decimal = Decimal('1.00')) -> tuple[pd.DataFrame, list[dict]]:
    """Exact Decimal reconciliation before floating-point analysis."""
    raw = pd.read_csv(path, dtype=str, keep_default_na=False)
    expected = {'fiscal_year', 'scope', 'source_url', 'verification_note', *MONEY}
    if not expected.issubset(raw.columns):
        raise ValueError(f'Missing columns: {sorted(expected-set(raw.columns))}')
    if raw['fiscal_year'].duplicated().any():
        raise ValueError('Duplicate fiscal-year record')
    if not raw['fiscal_year'].str.fullmatch(r'\d{4}-\d{2}').all():
        raise ValueError('Invalid fiscal year')
    years = raw['fiscal_year'].str[:4].astype(int)
    if not years.is_monotonic_increasing or years.duplicated().any():
        raise ValueError('Fiscal years must be strictly increasing')
    if not raw['scope'].isin(SCOPE_LABELS).all():
        raise ValueError('Invalid scope classification')
    if not raw['source_url'].str.startswith('https://').all():
        raise ValueError('Every record requires an HTTPS provenance link')
    problems = []
    out = raw.copy()
    for idx, row in raw.iterrows():
        values = {}
        for col in MONEY:
            try:
                if not row[col].strip():
                    raise ValueError(f'Blank financial value in {row["fiscal_year"]}: {col}')
                value = Decimal(row[col].replace(',', ''))
            except InvalidOperation as exc:
                raise ValueError(f'Invalid money in {row["fiscal_year"]}: {col}') from exc
            if not value.is_finite():
                raise ValueError('Nonfinite financial value')
            values[col] = value
            out.at[idx, col] = float(value)
        difference = sum(values[c] for c in QUARTERS) - values['reported_ytd_usd']
        status = 'pass' if abs(difference) <= tolerance_usd else 'fail'
        problems.append({'fiscal_year': row['fiscal_year'], 'scope': row['scope'],
                         'difference_usd': float(difference), 'status': status,
                         'source_url': row['source_url']})
    if any(p['status'] == 'fail' for p in problems):
        raise ValueError(f'Quarterly/YTD reconciliation failed: {problems}')
    return out, problems


def long_form(annual: pd.DataFrame) -> pd.DataFrame:
    frame = annual.melt(id_vars=['fiscal_year', 'scope', 'source_url', 'verification_note'],
                        value_vars=list(QUARTERS), var_name='quarter_column', value_name='expenditure_usd')
    frame['quarter'] = frame['quarter_column'].str[1].astype(int)
    frame['fiscal_start'] = frame['fiscal_year'].str[:4].astype(int)
    frame = frame.sort_values(['fiscal_start', 'quarter']).reset_index(drop=True)
    frame['period_index'] = 4 * (frame['fiscal_start'] - frame['fiscal_start'].min()) + frame['quarter'] - 1
    return frame.drop(columns='quarter_column')


def contiguous_scope_segments(frame: pd.DataFrame) -> pd.DataFrame:
    """Runs split on BOTH scope and missing years. Do not fabricate continuity."""
    rows = []
    for scope, group in frame.groupby('scope'):
        group = group.sort_values('period_index')
        segments = (group['period_index'].diff().fillna(1).ne(1)).cumsum()
        for _, part in group.groupby(segments):
            rows.append({'scope': scope, 'start': f"{part.iloc[0]['fiscal_year']} Q{part.iloc[0]['quarter']}",
                         'end': f"{part.iloc[-1]['fiscal_year']} Q{part.iloc[-1]['quarter']}",
                         'quarters': len(part), 'meets_24_quarter_gate': len(part) >= MIN_COMPARABLE_QUARTERS})
    return pd.DataFrame(rows).sort_values(['start','scope']).reset_index(drop=True)


def diagnostics(frame: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Flags are investigation prompts, never deletion instructions."""
    annual = frame.groupby(['fiscal_year','scope'], sort=True).agg(
        observed_usd=('expenditure_usd','sum'), quarters=('quarter','nunique')).reset_index()
    annual['q4_share'] = frame.loc[frame.quarter.eq(4)].set_index('fiscal_year').loc[annual.fiscal_year, 'expenditure_usd'].to_numpy() / annual['observed_usd'].to_numpy()
    annual['year_over_year_change'] = np.nan
    for i in range(1, len(annual)):
        if annual.loc[i, 'scope'] == annual.loc[i-1, 'scope'] and annual.loc[i-1,'observed_usd'] != 0:
            annual.loc[i,'year_over_year_change'] = annual.loc[i,'observed_usd'] / annual.loc[i-1,'observed_usd'] - 1
    results=[]
    for scope, group in frame.groupby('scope'):
        group = group.sort_values('period_index')
        for _, row in group.iterrows():
            # Compare with same quarter only, and require >=3 OTHER reference years.
            others=group.loc[(group['quarter']==row['quarter']) & (group['fiscal_year']!=row['fiscal_year']), 'expenditure_usd'].astype(float)
            med=float(others.median()) if len(others) else np.nan
            mad=float(np.median(np.abs(others-med))) if len(others) else np.nan
            robust_z=0.6745*(float(row['expenditure_usd'])-med)/mad if len(others)>=3 and mad>0 else np.nan
            results.append({'fiscal_year':row['fiscal_year'],'quarter':int(row['quarter']), 'scope':scope,
                            'expenditure_usd':row['expenditure_usd'], 'reference_n':len(others),
                            'robust_z':robust_z, 'statistical_flag': bool(np.isfinite(robust_z) and abs(robust_z)>3.5),
                            'classification':'investigation_only' if np.isfinite(robust_z) and abs(robust_z)>3.5 else 'not_flagged_or_insufficient_history'})
    return annual, pd.DataFrame(results).sort_values(['fiscal_year','quarter']).reset_index(drop=True)


def run(path: str|Path, outdir: str|Path) -> dict:
    annual,reconciliation=load_and_validate(path)
    frame=long_form(annual)
    segments=contiguous_scope_segments(frame)
    summary,anomalies=diagnostics(frame)
    outdir=Path(outdir)
    outdir.mkdir(parents=True,exist_ok=True)
    for name, dataframe in [('quarterly_observations',frame),('annual_diagnostics',summary),('anomaly_review',anomalies),('eligibility',segments),('reconciliation',pd.DataFrame(reconciliation))]:
        dataframe.to_csv(outdir/f'{name}.csv',index=False)
    eligible=bool(segments['meets_24_quarter_gate'].any())
    report={'source':'LA County Measure H published expenditure reports',
            'annual_source_reports':int(len(annual)), 'quarterly_observations':int(len(frame)),
            'reconciliation_max_abs_usd':max(abs(p['difference_usd']) for p in reconciliation),
            'min_comparable_quarters':MIN_COMPARABLE_QUARTERS,
            'eligible_for_confirmatory_model_comparison':eligible,
            'status':'GATE_PASSED' if eligible else 'BLOCKED_INSUFFICIENT_COMPARABLE_HISTORY',
            'warning':'Historic reporting scopes differ. No production forecasts or validated performance metrics are claimed.'}
    (outdir/'readiness.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    return report


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input',default='data/annual_quarterly_totals.csv')
    parser.add_argument('--output',default='outputs')
    args=parser.parse_args()
    print(json.dumps(run(args.input,args.output),indent=2))
