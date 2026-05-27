from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
RAW = DATA / 'raw'
OUT = ROOT / 'outputs'


def load_inputs():
    acs_path = RAW / 'acs_income_zcta_2015_2024.csv'
    zillow_path = RAW / 'Zip_zori_uc_sfrcondomfr_sm_month.csv'
    if not acs_path.exists() or not zillow_path.exists():
        raise FileNotFoundError('Place ACS and Zillow CSV files in data/raw before running the full pipeline.')
    acs = pd.read_csv(acs_path)
    zillow = pd.read_csv(zillow_path)
    return acs, zillow


def summarize_clean_panel(panel):
    summary = {
        'observations': len(panel),
        'unique_zip_codes': panel['zcta'].nunique() if 'zcta' in panel else None,
        'mean_rent_to_income_pct': panel['pct_rent_income'].mean() if 'pct_rent_income' in panel else None,
        'median_rent_to_income_pct': panel['pct_rent_income'].median() if 'pct_rent_income' in panel else None,
        'share_cost_burdened_pct': panel['cost_burdened_30pct'].mean() * 100 if 'cost_burdened_30pct' in panel else None,
    }
    return pd.DataFrame([summary])


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    print('This repository version contains a pipeline skeleton and final reported outputs.')
    print('Place the original ACS and Zillow CSV files in data/raw to rebuild the full analysis locally.')


if __name__ == '__main__':
    main()
