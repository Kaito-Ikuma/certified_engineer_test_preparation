"""Download the official first-exam question PDFs and record provenance."""
import csv
import hashlib
import re
import subprocess
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin

ROOT = Path(__file__).resolve().parents[1]
INDEX = 'https://www.engineer.or.jp/c_categories/index02021.html'

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.items = []
        self.href = None
        self.label = ''
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            href = dict(attrs).get('href', '')
            if href.lower().endswith('.pdf'):
                self.href, self.label = href, ''
    def handle_data(self, data):
        if self.href:
            self.label += data
    def handle_endtag(self, tag):
        if tag == 'a' and self.href:
            self.items.append((urljoin(INDEX, self.href), self.label.strip()))
            self.href = None

def main():
    snapshot = ROOT / 'sources' / 'index02021.html'
    snapshot.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(['curl', '-fsSL', '--retry', '3', '--max-time', '60', INDEX, '-o', str(snapshot)], check=True)
    parser = Links()
    parser.feed(snapshot.read_text(encoding='utf-8'))
    subjects = ['basic', 'aptitude', '01_mechanical', '02_marine', '03_aerospace',
                '04_electrical_electronics', '05_chemistry', '06_textile', '07_metals',
                '08_resources', '09_construction', '10_water_supply_sewerage',
                '11_sanitary', '12_agriculture', '13_forest', '14_fisheries',
                '15_industrial', '16_information', '17_applied_science',
                '18_biotechnology', '19_environment', '20_nuclear_radiation']
    assert len(parser.items) == 352, f'Unexpected link count: {len(parser.items)}'
    jobs = []
    for i, (url, label) in enumerate(parser.items):
        match = re.search(r'(平成|令和)(元|\d+)年度', label)
        assert match, label
        era, number = match.groups()
        year = ('H' if era == '平成' else 'R') + f'{1 if number == "元" else int(number):02d}'
        if '再' in label:
            year += '_retest'
        subject = subjects[i // 16]
        path = ROOT / 'sources' / year / f'{subject}.pdf'
        jobs.append((year, subject, label, url, path))
    def fetch(job):
        year, subject, label, url, path = job
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists():
            temp = path.with_suffix('.pdf.part')
            subprocess.run(['curl', '-fsSL', '--retry', '3', '--max-time', '90', url, '-o', str(temp)], check=True)
            assert temp.read_bytes().startswith(b'%PDF-'), url
            temp.replace(path)
        data = path.read_bytes()
        assert data.startswith(b'%PDF-') and b'%%EOF' in data[-4096:], path
        return [year, subject, label, str(path.relative_to(ROOT)), url, len(data), hashlib.sha256(data).hexdigest()]
    with ThreadPoolExecutor(max_workers=4) as pool:
        rows = []
        for row in pool.map(fetch, jobs):
            rows.append(row)
            if len(rows) % 22 == 0:
                print(f'Downloaded and verified {len(rows)}/352', flush=True)
    (ROOT / 'data').mkdir(exist_ok=True)
    with (ROOT / 'data' / 'source_files.csv').open('w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['year', 'subject', 'official_label', 'path', 'url', 'size_bytes', 'sha256'])
        writer.writerows(rows)
    print(f'Complete: {len(rows)} PDFs, {sum(r[5] for r in rows):,} bytes', flush=True)

if __name__ == '__main__':
    main()
