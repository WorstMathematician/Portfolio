from pathlib import Path
import pandas as pd
import pytest
from src.pipeline import load_and_validate, long_form, contiguous_scope_segments, diagnostics, run

SOURCE=Path(__file__).parents[1]/'data'/'annual_quarterly_totals.csv'

def test_real_source_totals_reconcile():
    annual,reconciliation=load_and_validate(SOURCE)
    assert len(annual)==8
    assert all(x['status']=='pass' for x in reconciliation)
    assert max(abs(x['difference_usd']) for x in reconciliation)==1

def test_source_scope_gate_blocks_invalid_claims():
    annual,_=load_and_validate(SOURCE)
    series=long_form(annual)
    segments=contiguous_scope_segments(series)
    assert len(series)==32
    assert not segments['meets_24_quarter_gate'].any()
    assert segments.loc[segments.scope.eq('ongoing'),'quarters'].max()==12

def test_missing_or_bad_amount_fails(tmp_path):
    df=pd.read_csv(SOURCE, dtype=str)
    df.loc[0,'q1_usd']=''
    path=tmp_path/'broken.csv'
    df.to_csv(path,index=False)
    with pytest.raises(ValueError,match='Blank financial'):
        load_and_validate(path)

def test_difference_over_tolerance_fails(tmp_path):
    df=pd.read_csv(SOURCE, dtype=str)
    df.loc[0,'q1_usd']='999999999'
    path=tmp_path/'broken.csv'
    df.to_csv(path,index=False)
    with pytest.raises(ValueError,match='reconciliation failed'):
        load_and_validate(path)

def test_diagnostics_does_not_delete_observations():
    annual,_=load_and_validate(SOURCE)
    frame=long_form(annual)
    _,anomalies=diagnostics(frame)
    assert len(anomalies)==len(frame)
    assert anomalies.loc[anomalies.scope.eq('ongoing'),'reference_n'].max()==2

def test_export_summary(tmp_path):
    status=run(SOURCE,tmp_path)
    assert not status['eligible_for_confirmatory_model_comparison']
    assert (tmp_path/'readiness.json').exists()
    assert (tmp_path/'reconciliation.csv').exists()
