"""Download original historical Measure H PDFs for independent page-by-page QA.

Run locally:
  python scripts/collect_historical_sources.py --manifest data/historical_pdf_sources.csv --output data/source_pdfs
PDFs are not financial observations. Review extracted tables before adding model data.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
from pathlib import Path
from urllib.request import Request, urlopen

ALLOWED_HOSTS = {"homeless.lacounty.gov", "file.lacounty.gov"}
MAX_BYTES = 30_000_000

def fetch_one(url: str, output: Path) -> dict:
    from urllib.parse import urlparse
    parsed = urlparse(url)
    if parsed.scheme != "https" or parsed.hostname not in ALLOWED_HOSTS:
        raise ValueError("Unapproved government source URL")
    req = Request(url, headers={"User-Agent": "PublicFinancePortfolioResearch/1.0"})
    with urlopen(req, timeout=30) as response:
        first = response.read(5)
        if first != b"%PDF-":
            raise ValueError("Source is not a PDF: refusing to save HTML/error page")
        chunks = [first]
        total = len(first)
        while True:
            chunk = response.read(1024 * 256)
            if not chunk:
                break
            total += len(chunk)
            if total > MAX_BYTES:
                raise ValueError("PDF exceeded 30 MB limit")
            chunks.append(chunk)
    data = b"".join(chunks)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(data)
    return {"url": url, "local_path": str(output), "size_bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest(), "download_status": "ok",
            "table_verified": False}

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", default="data/historical_pdf_sources.csv")
    ap.add_argument("--output", default="data/source_pdfs")
    args = ap.parse_args()
    with open(args.manifest, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    out = Path(args.output)
    results = []
    for row in rows:
        try:
            status = fetch_one(row["url"], out / (row["fiscal_year"] + ".pdf"))
            print("Downloaded:", row["fiscal_year"], status["sha256"])
        except Exception as e:
            status = {"url": row["url"], "download_status": "failed",
                      "error": str(e), "table_verified": False}
            print("Source unavailable:", row["fiscal_year"], str(e))
        status["fiscal_year"] = row["fiscal_year"]
        status["target_kind"] = row["target_kind"]
        results.append(status)
    out.mkdir(parents=True, exist_ok=True)
    (out / "download_manifest.json").write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    if any(r["download_status"] == "failed" for r in results):
        raise SystemExit("Some downloads failed. See download_manifest.json; do not invent records.")
if __name__ == "__main__":
    main()
