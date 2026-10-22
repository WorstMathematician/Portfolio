from pathlib import Path
from src.models import evaluate_eligibility, MODEL_GRID
from src.pipeline import load_and_validate, long_form
SOURCE=Path(__file__).parents[1]/'data'/'annual_quarterly_totals.csv'
def test_no_model_promoted_with_noncomparable_scopes():
    annual,_=load_and_validate(SOURCE)
    eligibility=evaluate_eligibility(long_form(annual))
    assert eligibility['status']=='blocked'
    assert all(m['eligibility']=='blocked_insufficient_history' for m in eligibility['models'])
    assert 'seasonal_naive' in MODEL_GRID
