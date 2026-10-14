"""Stage-aware semantic schema checks; flags require hash-bound evidence."""
import argparse,csv,json,re
from common import ROOT,read_csv,qid,digest,verification_payload_hash

STATUSES={'registered_initial','classified_initial','corrected','draft_written','explained_verified'}

def validate_rows(rows, source_rows=None, checks=None, phase='initial', staged_files=None):
    sources={r['path']:r for r in (source_rows if source_rows is not None else read_csv('data/source_files.csv'))}
    taxa=json.loads((ROOT/'config/taxonomy.json').read_text())['categories'];bytax={r['id']:r for r in taxa}
    concepts={r['id']:r for r in json.loads((ROOT/'config/concepts.json').read_text())['concepts']}
    checks=checks if checks is not None else (read_csv('data/verification_records.csv') if (ROOT/'data/verification_records.csv').exists() else [])
    ids=[r['question_id'] for r in rows];idset=set(ids);errors=[]
    fields=json.loads((ROOT/'config/question_schema.json').read_text())['fields']
    if len(ids)!=len(idset):errors.append('duplicate question ID')
    def verified(r,kind):
        payload=verification_payload_hash(r,kind)
        content=r.get('raw_text_sha256') if kind=='boundary' else r.get('corrected_content_sha256') or (r.get('raw_text_sha256') if kind=='classification' else None)
        return any(v['question_id']==r['question_id'] and v['kind']==kind and v['status']=='verified' and v['source_sha256']==r.get('source_sha256') and v.get('content_sha256')==content and (not payload or v.get('payload_sha256')==payload) and v.get('reviewer') and v.get('reviewed_at') for v in checks)
    for r in rows:
        q=r['question_id'];e=[]
        try:
            for f in fields:
                value=r.get(f['name'],'')
                if value=='':
                    if not f.get('empty_allowed',False):e.append('required field '+f['name'])
                    continue
                if f.get('allowed_values') and value not in f['allowed_values']:e.append('invalid enum '+f['name'])
                if f.get('pattern') and not re.fullmatch(f['pattern'],value):e.append('invalid pattern '+f['name'])
                if f['type'] in ('integer_string','optional_integer_string'):
                    if not re.fullmatch(r'\d+',value) or int(value)<f.get('minimum',0):e.append('invalid integer '+f['name'])
            if r['source_year_directory'] not in __import__('common').YEARS:e.append('invalid session directory')
            if r['subject'] not in ('BASIC','APT','APPLIED'):e.append('invalid subject')
            elif q!=qid(r['source_year_directory'],r['subject'],r['question_number']):e.append('ID mismatch')
            if r['year']!=r['source_year_directory'].replace('_retest',''):e.append('year mismatch')
            if r['exam_session']!=('RET' if r['source_year_directory'].endswith('_retest') else 'REG'):e.append('session mismatch')
            source=sources.get(r['source_file'])
            if not source:e.append('missing source FK')
            else:
                if not 1<=int(r['source_page'])<=int(r['source_page_end'])<=int(source['page_count']):e.append('invalid pages')
                if r.get('source_sha256') and r['source_sha256']!=source['sha256']:e.append('stale source hash')
            if int(r['heading_line_index'])<0:e.append('negative heading line')
            if r.get('end_line_index') and int(r['end_line_index'])<0:e.append('negative end line')
            if (int(r['source_page']),int(r['heading_line_index']))>(int(r['source_page_end']),int(r['end_line_index'])):e.append('reversed source span')
            box=json.loads(r['heading_bbox'])
            if set(box)!={'x','y','width','height'} or any(not isinstance(x,(int,float)) for x in box.values()):e.append('invalid bbox shape')
            elif any(not 0<=v<=1 for v in box.values()) or box['x']+box['width']>1.0001 or box['y']+box['height']>1.0001:e.append('invalid bbox range')
            endbox=json.loads(r['end_bbox'])
            if set(endbox)!={'x','y','width','height'} or any(not isinstance(v,(int,float)) or not 0<=v<=1 for v in endbox.values()):e.append('invalid end bbox')
            elif endbox['x']+endbox['width']>1.0001 or endbox['y']+endbox['height']>1.0001:e.append('invalid end bbox range')
            if r.get('official_group','')!=(r['question_number'].split('-')[0] if r['subject']=='BASIC' else ''):e.append('official group mismatch')
            for k in ['answer_verified','boundary_verified','classification_verified','summary_verified','needs_manual_verification','astra_review_required']:
                if r[k] not in ('true','false'):e.append('invalid bool '+k)
            for k in ['requires_calculation','requires_figure','requires_law']:
                if r[k] not in ('true','false','unknown'):e.append('invalid dependency '+k)
            if r['difficulty'] not in ('','1','2','3','4','5'):e.append('invalid difficulty')
            if r['priority'] not in ('','S','A','B','C'):e.append('invalid priority')
            if r['status'] not in STATUSES:e.append('invalid status')
            a=r['official_answer'];kind=r['answer_kind']
            if kind=='single' and not re.fullmatch('[1-5]',a):e.append('single answer mismatch')
            elif kind=='multiple_accepted' and (not re.fullmatch(r'[1-5](\|[1-5])+',a) or len(a.split('|'))!=len(set(a.split('|')))):e.append('multiple answer mismatch')
            elif kind=='all_awarded' and a!='ALL':e.append('ALL mismatch')
            elif kind not in ('single','multiple_accepted','all_awarded','official_note_required'):e.append('unknown answer kind')
            ans=sources.get(r['answer_source_file'])
            if not ans or not 1<=int(r['answer_source_page'])<=int(ans['page_count']):e.append('invalid answer source/page')
            if r.get('discipline_id'):
                cat=bytax.get(r['discipline_id'])
                if not cat or (cat['subject'],cat['major'],cat['middle'],cat['file'])!=(r['subject'],r['major_category'],r['middle_category'],r['tex_file']):e.append('taxonomy mismatch')
                if r.get('chapter_id')!=r['tex_file'].removeprefix('chapters/').removesuffix('.tex'):e.append('chapter mismatch')
            elif phase!='migration':e.append('missing discipline ID')
            if r.get('concept_id') and r['concept_id'] not in concepts:e.append('unknown concept')
            elif r.get('concept_id'):
                concept=concepts[r['concept_id']]
                if r['subject'] not in concept['subjects'] or concept['disciplines'] and r['discipline_id'] not in concept['disciplines']:e.append('concept outside allowed scope')
            if r.get('topic_verified')=='true' and (not r.get('concept_id') or r['classification_verified']!='true' or not verified(r,'classification')):e.append('primary concept evidence missing')
            for related in filter(None,r['related_question_ids'].split('|')):
                if related==q or related not in idset:e.append('invalid related question FK')
            if r['summary_verified']=='true' and (not r['question_summary'] or r.get('summary_status')!='verified' or not verified(r,'summary')):e.append('summary evidence missing')
            if r.get('corrected_content_sha256') or r['needs_manual_verification']=='false':
                corrected=ROOT/r.get('corrected_content_file','__missing__')
                data=(staged_files or {}).get(r.get('corrected_content_file'))
                if data is None and corrected.is_file():data=corrected.read_bytes()
                if data is None or __import__('hashlib').sha256(data).hexdigest()!=r.get('corrected_content_sha256'):e.append('corrected content missing/hash mismatch')
                elif json.loads(data).get('source_sha256')!=r.get('source_sha256') and r.get('correction_status')!='stale':e.append('corrected content stale')
                if r['needs_manual_verification']=='false' and not verified(r,'correction'):e.append('correction evidence missing')
            if r['classification_verified']=='true' and not verified(r,'classification'):e.append('classification evidence missing')
            if r['boundary_verified']=='true' and not verified(r,'boundary'):e.append('boundary evidence missing')
            if r['status']=='explained_verified':
                if r['needs_manual_verification']!='false' or r['summary_verified']!='true' or not r['solution_summary'] or not r['wrong_choice_summary'] or not verified(r,'solution'):e.append('unsubstantiated explained status')
        except (ValueError,TypeError,KeyError,json.JSONDecodeError) as ex:e.append('invalid typed field '+str(ex))
        errors.extend(q+': '+x for x in e)
    if errors:raise ValueError('\n'.join(errors[:50])+f'\nTotal schema errors: {len(errors)}')
    return True

def main():
    p=argparse.ArgumentParser();p.add_argument('--phase',choices=['initial','migration'],default='initial');a=p.parse_args()
    validate_rows(read_csv('data/questions.csv'),phase=a.phase);print('Schema verified')
if __name__=='__main__':main()
