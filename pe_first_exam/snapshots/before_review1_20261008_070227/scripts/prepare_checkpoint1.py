"""Save the first review package without generating final statistics or a textbook."""
import hashlib
import json
from collections import defaultdict
from common import ROOT, read_csv, write_csv
from build_question_db import FIELDS

def main():
    metrics=json.loads((ROOT/'extracted/logs/audit_metrics.json').read_text())
    assert metrics['initial_audit_passed'], 'Initial audit failed'
    rows=read_csv('data/questions.csv')
    schema={'version':'0.1-initial','primary_key':'question_id','encoding':'UTF-8 with BOM',
            'status':'proposed_for_astra_review','canonical_table':'data/questions.csv','fields':[]}
    for field in FIELDS:
        spec={'name':field,'type':'string','empty_allowed':True}
        if field in ['question_id','year','era_year','exam_session','subject','question_number','source_file','source_page','source_page_end','official_answer','answer_verified','major_category','middle_category','minor_category','topic','tex_label','tex_file','status','needs_manual_verification','question_text_file']:
            spec['empty_allowed']=False
        if field in ['requires_calculation','requires_figure','requires_law']:
            spec.update(type='tri_state',allowed_values=['true','false','unknown'],empty_allowed=False)
        elif field in ['answer_verified','needs_manual_verification','astra_review_required','boundary_verified','summary_verified','classification_verified']:
            spec.update(type='boolean_literal',allowed_values=['true','false'],empty_allowed=False)
        elif field in ['source_page','source_page_end','answer_source_page','heading_line_index']:
            spec.update(type='integer_string',minimum=0 if field=='heading_line_index' else 1)
        elif field=='difficulty':spec.update(type='optional_integer_string',allowed_values=['','1','2','3','4','5'])
        elif field=='priority':spec.update(allowed_values=['','S','A','B','C'])
        elif field=='subject':spec.update(allowed_values=['BASIC','APT','APPLIED'])
        elif field=='exam_session':spec.update(allowed_values=['REG','RET'])
        elif field=='official_answer':spec.update(pattern=r'[1-5](\|[1-5])*|ALL')
        elif field=='answer_kind':spec.update(allowed_values=['single','multiple_accepted','all_awarded','official_note_required'])
        schema['fields'].append(spec)
    for row in rows:
        for spec in schema['fields']:
            value=row[spec['name']]
            assert value or spec['empty_allowed'],(row['question_id'],spec['name'])
            if 'allowed_values' in spec:assert value in spec['allowed_values'],(row['question_id'],spec['name'],value)
    (ROOT/'config/question_schema.json').write_text(json.dumps(schema,ensure_ascii=False,indent=2))
    seen=defaultdict(int);queue=[]
    for row in rows:
        group=(row['subject'],row['major_category'],row['middle_category']);reasons=[]
        if row['classification_confidence']=='low':reasons.append('low_confidence')
        if row['classification_method']=='manual_content_review':reasons.append('manual_override')
        if row['answer_kind']!='single':reasons.append('official_special_treatment')
        if row['subject']=='APPLIED' and row['middle_category'] in ['同位体地球化学','地球化学','地球内部・プレート','物理探査','原子・分子・結晶']:
            if seen[group]<4:reasons.append('discipline_boundary_sample')
        if seen[group]<2:reasons.append('category_sample')
        seen[group]+=1
        if reasons:queue.append({'question_id':row['question_id'],'review_reasons':'|'.join(reasons),
            'subject':row['subject'],'major_category':row['major_category'],'middle_category':row['middle_category'],
            'minor_category':row['minor_category'],'classification_confidence':row['classification_confidence'],
            'source_file':row['source_file'],'source_page':row['source_page'],'question_text_file':row['question_text_file']})
    write_csv('data/review_queue_checkpoint1.csv',queue)
    files=[]
    for directory in ['scripts','config','data','handoff']:
        for path in (ROOT/directory).glob('*'):
            if path.is_file() and path.name not in ['ocr_pdf','CHECKPOINT_1_FILES.csv']:
                files.append(path)
    files.extend(ROOT.glob('*.md')); files.extend([ROOT/'Makefile',ROOT/'latexmkrc',ROOT/'.gitignore'])
    snapshot=[]
    for path in sorted(set(files)):
        data=path.read_bytes();snapshot.append({'path':str(path.relative_to(ROOT)),'size_bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
    write_csv('handoff/CHECKPOINT_1_FILES.csv',snapshot)
    print(f'Checkpoint 1 package saved: {len(rows)} questions, {len(queue)} priority review rows, {len(snapshot)} tracked files')
if __name__=='__main__':main()
