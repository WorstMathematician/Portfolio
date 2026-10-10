from pathlib import Path
import pandas as pd
import pytest
from src.program_panel import load_panel, quarterly_panel, panel_diagnostics

PROJECT = Path(__file__).resolve().parents[1]
DATA = PROJECT/'data'/'ongoing_program_agency_2023_2025.csv'
TOTALS = PROJECT/'data'/'annual_quarterly_totals.csv'

def test_reconciles_countywide_for_both_years():
    panel,report=load_panel(DATA,TOTALS)
    assert len(panel)==73
    assert report.agency_program_rows.tolist()==[32,41]
    assert report.reported_ytd_usd.tolist()==['400492675.72','538421310']

def test_real_panel_shape_and_coverage():
    panel,_=load_panel(DATA,TOTALS)
    long=quarterly_panel(panel)
    assert len(long)==292
    summary=panel_diagnostics(panel)
    assert summary['observed_quarterly_periods']==8
    assert summary['model_promotion_gate'].startswith('blocked')
    assert summary['pairs_present_both_years']>0

def test_duplicate_rejected(tmp_path):
    raw=pd.read_csv(DATA,dtype=str)
    path=tmp_path/'duplicate.csv'
    pd.concat([raw,raw.iloc[[0]]]).to_csv(path,index=False)
    with pytest.raises(ValueError,match='Duplicate'):
        load_panel(path,TOTALS)

def test_changed_program_amount_fails(tmp_path):
    raw=pd.read_csv(DATA,dtype=str)
    raw.loc[0,'q1_usd']='999999999'
    path=tmp_path/'tampered.csv'
    raw.to_csv(path,index=False)
    with pytest.raises(ValueError,match='quarterly-to-YTD'):
        load_panel(path,TOTALS)

def test_reported_ytd_mutation_fails_totals(tmp_path):
    raw=pd.read_csv(DATA,dtype=str)
    raw.loc[0,'q1_usd']=str(float(raw.loc[0,'q1_usd'])+2)
    raw.loc[0,'reported_ytd_usd']=str(float(raw.loc[0,'reported_ytd_usd'])+2)
    path=tmp_path/'tampered.csv'
    raw.to_csv(path,index=False)
    with pytest.raises(ValueError,match='aggregate'):
        load_panel(path,TOTALS)

def test_invalid_source_year_rejected(tmp_path):
    raw=pd.read_csv(DATA,dtype=str)
    raw.loc[0,'source_url']=raw.loc[34,'source_url']
    path=tmp_path/'bad_source.csv'
    raw.to_csv(path,index=False)
    with pytest.raises(ValueError,match='Source URL'):
        load_panel(path,TOTALS)