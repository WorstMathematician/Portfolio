"""Download the original UCI dataset ZIP; keep raw research data out of Git.

Official source: https://archive.ics.uci.edu/dataset/350/default+of+credit+card+clients
Yeh, I-C. (2009), CC BY 4.0, DOI 10.24432/C55S3H.
"""
import argparse
import hashlib
import io
import zipfile
from pathlib import Path
from urllib.request import Request, urlopen

URL = 'https://archive.ics.uci.edu/static/public/350/default+of+credit+card+clients.zip'


def download(out):
    out = Path(out)
    if out.exists():
        raise FileExistsError(f'Destination exists; will not overwrite: {out}')
    request = Request(URL, headers={'User-Agent': 'Portfolio-Research/1.0'})
    with urlopen(request, timeout=90) as response:
        contents = response.read()
    sha = hashlib.sha256(contents).hexdigest()
    with zipfile.ZipFile(io.BytesIO(contents)) as package:
        members = [name for name in package.namelist()
                   if name.lower().endswith('.xls') and '/' not in name]
        if len(members) != 1:
            raise ValueError(f'Expected one original XLS in ZIP, found: {members}')
        payload = package.read(members[0])
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(payload)
    print('Downloaded original XLS from UCI; ZIP SHA256:', sha)
    print('Original XLS saved to:', out)
    return out


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', default=str(Path(__file__).resolve().parents[1] /
                                                 'data' / 'default of credit card clients.xls'))
    args = parser.parse_args()
    download(args.output)
