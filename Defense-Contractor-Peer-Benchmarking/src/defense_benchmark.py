from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'data' / 'raw'
OUT = ROOT / 'outputs'


def find_file():
    files = sorted(RAW.glob('*.csv'))
    if not files:
        raise FileNotFoundError('Place the Kaggle CSV in data/raw before running this script.')
    return files[0]


def clean_columns(df):
    out = df.copy()
    out.columns = [str(c).strip().replace(' ', '_') for c in out.columns]
    return out


def pick(df, candidates):
    low = {c.lower(): c for c in df.columns}
    for candidate in candidates:
        if candidate.lower() in low:
            return low[candidate.lower()]
    for col in df.columns:
        for candidate in candidates:
            if candidate.lower() in col.lower():
                return col
    return None


def main():
    path = find_file()
    df = clean_columns(pd.read_csv(path))

    year_col = pick(df, ['Year'])
    company_col = pick(df, ['Company', 'Name'])
    country_col = pick(df, ['Country'])
    revenue_col = pick(df, ['Total_Revenue(in_millions)', 'Total_Revenue', 'Revenue'])
    share_col = pick(df, ['Percentage_of_Revenue_From_Defence', 'Percentage_of_Revenue_From_Defense', 'Defense_Revenue_Percentage'])

    if not all([year_col, company_col, revenue_col, share_col]):
        raise ValueError('Missing required fields for benchmarking analysis.')

    panel = pd.DataFrame({
        'year': pd.to_numeric(df[year_col], errors='coerce'),
        'company': df[company_col].astype(str).str.strip(),
        'country': df[country_col].astype(str).str.strip() if country_col else 'Unknown',
        'total_revenue_m': pd.to_numeric(df[revenue_col], errors='coerce'),
        'category_revenue_pct': pd.to_numeric(df[share_col], errors='coerce'),
    }).dropna(subset=['year', 'company', 'total_revenue_m', 'category_revenue_pct'])

    panel = panel[(panel['total_revenue_m'] > 0) & (panel['category_revenue_pct'] >= 0)]
    panel['category_revenue_m'] = panel['total_revenue_m'] * panel['category_revenue_pct'] / 100

    latest_year = int(panel['year'].max())
    latest = panel[panel['year'] == latest_year].copy()
    latest['market_share'] = latest['category_revenue_m'] / latest['category_revenue_m'].sum()
    latest = latest.sort_values('category_revenue_m', ascending=False)

    cagr_rows = []
    for company, group in panel.groupby('company'):
        group = group.sort_values('year')
        first = group.iloc[0]
        last = group.iloc[-1]
        years = last['year'] - first['year']
        if years >= 5 and first['category_revenue_m'] > 0 and last['category_revenue_m'] > 0:
            cagr = (last['category_revenue_m'] / first['category_revenue_m']) ** (1 / years) - 1
            cagr_rows.append({
                'company': company,
                'start_year': int(first['year']),
                'end_year': int(last['year']),
                'start_revenue_m': first['category_revenue_m'],
                'end_revenue_m': last['category_revenue_m'],
                'cagr': cagr,
            })
    cagr = pd.DataFrame(cagr_rows).sort_values('cagr', ascending=False)

    country = latest.groupby('country', as_index=False).agg(category_revenue_m=('category_revenue_m', 'sum'))
    country['share'] = country['category_revenue_m'] / country['category_revenue_m'].sum()
    country = country.sort_values('category_revenue_m', ascending=False)

    base_revenue = latest['category_revenue_m'].median()
    base_growth = cagr['cagr'].median() if not cagr.empty else 0.04
    scenarios = []
    for scenario, growth in {'Downside': max(base_growth - 0.03, 0), 'Base': base_growth, 'Upside': base_growth + 0.03}.items():
        for year_offset in range(0, 4):
            scenarios.append({
                'scenario': scenario,
                'year': latest_year + year_offset,
                'revenue_m': base_revenue * ((1 + growth) ** year_offset),
                'growth_assumption': growth,
            })

    OUT.mkdir(parents=True, exist_ok=True)
    panel.to_csv(OUT / 'defense_revenue_panel.csv', index=False)
    latest.to_csv(OUT / 'latest_company_benchmark.csv', index=False)
    cagr.to_csv(OUT / 'company_cagr_summary.csv', index=False)
    country.to_csv(OUT / 'country_revenue_summary.csv', index=False)
    pd.DataFrame(scenarios).to_csv(OUT / 'long_range_plan_scenarios.csv', index=False)
    print('Wrote benchmarking outputs to', OUT)


if __name__ == '__main__':
    main()
