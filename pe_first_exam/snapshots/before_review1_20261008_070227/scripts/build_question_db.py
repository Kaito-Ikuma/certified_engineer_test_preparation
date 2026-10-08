"""Build questions only from observed page headings, cross-checked with official IDs."""
import json
import re
from collections import defaultdict
from common import ROOT, YEARS, SUBJECTS, read_csv, write_csv, norm, qid, year_label

FIELDS='question_id year era_year exam_session subject question_number source_file source_page major_category middle_category minor_category topic subtopic question_type requires_calculation requires_figure requires_law difficulty priority official_answer answer_verified question_summary core_concept required_knowledge solution_summary wrong_choice_summary related_question_ids tex_label tex_file status needs_manual_verification notes astra_review_required source_year_directory source_page_end printed_question_number heading_text heading_line_index heading_bbox boundary_verified question_text_file extraction_method ocr_min_confidence summary_verified answer_kind answer_source_file answer_source_page classification_method classification_confidence classification_verified'.split()

def candidates(subject,line):
    raw=line['text'].strip(); text=norm(raw).replace('一','-')
    if not raw or raw[0] in '①②③④⑤⑥⑦⑧⑨' or line['x']>.30: return []
    if subject=='BASIC':
        match=re.match(r'^.{1,4}?\s*-?\s*([1-5])\s*-\s*(\d+)',text)
        if not match: return []
        g,digits=match.groups()
        # A heading may join to numeric prose: I-3-2 + 2次 => I-3-22次.
        return [(f'{g}-{digits[0]}',match.group(0))] if digits[0] in '1234567' else []
    match=re.match(r'^([^\d]{1,4}|[1Il]{1,4})\s*-\s*(\d+)',text)
    if not match:return []
    digits=match.group(2)
    possibilities=[]
    for length in (2,1):
        if len(digits)>=length and 1<=int(digits[:length])<= (15 if subject=='APT' else 35):
            possibilities.append((str(int(digits[:length])), match.group(0)))
    return possibilities

def main():
    answers=read_csv('data/answers_official.csv')
    groups=defaultdict(list)
    for row in answers: groups[(row['source_year_directory'],row['subject'])].append(row)
    overrides={}
    overridepath=ROOT/'config/boundary_overrides.json'
    if overridepath.exists():overrides=json.loads(overridepath.read_text())
    records=[]; issues=[]; boundary_audit=[]
    for directory in YEARS:
        for stem,subject in SUBJECTS.items():
            path=ROOT/'extracted/text'/directory/(stem+'.json')
            if not path.exists():raise FileNotFoundError(path)
            metadata=json.loads(path.read_text())
            expected=groups[(directory,subject)]
            expected.sort(key=lambda x:tuple(int(t) for t in x['question_number'].split('-')))
            expected_map={row['question_number']:row for row in expected}
            ordered=[row['question_number'] for row in expected]
            locations=[]; flattened=[]
            for page in metadata['pages']:
                for line_index,line in enumerate(page.get('lines',[])):
                    flattened.append((page['page'],line_index,line))
            # Greedy ordered recognition; skipped headings are reported, never fabricated.
            next_index=0
            for pos,(page,line_index,line) in enumerate(flattened):
                options=candidates(subject,line)
                override_key=f'{directory}/{stem}/{page}/{line_index}'
                if override_key in overrides: options=[(overrides[override_key]['number'],line['text'])]
                remaining=[n for n,_ in options if n in ordered[next_index:]]
                if not remaining: continue
                # Select the earliest compatible upcoming number, then audit any gaps.
                number=min(remaining,key=ordered.index)
                index=ordered.index(number)
                # Far jumps usually are equations; only accept if prefix is a heading or manually verified.
                if index-next_index>2 and override_key not in overrides:continue
                locations.append((number,pos,page,line_index,line,override_key in overrides))
                next_index=index+1
            found={x[0] for x in locations}
            missing=set(ordered)-found
            for n in sorted(missing):issues.append({'question_id':qid(directory,subject,n),'issue':'heading_not_found','source':metadata['source']})
            boundary_audit.append({'year':directory,'subject':subject,'expected':len(ordered),'found':len(found),'missing':sorted(missing)})
            for i,(number,pos,page,line_index,line,manual) in enumerate(locations):
                end=locations[i+1][1] if i+1<len(locations) else len(flattened)
                body=flattened[pos:end]
                text='\n'.join(l['text'] for _,_,l in body)
                question_id=qid(directory,subject,number); a=expected_map[number]
                record={field:'' for field in FIELDS}
                # Footer exclusion is lexical; raw OCR remains intact in page JSON.
                content=[l['text'] for _,_,l in body if not re.search(r'(基礎|適性|応用理学).*[（(][HR]',l['text'])]
                record.update(question_id=question_id,year=directory.replace('_retest',''),era_year=year_label(directory),
                    exam_session='RET' if directory.endswith('_retest') else 'REG',subject=subject,question_number=number,
                    source_file=metadata['source'],source_page=page,source_page_end=body[-1][0],source_year_directory=directory,
                    official_answer=a['official_answer'],answer_verified=a['answer_verified'],answer_kind=a['answer_kind'],
                    answer_source_file=a['source_file'],answer_source_page=a['source_page'],
                    printed_question_number=a['official_number'],heading_text=line['text'],heading_line_index=line_index,
                    heading_bbox=json.dumps({k:line[k] for k in ['x','y','width','height']}),
                    boundary_verified='true' if manual else 'false',extraction_method='ocr_unverified',
                    ocr_min_confidence=min(l['confidence'] for _,_,l in body),
                    question_summary='',summary_verified='false',tex_label='q:'+question_id.lower(),
                    status='registered_initial',needs_manual_verification='true',astra_review_required='true',
                    notes='OCR本文未校正。分類と要約は暫定。解説・難易度・優先度は後工程。')
                textfile=ROOT/'extracted/questions'/(question_id+'.txt');textfile.parent.mkdir(exist_ok=True)
                textfile.write_text('\n'.join(content))
                record['question_text_file']=str(textfile.relative_to(ROOT))
                records.append(record)
    write_csv('data/questions.csv',records,FIELDS)
    (ROOT/'extracted/logs/boundary_audit.json').write_text(json.dumps(boundary_audit,ensure_ascii=False,indent=2))
    (ROOT/'extracted/logs/boundary_missing.json').write_text(json.dumps(issues,ensure_ascii=False,indent=2))
    print(f'Registered {len(records)}; missing headings {len(issues)}')
    for row in boundary_audit:
        if row['missing']:print(row)

if __name__=='__main__':main()
