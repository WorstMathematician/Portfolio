"""Validate original FY22–23 Measure H ongoing strategy-agency table.

The strategy code taxonomy is deliberately NOT mapped onto later program names.
"""
import csv
from decimal import Decimal
from pathlib import Path

SOURCE=Path(__file__).resolve().parents[1]/'data'/'ongoing_strategy_agency_2022_23.csv'
EXPECTED={
  'allocation_usd':Decimal('481983147.00'),
  'q1_usd':Decimal('57011832.85'),
  'q2_usd':Decimal('82219890.91'),
  'q3_usd':Decimal('103759294.36'),
  'q4_usd':Decimal('111313795.51'),
  'reported_ytd_usd':Decimal('354304813.63'),
}
FIELDS=tuple(EXPECTED)
def validate(path=SOURCE):
    with open(path, newline='', encoding='utf-8-sig') as f:
        rows=list(csv.DictReader(f))
    if len(rows)!=36:
        raise ValueError(f'Expected 36 report lines; received {len(rows)}')
    keys=set()
    totals={name:Decimal(0) for name in FIELDS}
    for i,row in enumerate(rows,1):
        if row['fiscal_year']!='2022-23' or row['funding_scope']!='ongoing':
            raise ValueError(f'Invalid FY or financial reporting scope at line {i}')
        key=(row['strategy_code'],row['agency'])
        if key in keys: raise ValueError(f'Duplicate strategy/agency pair: {key}')
        keys.add(key)
        values={name:Decimal(row[name]) for name in FIELDS}
        if any(not n.is_finite() for n in values.values()):
            raise ValueError(f'Invalid monetary value at line {i}')
        if abs(sum(values[n] for n in ('q1_usd','q2_usd','q3_usd','q4_usd'))-values['reported_ytd_usd'])>Decimal('0.01'):
            raise ValueError(f'Row quarterly reconciliation failed at line {i}')
        for name,value in values.items():totals[name]+=value
    if totals!=EXPECTED:
        raise ValueError(f'Published totals do not reconcile: {totals}')
    return {'rows':len(rows),'quarters':4,'quarterly_cells':4*len(rows),'totals':{k:str(v) for k,v in totals.items()},
            'model_comparable_to_newer_program_names':False}

if __name__=='__main__':
    import json
    print(json.dumps(validate(),indent=2))
