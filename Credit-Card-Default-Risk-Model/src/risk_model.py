"""UCI credit-card next-month default: validated experimental risk pipeline.

UCI mode needs a user-downloaded original XLS. Synthetic mode is a DEMO ONLY.
Neither model is suitable for real consumer credit decisions.
"""
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (average_precision_score, brier_score_loss,
                             f1_score, precision_score, recall_score,
                             roc_auc_score)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[1]
TARGET = 'default payment next month'
SENSITIVE = ['SEX', 'EDUCATION', 'MARRIAGE', 'AGE']
FEATURES = ['LIMIT_BAL', 'PAY_0', 'PAY_2', 'PAY_3', 'PAY_4', 'PAY_5', 'PAY_6'] + [
    f'{prefix}{n}' for prefix in ('BILL_AMT', 'PAY_AMT') for n in range(1, 7)
]
REQUIRED = ['ID', TARGET] + FEATURES + SENSITIVE
PROFIT_PER_PERFORMING_ACCOUNT = 120.0  # Hypothetical units per approved account
LOSS_PER_DEFAULT_ACCOUNT = 500.0       # Hypothetical units per approved account


def synthetic_sample(n=6000, seed=20261018):
    """Fabricated feature/target process; NOT a substitute for UCI validation."""
    if n < 300:
        raise ValueError('demo sample must contain at least 300 rows')
    rng = np.random.default_rng(seed)
    limit = rng.choice([30000, 50000, 80000, 120000, 200000, 300000], size=n)
    latent = rng.normal(0, 1, n)
    payment_status = np.clip(np.rint(latent * 1.4 + rng.normal(0, 1, n)), -2, 7)
    values = {
        'ID': np.arange(1, n + 1, dtype=int),
        'LIMIT_BAL': limit,
        'SEX': rng.integers(1, 3, size=n),
        'EDUCATION': rng.integers(1, 5, size=n),
        'MARRIAGE': rng.integers(1, 4, size=n),
        'AGE': rng.integers(21, 70, size=n),
        'PAY_0': payment_status,
    }
    for k in range(2, 7):
        values[f'PAY_{k}'] = np.clip(np.rint(latent + rng.normal(0, 1.2, n)), -2, 8)
    for k in range(1, 7):
        bill = np.maximum(0, limit * rng.uniform(0.08, 0.86, n) + rng.normal(0, 6000, n))
        values[f'BILL_AMT{k}'] = np.rint(bill)
        values[f'PAY_AMT{k}'] = np.rint(np.maximum(0, bill * rng.uniform(0.02, 0.4, n)))
    logit = -1.95 + 0.81 * payment_status + 0.34 * latent + 0.13 * (limit <= 50000)
    probability = 1 / (1 + np.exp(-np.clip(logit, -20, 20)))
    values[TARGET] = rng.binomial(1, probability)
    return pd.DataFrame(values)


def load_uci_xls(path):
    """UCI original Excel has a descriptor row followed by the true header."""
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f'UCI XLS missing: {path}. See README for official source.')
    return pd.read_excel(path, sheet_name='Data', header=1, engine='xlrd')


def validate(df):
    if not isinstance(df, pd.DataFrame):
        raise TypeError('Expected a pandas DataFrame')
    if df.columns.duplicated().any():
        raise ValueError('Duplicate column names')
    missing = set(REQUIRED) - set(df.columns)
    if missing:
        raise ValueError(f'Missing expected UCI columns: {sorted(missing)}')
    if df.empty or df['ID'].isna().any() or df['ID'].duplicated().any():
        raise ValueError('Empty dataset, null ID or duplicate ID')
    target = pd.to_numeric(df[TARGET], errors='coerce')
    if target.isna().any() or not set(target.unique()) <= {0, 1}:
        raise ValueError('Target must contain only 0/1 without missing values')
    if target.nunique() != 2:
        raise ValueError('Need both classes for stratified validation')
    clean = df.copy()
    for name in FEATURES:
        clean[name] = pd.to_numeric(df[name], errors='coerce')
    if clean[FEATURES].isna().all(axis=None):
        raise ValueError('No usable feature values')
    if (clean['LIMIT_BAL'].dropna() <= 0).any():
        raise ValueError('Invalid nonpositive credit limit')
    clean[TARGET] = target.astype(int)
    return clean


def metric_bundle(y, probability, classification_cutoff=0.5):
    predicted = (np.asarray(probability) >= classification_cutoff).astype(int)
    return {
        'roc_auc': float(roc_auc_score(y, probability)),
        'average_precision': float(average_precision_score(y, probability)),
        'brier_score': float(brier_score_loss(y, probability)),
        'precision_at_0_5': float(precision_score(y, predicted, zero_division=0)),
        'recall_at_0_5': float(recall_score(y, predicted, zero_division=0)),
        'f1_at_0_5': float(f1_score(y, predicted, zero_division=0)),
        'positive_rate': float(np.mean(y)),
        'n': int(len(y)),
    }


def policy_rows(y, scores, cutoffs=None):
    """Retrospective what-if ONLY: cardholder defaults are not applicant counterfactuals."""
    if cutoffs is None:
        cutoffs = np.linspace(0.05, 0.95, 37)
    y = np.asarray(y).astype(int)
    scores = np.asarray(scores)
    rows = []
    for cutoff in cutoffs:
        approved = scores <= cutoff
        accepted = y[approved]
        payoff = np.where(accepted == 1, -LOSS_PER_DEFAULT_ACCOUNT,
                          PROFIT_PER_PERFORMING_ACCOUNT)
        rows.append({
            'maximum_predicted_default_probability': round(float(cutoff), 6),
            'approval_rate_pct': round(100 * float(approved.mean()), 4),
            'approved_accounts': int(approved.sum()),
            'observed_default_rate_in_approved_pct': (
                round(100 * float(accepted.mean()), 4) if len(accepted) else None),
            'hypothetical_total_payoff': float(payoff.sum()),
            'hypothetical_payoff_per_applicant': float(payoff.sum() / len(y)),
        })
    return rows


def calibration_rows(y, scores, bins=10):
    """Equal-width risk score bins, with observed bin default frequency."""
    y = np.asarray(y).astype(int)
    scores = np.asarray(scores)
    indices = np.minimum((scores * bins).astype(int), bins - 1)
    rows = []
    for index in range(bins):
        mask = indices == index
        rows.append({'bin_lower': index / bins, 'bin_upper': (index + 1) / bins,
                     'n': int(mask.sum()),
                     'mean_predicted_probability': float(scores[mask].mean()) if mask.any() else None,
                     'observed_default_rate': float(y[mask].mean()) if mask.any() else None})
    return rows


def subgroup_rows(data, y, scores, cutoff):
    """Diagnostic-only comparisons; not evidence of compliance or causation."""
    raw = data.reset_index(drop=True)
    groups = {
        'SEX': raw['SEX'].astype('string').fillna('missing'),
        'AGE_BAND': pd.cut(pd.to_numeric(raw['AGE'], errors='coerce'),
                           [0, 29, 44, 59, 120], labels=['<=29', '30-44', '45-59', '60+']).astype('string').fillna('missing'),
    }
    label = np.asarray(y).astype(int)
    scores = np.asarray(scores)
    predicted = scores >= cutoff
    results = []
    for field, series in groups.items():
        for value in sorted(series.unique()):
            mask = (series == value).to_numpy(dtype=bool)
            positives = (label == 1) & mask
            negatives = (label == 0) & mask
            if mask.sum() < 50:
                continue
            results.append({
                'attribute': field, 'group': str(value), 'n': int(mask.sum()),
                'observed_default_rate': float(label[mask].mean()),
                'average_predicted_risk': float(scores[mask].mean()),
                'false_positive_rate_at_cutoff': (float(predicted[negatives].mean())
                                                  if negatives.any() else None),
                'true_positive_rate_at_cutoff': (float(predicted[positives].mean())
                                                 if positives.any() else None),
            })
    return results


def run(df, output, source):
    """60/20/20 stratified split; select model and cutoff on validation only."""
    if source not in {'uci', 'synthetic_demo'}:
        raise ValueError('Unrecognized source')
    data = validate(df)
    y = data[TARGET].astype(int)
    X = data[FEATURES].copy()  # Excludes ID, sensitive attributes, and outcome.
    idx_trainval, idx_test = train_test_split(np.arange(len(data)), test_size=0.2,
                                               random_state=42, stratify=y)
    idx_train, idx_val = train_test_split(idx_trainval, test_size=0.25,
                                          random_state=42, stratify=y.iloc[idx_trainval])
    x_train, y_train = X.iloc[idx_train], y.iloc[idx_train]
    x_val, y_val = X.iloc[idx_val], y.iloc[idx_val]
    x_test, y_test = X.iloc[idx_test], y.iloc[idx_test]
    if min(y_train.value_counts()) < 10:
        raise ValueError('Insufficient training observations per class')
    scaler = Pipeline([('imputer', SimpleImputer(strategy='median')),
                       ('scale', StandardScaler())])
    models = {
        'prevalence_baseline': DummyClassifier(strategy='prior'),
        'logistic_regression': Pipeline([('prepare', scaler),
            ('model', LogisticRegression(max_iter=1500, random_state=42))]),
        'hist_gradient_boosting': Pipeline([
            ('imputer', SimpleImputer(strategy='median')),
            ('model', HistGradientBoostingClassifier(max_iter=125,
                learning_rate=0.06, max_leaf_nodes=15, min_samples_leaf=50,
                l2_regularization=8, random_state=42))]),
    }
    scored = {}
    for name, model in models.items():
        model.fit(x_train, y_train)
        proba = model.predict_proba(x_val)[:, 1]
        scored[name] = {'model': model, 'validation_scores': proba,
                        'validation_metrics': metric_bundle(y_val, proba)}
    # Baseline is a comparator, never a selected champion.
    candidates = ['logistic_regression', 'hist_gradient_boosting']
    winner = min(candidates, key=lambda name: (
        scored[name]['validation_metrics']['brier_score'],
        -scored[name]['validation_metrics']['roc_auc']))
    best = scored[winner]['model']
    selected_validation = policy_rows(y_val, scored[winner]['validation_scores'])
    # Predefined 0.05:0.95 threshold grid, selected on held-out validation only.
    chosen = max(selected_validation, key=lambda row: (
        row['hypothetical_total_payoff'], -row['maximum_predicted_default_probability']))
    threshold = chosen['maximum_predicted_default_probability']
    test_score = best.predict_proba(x_test)[:, 1]
    selected_test = policy_rows(y_test, test_score, cutoffs=[threshold])[0]
    baseline_test_score = scored['prevalence_baseline']['model'].predict_proba(x_test)[:, 1]
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    val_metric_rows = [{'model': name, **s['validation_metrics']}
                       for name, s in scored.items()]
    pd.DataFrame(val_metric_rows).to_csv(output / 'validation_models.csv', index=False)
    pd.DataFrame(selected_validation).to_csv(output / 'validation_policy_grid.csv', index=False)
    pd.DataFrame(calibration_rows(y_test, test_score)).to_csv(output / 'test_calibration_bins.csv', index=False)
    pd.DataFrame(subgroup_rows(data.iloc[idx_test], y_test, test_score, 0.5)).to_csv(
        output / 'test_subgroup_diagnostics.csv', index=False)
    # Only aggregate score deciles for the test set; no customer-level records in GitHub.
    test_report = {
        'data_source': source,
        'observations': int(len(data)),
        'train_rows': int(len(idx_train)), 'validation_rows': int(len(idx_val)),
        'test_rows': int(len(idx_test)),
        'split': 'stratified random; temporal split impossible on single 2005 cross-section',
        'excluded_features': ['ID'] + SENSITIVE,
        'champion_selected_on_validation': winner,
        'validation_baseline': scored['prevalence_baseline']['validation_metrics'],
        'validation_champion': scored[winner]['validation_metrics'],
        'held_out_test': metric_bundle(y_test, test_score),
        'held_out_test_baseline': metric_bundle(y_test, baseline_test_score),
        'chosen_policy_cutoff_on_validation': threshold,
        'validation_policy': chosen,
        'held_out_test_policy': selected_test,
        'scenario_assumptions': {
            'performing_account_payoff_units': PROFIT_PER_PERFORMING_ACCOUNT,
            'default_account_payoff_units': -LOSS_PER_DEFAULT_ACCOUNT,
            'reject_payoff_units': 0,
        },
        'limitations': [
            'The dataset contains existing Taiwan 2005 credit-card customers; not Affirm loan applicants.',
            'The next-month default outcome is not a loan approval decision or an actual recovery/loss amount.',
            'No per-application decision timestamp exists; chronological holdout is unavailable.',
            'Observed outcomes on cardholders are not counterfactual outcomes for rejected applicants.',
            'Hypothetical payoff coefficients are not real bank profitability or fair-lending policy.',
            'Sensitive fields excluded from features, but exclusion alone does not establish fairness.',
            'Do not deploy this scoring model for real consumer credit decisions.',
        ],
    }
    (output / 'metrics.json').write_text(json.dumps(test_report, indent=2) + '\n', encoding='utf-8')
    (output / 'REPORT.md').write_text(
        f'# Next-month credit-card default model ({source})\n\n'
        f'> **{("SIMULATED demonstration only" if source == "synthetic_demo" else "Real historical UCI data: Taiwan, 2005")}**. '
        'This is a learning case, **not an approved underwriting model**.\n\n'
        f'- Rows: {len(data):,} (train {len(idx_train):,}; validation {len(idx_val):,}; held-out test {len(idx_test):,}).\n'
        f'- Validation-chosen classifier: **{winner.replace("_", " ")}** (minimum validation Brier score).\n'
        f'- Held-out test ROC-AUC: **{test_report["held_out_test"]["roc_auc"]:.4f}**; '
        f'PR-AUC: **{test_report["held_out_test"]["average_precision"]:.4f}**; '
        f'Brier: **{test_report["held_out_test"]["brier_score"]:.4f}**.\n'
        f'- Held-out test F1 at default-probability 0.50: **{test_report["held_out_test"]["f1_at_0_5"]:.4f}**.\n'
        f'- Fictional payoff threshold selected using **validation only**: **{threshold:.3f}** '
        '(approve if estimated default probability <= threshold).\n'
        f'- Held-out scenario approval rate: **{selected_test["approval_rate_pct"]:.2f}%**; '
        f'fictional payoff/application **{selected_test["hypothetical_payoff_per_applicant"]:.2f} units**.\n\n'
        'Model selection and threshold selection never use the final test partition. '
        'See `metrics.json`, `validation_models.csv`, `test_calibration_bins.csv`, '
        'and `test_subgroup_diagnostics.csv` for diagnostics.\n\n'
        '**Interpretation restrictions:** No application decision date permits genuine out-of-time testing. '
        'Our fictional payoff assumption does not estimate real profits, causal intervention effects, '
        'or legally permissible lending decisions. Excluding demographic features does not establish '
        'non-discrimination. Real use would require validation, documented monitoring, governance, '
        'legal review, data access controls, and independent fair-lending testing.\n',
        encoding='utf-8')
    return test_report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mode', choices=['uci', 'synthetic-demo'], required=True)
    parser.add_argument('--file', help='Path to the original UCI XLS for --mode uci')
    parser.add_argument('--output', default=None)
    parser.add_argument('--demo-rows', type=int, default=6000)
    args = parser.parse_args()
    if args.mode == 'uci' and not args.file:
        parser.error('--mode uci requires --file PATH')
    if args.mode == 'uci':
        dataset = load_uci_xls(args.file)
        source = 'uci'
    else:
        dataset = synthetic_sample(args.demo_rows)
        source = 'synthetic_demo'
    out = Path(args.output) if args.output else ROOT / 'outputs' / source
    result = run(dataset, out, source)
    print(json.dumps({k: result[k] for k in ('data_source', 'observations',
          'champion_selected_on_validation', 'held_out_test',
          'chosen_policy_cutoff_on_validation')}, indent=2))


if __name__ == '__main__':
    main()
