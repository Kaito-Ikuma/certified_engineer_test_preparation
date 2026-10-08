import csv
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
YEARS = [*[f'H{x}' for x in range(23,31)], 'R01', 'R01_retest', *[f'R{x:02}' for x in range(2,8)]]
SUBJECTS = {'basic':'BASIC', 'aptitude':'APT', '17_applied_science':'APPLIED'}
def read_csv(path):
    with (ROOT/path).open(encoding='utf-8-sig',newline='') as f: return list(csv.DictReader(f))
def write_csv(path, rows, fields=None):
    path = ROOT/path
    path.parent.mkdir(parents=True,exist_ok=True)
    fields = fields or list(rows[0])
    with path.open('w',encoding='utf-8-sig',newline='') as f:
        writer = csv.DictWriter(f,fieldnames=fields)
        writer.writeheader(); writer.writerows(rows)
def norm(text):
    text = unicodedata.normalize('NFKC',text)
    return re.sub(r'[－−―—–ーｰ]', '-', text)
def qid(directory,subject,number):
    year=directory.replace('_retest','')
    session='RET' if directory.endswith('_retest') else 'REG'
    number=number if subject=='BASIC' else f'{int(number):02}'
    return f'{year}-{session}-{subject}-{number}'
def year_label(directory):
    n=int(directory[1:3]); era='平成' if directory[0]=='H' else '令和'
    label=f'{era}{"元" if era=="令和" and n==1 else n}年度'
    return label + ('再試験' if directory.endswith('_retest') else '')
