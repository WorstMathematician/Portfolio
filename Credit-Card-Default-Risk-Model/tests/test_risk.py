import importlib.util
import json
from pathlib import Path

import pytest

pytest.importorskip('pandas')
pytest.importorskip('sklearn')

MODULE = Path(__file__).resolve().parents[1] / 'src' / 'risk_model.py'
spec = importlib.util.spec_from_file_location('risk_model', MODULE)
risk = importlib.util.module_from_spec(spec)
spec.loader.exec_module(risk)


def test_validation_rejects_duplicates_and_targets():
    df = risk.synthetic_sample(400, seed=3)
    assert len(risk.validate(df)) == 400
    df.loc[1, 'ID'] = 1
    with pytest.raises(ValueError, match='duplicate ID'):
        risk.validate(df)
    df = risk.synthetic_sample(400, seed=3)
    df.loc[0, risk.TARGET] = 3
    with pytest.raises(ValueError, match='Target'):
        risk.validate(df)


def test_feature_leakage_guard():
    assert risk.TARGET not in risk.FEATURES
    assert 'ID' not in risk.FEATURES
    assert not set(risk.SENSITIVE).intersection(risk.FEATURES)


def test_policy_threshold_monotone_and_reject_all():
    y = [1, 0, 1, 0]
    scores = [0.9, 0.1, 0.6, 0.3]
    rows = risk.policy_rows(y, scores, cutoffs=[0, 0.25, 0.5, 1])
    assert [r['approved_accounts'] for r in rows] == [0, 1, 2, 4]
    assert rows[0]['hypothetical_total_payoff'] == 0
    assert rows[2]['hypothetical_total_payoff'] == 240
    assert rows[3]['hypothetical_total_payoff'] == -760


def test_full_pipeline_synthetic_and_held_out(tmp_path):
    result = risk.run(risk.synthetic_sample(800, seed=77), tmp_path,
                      source='synthetic_demo')
    assert result['train_rows'] == 480
    assert result['validation_rows'] == 160
    assert result['test_rows'] == 160
    assert 0 <= result['held_out_test']['roc_auc'] <= 1
    assert 0 <= result['held_out_test']['brier_score'] <= 1
    assert set(risk.SENSITIVE).issubset(set(result['excluded_features']))
    assert (tmp_path / 'validation_policy_grid.csv').exists()
    assert json.loads((tmp_path / 'metrics.json').read_text())['data_source'] == 'synthetic_demo'
