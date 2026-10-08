"""Try Poppler first; optionally OCR only pages lacking extractable text."""
import argparse
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def extract(path, ocr):
    relative = path.relative_to(ROOT / 'sources').with_suffix('')
    textpath = ROOT / 'extracted/text' / relative.with_suffix('.txt')
    textpath.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(['pdftotext', '-layout', str(path), str(textpath)], check=True)
    pages = textpath.read_text().split('\f')[:-1]
    images = ROOT / 'extracted/pages' / relative
    results = []
    for i, page in enumerate(pages, 1):
        if page.strip():
            results.append({'page': i, 'method': 'pdftotext', 'text': page})
        elif ocr:
            jsonpath = images / f'page_{i:03d}.json'
            if not jsonpath.exists():
                process = subprocess.run([str(ROOT/'scripts/ocr_pdf'), str(path), str(images), str(i), str(i)], capture_output=True, text=True)
                if process.returncode:
                    raise RuntimeError(f'{path} page {i}: {process.stderr}')
            result = json.loads(jsonpath.read_text())
            result['method'] = 'ocr_unverified'
            result['text'] = '\n'.join(line['text'] for line in result['lines'])
            results.append(result)
        else:
            results.append({'page': i, 'method': 'no_text', 'text': ''})
    combined = '\f'.join(result['text'] for result in results) + '\f'
    textpath.write_text(combined)
    metadata = textpath.with_suffix('.json')
    metadata.write_text(json.dumps({'source': str(path.relative_to(ROOT)), 'pages': results}, ensure_ascii=False, indent=2))
    print(f'{relative}: {len(results)} pages; {sum(bool(r["text"].strip()) for r in results)} nonempty', flush=True)
    return [str(path.relative_to(ROOT)), len(results), sum(r['method'] == 'ocr_unverified' for r in results)]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ocr', action='store_true')
    parser.add_argument('--answers-only', action='store_true')
    parser.add_argument('--workers', type=int, default=2)
    args = parser.parse_args()
    targets = sorted(p for p in (ROOT/'sources').rglob('*.pdf') if
                     (p.name in ['basic.pdf','aptitude.pdf','17_applied_science.pdf'] and not args.answers_only)
                     or 'official_answers' in p.name)
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        rows = list(pool.map(lambda p: extract(p, args.ocr), targets))
    (ROOT/'extracted/logs/extraction_summary.json').write_text(json.dumps(rows, indent=2))

if __name__ == '__main__': main()
