"""Project paths, deterministic CSV and recoverable multi-file publication."""
import csv
import hashlib
import io
import json
import os
import re
import shutil
import tempfile
import unicodedata
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
YEARS = [*[f'H{x}' for x in range(23,31)], 'R01', 'R01_retest', *[f'R{x:02}' for x in range(2,8)]]
SUBJECTS = {'basic':'BASIC', 'aptitude':'APT', '17_applied_science':'APPLIED'}

def now(): return datetime.now(timezone(timedelta(hours=9))).isoformat(timespec='seconds')
def digest(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def read_csv(path):
    if (ROOT/'data/publication.lock').exists():raise RuntimeError('Publication in progress or interrupted; recover before reading')
    with (ROOT/path).open(encoding='utf-8-sig',newline='') as f: return list(csv.DictReader(f))
def csv_bytes(rows, fields=None):
    fields = fields or (list(rows[0]) if rows else [])
    stream=io.StringIO(newline='');writer=csv.DictWriter(stream,fieldnames=fields)
    writer.writeheader();writer.writerows(rows)
    return stream.getvalue().encode('utf-8-sig')
def json_bytes(value): return (json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
def verification_payload_hash(row,kind):
    fields={'classification':['discipline_id','chapter_id','concept_id','major_category','middle_category','minor_category','topic','taxonomy_version'],
            'summary':['question_summary'],
            'solution':['solution_summary','wrong_choice_summary','explanation_citations','explanation_reference_date']}.get(kind,[])
    return hashlib.sha256(json_bytes({k:row.get(k,'') for k in fields})).hexdigest() if fields else ''
def publish_bundle(files, validator=None):
    """Stage and validate before any replacement; retain recovery snapshot/journal.

    Consumers must not read while publication.lock exists. A crash leaves a journal
    and prevents the next publication; recover_publication.py restores the snapshot.
    """
    payload={str(k):(v.encode('utf-8') if isinstance(v,str) else v) for k,v in files.items()}
    changed={k:v for k,v in payload.items() if not (ROOT/k).exists() or (ROOT/k).read_bytes()!=v}
    if not changed:return
    lock=ROOT/'data/publication.lock';lock.parent.mkdir(parents=True,exist_ok=True)
    try:fd=os.open(str(lock),os.O_CREAT|os.O_EXCL|os.O_WRONLY)
    except FileExistsError:raise RuntimeError('Interrupted or concurrent publication: inspect data/publication.lock')
    os.close(fd)
    txn=ROOT/'snapshots'/('txn_'+datetime.now().strftime('%Y%m%dT%H%M%S%f'))
    txn.mkdir(parents=True);journal={'status':'staging','time':now(),'paths':list(changed),'existed':{},'sha256':{}}
    staged={};replaced=[]
    try:
        (txn/'journal.json').write_bytes(json_bytes(journal))
        lock.write_text(str(txn.relative_to(ROOT)))
        for key,data in changed.items():
            path=ROOT/key
            if not path.resolve().is_relative_to(ROOT.resolve()):raise ValueError('Outside project: '+key)
            journal['existed'][key]=path.exists()
            if path.exists():
                backup=txn/'before'/key;backup.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(path,backup)
            stage=txn/'after'/key;stage.parent.mkdir(parents=True,exist_ok=True)
            with stage.open('wb') as out:out.write(data);out.flush();os.fsync(out.fileno())
            staged[key]=stage;journal['sha256'][key]=hashlib.sha256(data).hexdigest()
        if validator:validator(staged)
        journal['status']='prepared';(txn/'journal.json').write_bytes(json_bytes(journal))
        for key,stage in staged.items():
            path=ROOT/key;path.parent.mkdir(parents=True,exist_ok=True)
            # Copy rather than move: keep staged after-image for recovery/audit.
            handle,tmp=tempfile.mkstemp(prefix='.'+path.name,dir=path.parent)
            with os.fdopen(handle,'wb') as out:out.write(stage.read_bytes());out.flush();os.fsync(out.fileno())
            os.replace(tmp,path);replaced.append(key)
        journal['status']='committed';(txn/'journal.json').write_bytes(json_bytes(journal))
    except BaseException:
        for key in reversed(replaced):
            if journal['existed'][key]:shutil.copy2(txn/'before'/key,ROOT/key)
            else:(ROOT/key).unlink(missing_ok=True)
        journal['status']='rolled_back';(txn/'journal.json').write_bytes(json_bytes(journal));raise
    finally:lock.unlink(missing_ok=True)

def write_csv(path, rows, fields=None):publish_bundle({path:csv_bytes(rows,fields)})
def norm(text):
    return re.sub(r'[－−―—–ーｰ]','-',unicodedata.normalize('NFKC',text))
def qid(directory,subject,number):
    year=directory.replace('_retest','');session='RET' if directory.endswith('_retest') else 'REG'
    number=number if subject=='BASIC' else f'{int(number):02}'
    return f'{year}-{session}-{subject}-{number}'
def year_label(directory):
    n=int(directory[1:3]);era='平成' if directory[0]=='H' else '令和'
    label=f'{era}{"元" if era=="令和" and n==1 else n}年度'
    return label+('再試験' if directory.endswith('_retest') else '')
