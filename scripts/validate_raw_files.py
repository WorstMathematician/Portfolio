from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECTS = {
    'Program Finance Control Tower': ROOT / 'Program-Finance-Control-Tower' / 'data' / 'raw',
    'Budget vs Actual Variance': ROOT / 'Budget-vs-Actual-FPA-Variance-Analysis' / 'data' / 'raw',
    'Defense Peer Benchmarking': ROOT / 'Defense-Contractor-Peer-Benchmarking' / 'data' / 'raw',
}
VALID_EXTENSIONS = {'.csv', '.xlsx', '.xls', '.json'}

ok = True
for name, raw_dir in PROJECTS.items():
    files = [p for p in raw_dir.iterdir() if p.is_file() and p.suffix.lower() in VALID_EXTENSIONS]
    if files:
        print('OK:', name)
        for file in files:
            print(' -', file.relative_to(ROOT))
    else:
        ok = False
        print('MISSING:', name, 'has no dataset files in', raw_dir.relative_to(ROOT))

raise SystemExit(0 if ok else 1)
