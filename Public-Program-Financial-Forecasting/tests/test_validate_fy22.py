from pathlib import Path
import csv
import pytest
from src.validate_fy22 import validate,SOURCE

def test_fy22_published_totals_exact():
    r=validate()
    assert r['rows']==36
    assert r['totals']['reported_ytd_usd']=='354304813.63'
    assert not r['model_comparable_to_newer_program_names']

def test_fy22_corruption_fails(tmp_path):
    with SOURCE.open(newline='',encoding='utf-8-sig') as fh:rows=list(csv.DictReader(fh))
    rows[0]['q1_usd']='999999'
    p=tmp_path/'corrupt.csv'
    with p.open('w',newline='',encoding='utf-8') as fh:
        w=csv.DictWriter(fh,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    with pytest.raises(ValueError,match='reconciliation'):validate(p)
