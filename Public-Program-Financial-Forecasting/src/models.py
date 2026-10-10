"""Candidate model registry; not fitted results."""
from __future__ import annotations
from .pipeline import MIN_COMPARABLE_QUARTERS, contiguous_scope_segments

MODEL_GRID = {
    'seasonal_naive': {'lag': [4]},
    'lag1_naive': {'lag': [1]},
    'ridge_regression': {'alpha': [0.1, 1, 10, 100], 'lags': [[1, 4]]},
    'ets': {'trend': [None, 'add', 'damped'], 'seasonal': [None, 'add'], 'period': [4]},
    'sarima': {'p': [0, 1], 'd': [0, 1], 'q': [0, 1], 'P': [0, 1], 'D': [0, 1], 'Q': [0, 1], 'm': [4]},
    'gradient_boosting': {'learning_rate': [0.03, 0.1], 'max_leaf_nodes': [3, 5, 7], 'min_samples_leaf': [10, 20, 40]},
}
def evaluate_eligibility(quarterly):
    segments = contiguous_scope_segments(quarterly)
    max_n = int(segments['quarters'].max()) if len(segments) else 0
    eligible = max_n >= MIN_COMPARABLE_QUARTERS
    return {
        'status': 'eligible_for_candidate_backtesting' if eligible else 'blocked',
        'maximum_contiguous_comparable_quarters': max_n,
        'required_quarters': MIN_COMPARABLE_QUARTERS,
        'models': [{'model': name,
                    'eligibility': 'candidate_only_requires_backtests' if eligible and name in ('seasonal_naive','lag1_naive','ridge_regression','ets') else
                                   ('needs_panel_sufficiency_review' if eligible else 'blocked_insufficient_history'),
                    'candidate_grid': grid} for name, grid in MODEL_GRID.items()],
        'reasons': ['Use consistent historical definitions', 'Never train on future values', 'Require holdout backtests before promotion']
    }
