"""Audit public LA County Measure H ongoing program/agency quarter-level reports.

Usage: python -m src.program_panel --input data/ongoing_program_agency_2023_2025.csv

No forecasts are fit by this module. Program-year records are manually transcribed
from the two official report tables and independently reconciled to published
countywide quarterly and annual totals.
"""
from __future__ import annotations

import argparse
import json
from decimal import Decimal, InvalidOperation
from pathlib import Path

import pandas as pd

NUMERIC = ('allocation_usd','q1_usd','q2_usd','q3_usd','q4_usd','reported_ytd_usd')
QUARTERLY = ('q1_usd','q2_usd','q3_usd','q4_usd')
REQUIRED = ('fiscal_year','funding_scope','program','agency','source_url','source_page',*NUMERIC)
TOLERANCE = Decimal('1.00')


def parse_money(value: str, field: str, line: int) -> Decimal:
    if not isinstance(value,str) or not value.strip():
        raise ValueError(f'Blank amount: {field}, row {line}')
    try:
        amount = Decimal(value.strip().replace(',',''))
    except InvalidOperation as exc:
        raise ValueError(f'Invalid amount: {field}, row {line}') from exc
    if not amount.is_finite():
        raise ValueError(f'Nonfinite amount: {field}, row {line}')
    return amount


def load_panel(path: str | Path, published_totals: str | Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    raw = pd.read_csv(path,dtype=str,keep_default_na=False)
    if raw.empty:
        raise ValueError('No panel observations')
    missing=set(REQUIRED)-set(raw.columns)
    if missing:
        raise ValueError(f'Missing required columns: {sorted(missing)}')
    if not raw['funding_scope'].eq('ongoing').all():
        raise ValueError('Panel must be ongoing Measure H expenditure only')
    if not raw.fiscal_year.isin(['2023-24','2024-25']).all():
        raise ValueError('Unexpected fiscal year in reviewed source set')
    if raw.duplicated(['fiscal_year','program','agency']).any():
        raise ValueError('Duplicate fiscal year / program / agency')
    for field in ('program','agency','source_url','source_page'):
        if raw[field].str.strip().eq('').any():
            raise ValueError(f'Blank {field}')
    if not raw.source_url.str.startswith('https://').all():
        raise ValueError('Source URL missing HTTPS')
    expected_urls = {
        '2023-24':'https://file.lacounty.gov/SDSInter/lac/1187357_MeasureHExpenditureLog-FY23-24-COAB.pdf',
        '2024-25':'https://file.lacounty.gov/SDSInter/lac/1195430_MeasureHExpenditureLog-FY24-25-COAB.pdf'
    }
    if any(row.source_url != expected_urls[row.fiscal_year] for row in raw.itertuples()):
        raise ValueError('Source URL and reporting year mismatch')
    if not raw.source_page.isin(['1','2']).all():
        raise ValueError('Invalid source page for ongoing-spending section')
    checked=[]
    year_totals={}
    for i,row in raw.iterrows():
        values={field:parse_money(row[field],field,i+2) for field in NUMERIC}
        if values['allocation_usd'] < 0:
            raise ValueError('Negative allocation')
        delta=sum((values[c] for c in QUARTERLY),Decimal('0'))-values['reported_ytd_usd']
        if abs(delta)>TOLERANCE:
            raise ValueError(f'Row {i+2} fails quarterly-to-YTD reconciliation by {delta} USD')
        checked.append({'fiscal_year':row.fiscal_year,'program':row.program,'agency':row.agency,'row_difference_usd':str(delta)})
        dest=year_totals.setdefault(row.fiscal_year,{key:Decimal('0') for key in NUMERIC})
        for key,amount in values.items():
            dest[key]+=amount
    official=pd.read_csv(published_totals,dtype=str,keep_default_na=False)
    report=[]
    for year, sums in sorted(year_totals.items()):
        matches=official.loc[official.fiscal_year.eq(year)&official.scope.eq('ongoing')]
        if len(matches)!=1:
            raise ValueError('Missing or ambiguous published fiscal-year benchmark')
        benchmark=matches.iloc[0]
        differences={}
        for column in NUMERIC:
            published_col='reported_ytd_usd' if column=='reported_ytd_usd' else column
            if column=='allocation_usd':
                published_col='allocation_usd'
            difference=sums[column]-parse_money(benchmark[published_col],published_col,0)
            differences[column]=str(difference)
            if abs(difference)>TOLERANCE:
                raise ValueError(f'{year}: aggregate {column} mismatch by {difference} USD')
        report.append({'fiscal_year':year,'agency_program_rows':int(raw.fiscal_year.eq(year).sum()),
                       'allocation_usd':str(sums['allocation_usd']),
                       'reported_ytd_usd':str(sums['reported_ytd_usd']),
                       'differences_vs_official_usd':differences,
                       'max_abs_record_reconciliation_usd':str(max(abs(Decimal(x['row_difference_usd'])) for x in checked if x['fiscal_year']==year))})
    output=raw.copy()
    for column in NUMERIC:
        output[column]=pd.to_numeric(output[column],errors='raise')
    audit=pd.DataFrame(checked)
    return output,pd.DataFrame(report)


def quarterly_panel(panel: pd.DataFrame) -> pd.DataFrame:
    long=panel.melt(id_vars=['fiscal_year','program','agency','funding_scope','allocation_usd','source_url','source_page'],
                    value_vars=list(QUARTERLY),var_name='quarter_label',value_name='expenditure_usd')
    long['quarter']=long.quarter_label.str[1].astype(int)
    long['fiscal_start']=long.fiscal_year.str[:4].astype(int)
    long['period_index']=long.fiscal_start*4+long.quarter-1
    long=long.drop(columns=['quarter_label']).sort_values(['period_index','program','agency']).reset_index(drop=True)
    return long


def panel_diagnostics(panel:pd.DataFrame) -> dict:
    keys=panel.groupby(['program','agency'])['fiscal_year'].nunique()
    return {'program_agency_year_rows':len(panel),
            'quarterly_observations':len(panel)*4,
            'distinct_programs':int(panel.program.nunique()),
            'distinct_agencies':int(panel.agency.nunique()),
            'program_agency_pairs':int(keys.size),
            'pairs_present_both_years':int(keys.eq(2).sum()),
            'pairs_present_once':int(keys.eq(1).sum()),
            'observed_quarterly_periods':8,
            'model_promotion_gate':'blocked_insufficient_historical_quarters',
            'comment':'Program-panel cross-sectional size does not create more independent fiscal quarters.'}


def run(panel_path: str|Path, totals_path: str|Path, out_dir:str|Path) -> dict:
    panel,verification=load_panel(panel_path,totals_path)
    out_dir=Path(out_dir);out_dir.mkdir(parents=True,exist_ok=True)
    quarterly_panel(panel).to_csv(out_dir/'ongoing_quarterly_program_panel.csv',index=False)
    verification.to_json(out_dir/'program_panel_reconciliation.json',orient='records',indent=2)
    status=panel_diagnostics(panel)
    (out_dir/'program_panel_readiness.json').write_text(json.dumps(status,indent=2)+'\n',encoding='utf-8')
    return {'readiness':status,'reconciliation':verification.to_dict(orient='records')}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input',default='data/ongoing_program_agency_2023_2025.csv')
    p.add_argument('--totals',default='data/annual_quarterly_totals.csv')
    p.add_argument('--output',default='outputs')
    args=p.parse_args()
    print(json.dumps(run(args.input,args.totals,args.output),indent=2))