"""Parse text-native official answer tables; never infer values from question bodies."""
import json
import re
from common import ROOT, norm, qid, write_csv

FIELDS=['question_id','year','exam_session','source_year_directory','subject','question_number',
        'official_answer','answer_kind','source_file','source_page','official_number',
        'source_line','official_note','verification_method','answer_verified']

def main():
    rows=[]; page_register=[]
    for path in sorted((ROOT/'extracted/text').rglob('*official_answers.txt')):
        source='sources/'+str(path.relative_to(ROOT/'extracted/text').with_suffix('.pdf'))
        for page_number,raw in enumerate(path.read_text().split('\f'),1):
            page=norm(raw)
            if '基礎科目' in page: subject='BASIC'
            elif '適性科目' in page: subject='APT'
            elif re.search(r'17\.\s*応用理学',page): subject='APPLIED'
            else: continue
            match=re.search(r'(平成|令和)(元|\d+)年度',page)
            if not match: raise ValueError((path,page_number,'year missing'))
            era,n=match.groups(); directory=('H' if era=='平成' else 'R')+f'{1 if n=="元" else int(n):02}'
            if '再試験' in page: directory+='_retest'
            pattern = re.compile(r'(I|II|III|IV)\s*-\s*(\d+)(?:\s*-\s*(\d+))?')
            # Everything following the table is preserved as an official note.
            note_match=re.search(r'(?m)^\s*[*※]\s*(?:[ⅠⅡⅢⅣ]|I)',raw)
            notes=raw[note_match.start():].strip() if note_match else ''
            in_note=False; count=0
            for original in raw.splitlines():
                line=norm(original).strip()
                if re.match(r'^[*※]\s*(?:I|II|III|IV)\s*-',line): in_note=True
                if in_note or not re.match(r'^(?:I|II|III|IV)\s*-',line): continue
                hits=list(pattern.finditer(line))
                for i,hit in enumerate(hits):
                    prefix,a,b=hit.groups()
                    number=f'{int(a)}-{int(b)}' if b else str(int(a))
                    value=line[hit.end():hits[i+1].start() if i+1<len(hits) else len(line)].strip()
                    vals=re.findall(r'[1-5]',value)
                    if '又は' in value and len(vals)==2: answer='|'.join(vals); kind='multiple_accepted'
                    elif len(vals)==1 and re.fullmatch(r'[*※]?\s*[1-5]\s*[*※]?',value): answer=vals[0];kind='single'
                    elif re.fullmatch(r'[*※]',value) and '全員に得点' in norm(notes): answer='ALL';kind='all_awarded'
                    elif re.fullmatch(r'[*※]',value): answer='';kind='official_note_required'
                    else: raise ValueError((source,page_number,line,value))
                    if subject=='BASIC': assert prefix=='I' and b
                    if subject=='APT': assert prefix=='II' and not b
                    if subject=='APPLIED': assert prefix in ('III','IV') and not b
                    rows.append(dict(zip(FIELDS,[qid(directory,subject,number),directory.replace('_retest',''),
                        'RET' if directory.endswith('_retest') else 'REG',directory,subject,number,answer,kind,
                        source,page_number,hit.group(0),original.strip(),notes,'text_native_table_structural_check','true' if answer else 'false'])))
                    count+=1
            page_register.append({'source':source,'page':page_number,'year':directory,'subject':subject,'count':count,'note':notes})
    ids=[r['question_id'] for r in rows]
    assert len(ids)==len(set(ids)), 'Duplicate answer IDs'
    write_csv('data/answers_official.csv',rows,FIELDS)
    (ROOT/'extracted/logs/answer_pages.json').write_text(json.dumps(page_register,ensure_ascii=False,indent=2))
    for page in page_register: print(page['year'],page['subject'],page['count'],page['note'])
    print('Official answer rows:',len(rows))

if __name__=='__main__': main()
