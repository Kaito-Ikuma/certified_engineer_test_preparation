"""Refresh inventory while preserving existing official URL provenance."""
import hashlib
import re
import subprocess
from common import ROOT, read_csv, write_csv, SUBJECTS

def main():
    existing={r['path']:r for r in read_csv('data/source_files.csv')}
    attachments=dict(R07=4,R06=5,R05=6,R04=7,R03=8,R02=9,R01_retest=10,R01=11,answers=12)
    rows=[]
    for path in sorted((ROOT/'sources').rglob('*.pdf')):
        relative=str(path.relative_to(ROOT)); directory=path.parent.name
        old=existing.get(relative,{})
        official='official_answers' in path.stem
        url=old.get('url','')
        if official: url=f'https://www.engineer.or.jp/c_topics/004/attached/attach_4106_{attachments[directory]}.pdf'
        data=path.read_bytes()
        result=subprocess.run(['pdfinfo',str(path)],capture_output=True,text=True,check=True)
        count=int(re.search(r'^Pages:\s+(\d+)',result.stdout,re.M).group(1))
        rows.append({'year':old.get('year',directory),'subject':old.get('subject','official_answers'),
            'official_label':old.get('official_label',directory),'path':relative,'url':url,'size_bytes':len(data),
            'sha256':hashlib.sha256(data).hexdigest(),'source_type':'official_answers' if official else 'question',
            'target_scope':'true' if official or path.stem in SUBJECTS else 'false','page_count':count})
    write_csv('data/source_files.csv',rows)
    print(f'Inventory: {len(rows)} PDFs; target question PDFs: {sum(r["source_type"]=="question" and r["target_scope"]=="true" for r in rows)}')

if __name__=='__main__': main()
