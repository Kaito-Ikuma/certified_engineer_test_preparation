"""Collect official answer attachments; preserves the original combined H23-H30 file."""
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def main():
    entries = [('R07', 4), ('R06', 5), ('R05', 6), ('R04', 7), ('R03', 8),
               ('R02', 9), ('R01_retest', 10), ('R01', 11), ('H23_H30', 12)]
    for year, attachment in entries:
        path = ROOT / 'sources' / ('answers' if year == 'H23_H30' else year) / ('H23_H30_official_answers.pdf' if year == 'H23_H30' else 'official_answers.pdf')
        path.parent.mkdir(parents=True, exist_ok=True)
        url = f'https://www.engineer.or.jp/c_topics/004/attached/attach_4106_{attachment}.pdf'
        if not path.exists():
            subprocess.run(['curl', '-fL', '--retry', '3', '--max-time', '90', url, '-o', str(path)], check=True)
        assert path.read_bytes().startswith(b'%PDF-')
        print(year, path.relative_to(ROOT), flush=True)
if __name__ == '__main__': main()
